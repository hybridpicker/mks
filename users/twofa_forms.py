from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class TOTPSetupForm(forms.Form):
    token = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter 6-digit code from your authenticator app'),
            'autocomplete': 'one-time-code',
            'pattern': '[0-9]{6}',
            'inputmode': 'numeric'
        }),
        label=_('Authentication Code')
    )

    def clean_token(self):
        token = self.cleaned_data.get('token')
        if not token or len(token) != 6 or not token.isdigit():
            raise forms.ValidationError(_('Please enter a valid 6-digit authentication code.'))
        return token


class TOTPVerificationForm(forms.Form):
    token = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter 6-digit code'),
            'autocomplete': 'one-time-code',
            'pattern': '[0-9]{6}',
            'inputmode': 'numeric',
            'autofocus': True
        }),
        label=_('Authentication Code')
    )

    def clean_token(self):
        token = self.cleaned_data.get('token')
        if not token or len(token) != 6 or not token.isdigit():
            raise forms.ValidationError(_('Please enter a valid 6-digit authentication code.'))
        return token


class BackupCodeForm(forms.Form):
    backup_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter backup code (e.g., a1b2-c3d4-e5f6)'),
            'autocomplete': 'one-time-code'
        }),
        label=_('Backup Code')
    )

    def clean_backup_code(self):
        code = self.cleaned_data.get('backup_code', '').strip()
        if not code:
            raise forms.ValidationError(_('Please enter a backup code.'))
        return code


class CustomAuthenticationForm(AuthenticationForm):
    """Extended authentication form with 2FA support"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Username or Email')
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Password')
        })


class Disable2FAForm(forms.Form):
    """Form to disable 2FA with password confirmation"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your password to disable 2FA')
        }),
        label=_('Current Password')
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError(_('Incorrect password.'))
        return password
