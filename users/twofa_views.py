from django.shortcuts import render, redirect
from django.contrib.auth import login, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import TemplateView
from .twofa_forms import (
    TOTPSetupForm, TOTPVerificationForm, BackupCodeForm, 
    CustomAuthenticationForm, Disable2FAForm, TwoFAResetRequestForm, TwoFAResetConfirmForm
)
from .models import CustomUser


@method_decorator([csrf_protect, never_cache], name='dispatch')
class CustomLoginView(LoginView):
    """Extended login view with 2FA support"""
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        
        # Check if user has 2FA enabled
        if user.is_2fa_enabled:
            # Store user in session for 2FA verification
            self.request.session['pre_2fa_user_id'] = user.id
            return redirect('users:2fa_verify')
        
        # For users without 2FA, log them in but they'll be redirected by middleware
        user.backend = f'{get_backends()[0].__module__}.{get_backends()[0].__class__.__name__}'
        login(self.request, user)
        
        # Add message for users who need to setup 2FA
        if not user.is_2fa_enabled:
            messages.warning(
                self.request, 
                _('Für die Sicherheit Ihres Kontos müssen Sie die Zwei-Faktor-Authentifizierung einrichten.')
            )
        else:
            messages.success(self.request, _('Erfolgreich angemeldet!'))
            
        return super().form_valid(form)


@csrf_protect
@never_cache
def two_factor_verify(request):
    """Verify 2FA token after initial login"""
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        messages.error(request, _('Session expired. Please log in again.'))
        return redirect('users:login')
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, _('Invalid session. Please log in again.'))
        return redirect('users:login')
    
    if not user.is_2fa_enabled:
        messages.error(request, _('2FA is not enabled for this account.'))
        return redirect('users:login')
    
    if request.method == 'POST':
        totp_form = TOTPVerificationForm(request.POST)
        backup_form = BackupCodeForm(request.POST)
        
        # Check which form was submitted
        if 'token' in request.POST and totp_form.is_valid():
            token = totp_form.cleaned_data['token']
            if user.verify_totp(token):
                # Clear session and log in user
                del request.session['pre_2fa_user_id']
                # Use the first available backend - typically ModelBackend
                backend = get_backends()[0]
                user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
                login(request, user)
                messages.success(request, _('Successfully logged in with 2FA!'))
                return redirect(request.GET.get('next', '/team/'))
            else:
                messages.error(request, _('Invalid authentication code. Please try again.'))
        
        elif 'backup_code' in request.POST and backup_form.is_valid():
            backup_code = backup_form.cleaned_data['backup_code']
            if user.use_backup_code(backup_code):
                # Clear session and log in user
                del request.session['pre_2fa_user_id']
                # Use the first available backend - typically ModelBackend
                backend = get_backends()[0]
                user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
                login(request, user)
                messages.success(request, _('Successfully logged in using backup code!'))
                messages.warning(request, _('You have used a backup code. Consider generating new ones.'))
                return redirect(request.GET.get('next', '/team/'))
            else:
                messages.error(request, _('Invalid backup code. Please try again.'))
    else:
        totp_form = TOTPVerificationForm()
        backup_form = BackupCodeForm()
    
    context = {
        'totp_form': totp_form,
        'backup_form': backup_form,
        'user': user,
    }
    return render(request, 'users/2fa_verify.html', context)


@login_required
def setup_2fa(request):
    """Setup TOTP 2FA for user"""
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
            # Allow reuse during setup for better user experience
            if user.verify_totp(token, allow_reuse=True):
                user.is_2fa_enabled = True
                backup_codes = user.generate_backup_codes()
                user.save()
                
                messages.success(request, _('2FA has been successfully enabled!'))
                return render(request, 'users/2fa_backup_codes.html', {
                    'backup_codes': backup_codes,
                    'show_codes': True
                })
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


@login_required
def disable_2fa(request):
    """Disable 2FA for user"""
    user = request.user
    
    if not user.is_2fa_enabled:
        messages.info(request, _('2FA is not enabled for your account.'))
        return redirect('users:2fa_settings')
    
    if request.method == 'POST':
        form = Disable2FAForm(user, request.POST)
        if form.is_valid():
            user.is_2fa_enabled = False
            user.totp_secret = ''
            user.backup_codes = []
            user.save()
            
            messages.success(request, _('2FA has been disabled for your account.'))
            return redirect('users:2fa_settings')
    else:
        form = Disable2FAForm(user)
    
    return render(request, 'users/2fa_disable.html', {'form': form})


@login_required
def regenerate_backup_codes(request):
    """Regenerate backup codes"""
    user = request.user
    
    if not user.is_2fa_enabled:
        messages.error(request, _('2FA must be enabled to generate backup codes.'))
        return redirect('users:2fa_settings')
    
    if request.method == 'POST':
        backup_codes = user.generate_backup_codes()
        messages.success(request, _('New backup codes have been generated!'))
        return render(request, 'users/2fa_backup_codes.html', {
            'backup_codes': backup_codes,
            'show_codes': True
        })
    
    return render(request, 'users/2fa_regenerate_confirm.html')


@login_required
def two_factor_settings(request):
    """2FA settings page"""
    user = request.user
    context = {
        'is_2fa_enabled': user.is_2fa_enabled,
        'backup_codes_count': len(user.backup_codes) if user.backup_codes else 0,
    }
    return render(request, 'users/2fa_settings.html', context)


@csrf_protect
@never_cache
def two_factor_reset_request(request):
    """Request 2FA reset via email"""
    if request.method == 'POST':
        form = TwoFAResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email, is_2fa_enabled=True)
                user.send_2fa_reset_email()
                messages.success(request, _('Reset code has been sent to your email address.'))
                return redirect('users:2fa_reset_confirm')
            except CustomUser.DoesNotExist:
                messages.error(request, _('No account found with 2FA enabled for this email address.'))
    else:
        form = TwoFAResetRequestForm()
    
    return render(request, 'users/2fa_reset_request.html', {'form': form})


@csrf_protect
@never_cache
def two_factor_reset_confirm(request):
    """Confirm 2FA reset with email code"""
    if request.method == 'POST':
        form = TwoFAResetConfirmForm(request.POST)
        if form.is_valid():
            reset_code = form.cleaned_data['reset_code']
            # Try to find user with this reset code
            try:
                user = CustomUser.objects.get(twofa_reset_code=reset_code)
                if user.verify_2fa_reset_code(reset_code):
                    # Disable 2FA for this user
                    user.is_2fa_enabled = False
                    user.totp_secret = ''
                    user.backup_codes = []
                    user.save()
                    
                    messages.success(request, _('2FA has been successfully disabled. You can now log in normally.'))
                    return redirect('users:login')
                else:
                    messages.error(request, _('Invalid or expired reset code.'))
            except CustomUser.DoesNotExist:
                messages.error(request, _('Invalid reset code.'))
    else:
        form = TwoFAResetConfirmForm()
    
    return render(request, 'users/2fa_reset_confirm.html', {'form': form})


class TwoFactorSettingsView(TemplateView):
    """Class-based view for 2FA settings (alternative)"""
    template_name = 'users/2fa_settings.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'is_2fa_enabled': user.is_2fa_enabled,
            'backup_codes_count': len(user.backup_codes) if user.backup_codes else 0,
        })
        return context
