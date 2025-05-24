import logging

# Add to the top of twofa_views.py
logger = logging.getLogger(__name__)

@login_required
def setup_2fa(request):
    """Setup TOTP 2FA for user with enhanced logging"""
    user = request.user
    logger.info(f"2FA setup started for user: {user.email}")
    
    if user.is_2fa_enabled:
        logger.warning(f"2FA already enabled for user: {user.email}")
        messages.info(request, _('2FA is already enabled for your account.'))
        return redirect('users:2fa_settings')
    
    # Generate secret if not exists
    try:
        user.generate_totp_secret()
        logger.info(f"TOTP secret generated for user: {user.email}")
    except Exception as e:
        logger.error(f"Failed to generate TOTP secret for user {user.email}: {e}")
        messages.error(request, _('Error setting up 2FA. Please try again.'))
        return redirect('users:2fa_settings')
    
    if request.method == 'POST':
        logger.info(f"2FA setup POST request for user: {user.email}")
        form = TOTPSetupForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            logger.info(f"Token submitted for verification: {token}")
            
            # Allow reuse during setup for better user experience
            try:
                is_valid = user.verify_totp(token, allow_reuse=True)
                logger.info(f"Token verification result for user {user.email}: {is_valid}")
                
                if is_valid:
                    try:
                        user.is_2fa_enabled = True
                        backup_codes = user.generate_backup_codes()
                        user.save()
                        logger.info(f"2FA successfully enabled for user: {user.email}")
                        
                        messages.success(request, _('2FA has been successfully enabled!'))
                        return render(request, 'users/2fa_backup_codes.html', {
                            'backup_codes': backup_codes,
                            'show_codes': True
                        })
                    except Exception as e:
                        logger.error(f"Failed to save 2FA settings for user {user.email}: {e}")
                        messages.error(request, _('Error saving 2FA settings. Please try again.'))
                else:
                    logger.warning(f"Invalid token submitted by user: {user.email}")
                    messages.error(request, _('Invalid code. Please try again. Make sure your device time is synchronized and wait for a new code if necessary.'))
            except Exception as e:
                logger.error(f"Token verification failed for user {user.email}: {e}")
                messages.error(request, _('Error verifying code. Please try again.'))
        else:
            logger.warning(f"Invalid form submission for user: {user.email}, errors: {form.errors}")
    else:
        form = TOTPSetupForm()
    
    try:
        context = {
            'form': form,
            'qr_code': user.get_qr_code(),
            'secret': user.totp_secret,
        }
        logger.info(f"Rendering 2FA setup page for user: {user.email}")
        return render(request, 'users/2fa_setup.html', context)
    except Exception as e:
        logger.error(f"Error rendering 2FA setup page for user {user.email}: {e}")
        messages.error(request, _('Error loading 2FA setup page. Please try again.'))
        return redirect('users:2fa_settings')
