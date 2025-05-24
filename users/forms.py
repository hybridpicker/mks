from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'coordinator')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'coordinator')



from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserRole

class UserRoleForm(forms.ModelForm):
    """Form for creating and editing user roles"""
    
    class Meta:
        model = UserRole
        fields = [
            'name', 'description', 'is_active',
            'can_view_students', 'can_edit_students', 'can_delete_students',
            'can_view_teachers', 'can_edit_teachers', 'can_delete_teachers',
            'can_view_events', 'can_edit_events', 'can_delete_events',
            'can_view_gallery', 'can_edit_gallery', 'can_delete_gallery',
            'can_view_controlling', 'can_export_data',
            'can_manage_users', 'can_manage_roles'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'z.B. Koordinator, Lehrer, Assistent'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Beschreibung der Rolle und ihrer Aufgaben...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Group permissions by category
        permission_groups = {
            'Schüler-Verwaltung': [
                'can_view_students', 'can_edit_students', 'can_delete_students'
            ],
            'Lehrkräfte-Verwaltung': [
                'can_view_teachers', 'can_edit_teachers', 'can_delete_teachers'
            ],
            'Veranstaltungen': [
                'can_view_events', 'can_edit_events', 'can_delete_events'
            ],
            'Galerie': [
                'can_view_gallery', 'can_edit_gallery', 'can_delete_gallery'
            ],
            'System-Berechtigung': [
                'can_view_controlling', 'can_export_data', 
                'can_manage_users', 'can_manage_roles'
            ]
        }
        
        # Add CSS classes to all permission fields
        for group_name, permissions in permission_groups.items():
            for permission in permissions:
                if permission in self.fields:
                    self.fields[permission].widget.attrs.update({
                        'class': 'form-check-input',
                        'data-group': group_name.lower().replace('-', '_')
                    })

class UserEditForm(forms.ModelForm):
    """Form for editing user details and role assignment"""
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'username',
            'user_role', 'is_active', 'is_staff', 'coordinator'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'user_role': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Only show active roles
        self.fields['user_role'].queryset = UserRole.objects.filter(is_active=True).order_by('name')
        self.fields['user_role'].empty_label = '--- Keine Rolle ---'
        
        # Update field labels
        self.fields['first_name'].label = 'Vorname'
        self.fields['last_name'].label = 'Nachname'
        self.fields['email'].label = 'E-Mail-Adresse'
        self.fields['username'].label = 'Benutzername'
        self.fields['user_role'].label = 'Benutzerrolle'
        self.fields['is_active'].label = 'Aktiv'
        self.fields['is_staff'].label = 'Staff-Status'
        self.fields['coordinator'].label = 'Koordinator'

class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users"""
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'user_role')

class CustomUserChangeForm(UserChangeForm):
    """Form for changing user details in admin"""
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'user_role')
