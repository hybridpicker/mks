@login_required
def user_profile(request):
    """User profile page with optional 2FA settings"""
    user = request.user
    
    context = {
        'user': user,
        'is_2fa_enabled': user.is_2fa_enabled,
        'backup_codes_count': len(user.backup_codes) if user.backup_codes else 0,
    }
    
    return render(request, 'users/profile.html', context)


@login_required  
def user_security_settings(request):
    """Security settings page with 2FA options"""
    user = request.user
    
    context = {
        'user': user,
        'is_2fa_enabled': user.is_2fa_enabled,
        'backup_codes_count': len(user.backup_codes) if user.backup_codes else 0,
        'show_2fa_info': True,  # Show 2FA as optional security enhancement
    }
    
    return render(request, 'users/security_settings.html', context)
