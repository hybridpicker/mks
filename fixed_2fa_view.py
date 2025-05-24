@login_required
def setup_2fa(request):
    """Setup TOTP 2FA for user - Fixed version"""
    user = request.user
    
    if user.is_2fa_enabled:
        messages.info(request, _('2FA is already enabled for your account.'))
        return redirect('users:2fa_settings')
    
    # Generate secret if not exists
    user.generate_totp_secret()
    
    if request.method == 'POST':
        form = TOTPSetupForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            
            # Verify token
            if user.verify_totp(token, allow_reuse=True):
                try:
                    # WICHTIG: Atomare Transaktion für 2FA-Aktivierung
                    from django.db import transaction
                    
                    with transaction.atomic():
                        user.is_2fa_enabled = True
                        backup_codes = user.generate_backup_codes()
                        user.save()
                        
                        # Session-Flag setzen um Middleware-Konflikte zu vermeiden
                        request.session['2fa_just_setup'] = True
                    
                    messages.success(request, _('2FA has been successfully enabled!'))
                    
                    # Direct return - kein Redirect der vom Middleware abgefangen werden kann
                    return render(request, 'users/2fa_backup_codes.html', {
                        'backup_codes': backup_codes,
                        'show_codes': True
                    })
                    
                except Exception as e:
                    # Log error if possible
                    messages.error(request, _('Error saving 2FA settings. Please try again.'))
            else:
                messages.error(request, _('Invalid code. Please try again. Make sure your device time is synchronized and wait for a new code if necessary.'))
    else:
        form = TOTPSetupForm()
    
    context = {
        'form': form,
        'qr_code': user.get_qr_code(),
        'secret': user.totp_secret,
    }
    return render(request, 'users/2fa_setup.html', context)
