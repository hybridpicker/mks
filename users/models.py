
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext as _
from django.db import models
import pyotp
import qrcode
from io import BytesIO
import base64

class UserRole(models.Model):
    """Custom user roles with specific permissions"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Rollenname')
    description = models.TextField(blank=True, verbose_name='Beschreibung')
    is_active = models.BooleanField(default=True, verbose_name='Aktiv')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Permission categories
    can_view_students = models.BooleanField(default=False, verbose_name='Schüler anzeigen')
    can_edit_students = models.BooleanField(default=False, verbose_name='Schüler bearbeiten')
    can_delete_students = models.BooleanField(default=False, verbose_name='Schüler löschen')
    
    can_view_teachers = models.BooleanField(default=False, verbose_name='Lehrkräfte anzeigen')
    can_edit_teachers = models.BooleanField(default=False, verbose_name='Lehrkräfte bearbeiten')
    can_delete_teachers = models.BooleanField(default=False, verbose_name='Lehrkräfte löschen')
    
    can_view_events = models.BooleanField(default=False, verbose_name='Veranstaltungen anzeigen')
    can_edit_events = models.BooleanField(default=False, verbose_name='Veranstaltungen bearbeiten')
    can_delete_events = models.BooleanField(default=False, verbose_name='Veranstaltungen löschen')
    
    can_view_gallery = models.BooleanField(default=False, verbose_name='Galerie anzeigen')
    can_edit_gallery = models.BooleanField(default=False, verbose_name='Galerie bearbeiten')
    can_delete_gallery = models.BooleanField(default=False, verbose_name='Galerie löschen')
    
    can_view_controlling = models.BooleanField(default=False, verbose_name='Controlling anzeigen')
    can_export_data = models.BooleanField(default=False, verbose_name='Daten exportieren')
    
    can_manage_users = models.BooleanField(default=False, verbose_name='Benutzer verwalten')
    can_manage_roles = models.BooleanField(default=False, verbose_name='Rollen verwalten')
    
    class Meta:
        verbose_name = 'Benutzerrolle'
        verbose_name_plural = 'Benutzerrollen'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_permission_summary(self):
        """Get a summary of permissions for this role"""
        permissions = []
        
        if self.can_view_students: permissions.append('Schüler anzeigen')
        if self.can_edit_students: permissions.append('Schüler bearbeiten')
        if self.can_delete_students: permissions.append('Schüler löschen')
        
        if self.can_view_teachers: permissions.append('Lehrkräfte anzeigen')
        if self.can_edit_teachers: permissions.append('Lehrkräfte bearbeiten')
        if self.can_delete_teachers: permissions.append('Lehrkräfte löschen')
        
        if self.can_view_events: permissions.append('Events anzeigen')
        if self.can_edit_events: permissions.append('Events bearbeiten')
        if self.can_delete_events: permissions.append('Events löschen')
        
        if self.can_view_gallery: permissions.append('Galerie anzeigen')
        if self.can_edit_gallery: permissions.append('Galerie bearbeiten')
        if self.can_delete_gallery: permissions.append('Galerie löschen')
        
        if self.can_view_controlling: permissions.append('Controlling')
        if self.can_export_data: permissions.append('Export')
        
        if self.can_manage_users: permissions.append('Benutzer verwalten')
        if self.can_manage_roles: permissions.append('Rollen verwalten')
        
        return permissions

class CustomUser(AbstractUser):
    first_name = models.CharField(_(u'First Name'), max_length=30)
    last_name = models.CharField(_(u'Last Name'), max_length=30)
    coordinator = models.BooleanField(default=False)
    
    # Role assignment
    user_role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True, 
                                 verbose_name='Benutzerrolle', related_name='users')
    
    # 2FA fields
    totp_secret = models.CharField(max_length=32, blank=True, null=True, help_text="TOTP secret key")
    is_2fa_enabled = models.BooleanField(default=False, help_text="Two-Factor Authentication enabled")
    backup_codes = models.JSONField(default=list, blank=True, help_text="Backup codes for 2FA")

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_role_name(self):
        """Get the name of the user's role"""
        return self.user_role.name if self.user_role else 'Keine Rolle'
    
    def has_permission(self, permission):
        """Check if user has a specific permission"""
        if self.is_superuser:
            return True
        
        if not self.user_role or not self.user_role.is_active:
            return False
        
        return getattr(self.user_role, permission, False)
    
    def get_permissions_list(self):
        """Get list of user's permissions"""
        if self.is_superuser:
            return ['Alle Berechtigungen (Superuser)']
        
        if not self.user_role:
            return ['Keine Berechtigungen']
        
        return self.user_role.get_permission_summary()

    def generate_totp_secret(self):
        """Generate a new TOTP secret for the user"""
        if not self.totp_secret:
            self.totp_secret = pyotp.random_base32()
            self.save()
        return self.totp_secret

    def get_totp_uri(self):
        """Get the TOTP URI for QR code generation"""
        if not self.totp_secret:
            self.generate_totp_secret()
        
        totp = pyotp.TOTP(self.totp_secret)
        return totp.provisioning_uri(
            name=self.email,
            issuer_name="MKS Portal"
        )

    def get_qr_code(self):
        """Generate QR code for TOTP setup"""
        uri = self.get_totp_uri()
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Convert to base64 for HTML embedding
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    def verify_totp(self, token, allow_reuse=False):
        """Verify TOTP token with improved tolerance"""
        if not self.totp_secret:
            return False
        
        # Clean token (remove spaces, ensure 6 digits)
        token = str(token).replace(' ', '').strip()
        if len(token) != 6 or not token.isdigit():
            return False
        
        totp = pyotp.TOTP(self.totp_secret)
        
        # For setup, we allow reuse since users might need to try multiple times
        if allow_reuse:
            # Try current time window first
            if totp.verify(token, valid_window=0):
                return True
                
            # Try with wider window for clock synchronization issues
            return totp.verify(token, valid_window=2)
        else:
            # For login, standard verification (prevents replay attacks)
            return totp.verify(token, valid_window=1)

    def generate_backup_codes(self):
        """Generate backup codes for 2FA recovery"""
        import secrets
        codes = []
        for _ in range(10):  # Generate 10 backup codes
            code = '-'.join([secrets.token_hex(2) for _ in range(3)])
            codes.append(code)
        
        self.backup_codes = codes
        self.save()
        return codes

    def use_backup_code(self, code):
        """Use a backup code (one-time use)"""
        if code in self.backup_codes:
            self.backup_codes.remove(code)
            self.save()
            return True
        return False

    class Meta:
        verbose_name = u'User'
        verbose_name_plural = u'Users'
