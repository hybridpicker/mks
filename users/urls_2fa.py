from django.urls import path, include
from . import views
from .views import HomePageView
from . import twofa_views

app_name = 'users'

urlpatterns = [
    # Existing URLs
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', HomePageView.as_view(), name='user_home'),
    path('profile/', views.user_profile, name='profile'),  # Neu: User Profile
    path('security/', views.user_security_settings, name='security_settings'),  # Neu: Security Settings
    path('events', views.eventView, name='event_managing_view'),
    path('password/change', views.change_password, name='change_password'),
    path('password/sucess', views.change_password_success, name='change_password_success'),
    path('controlling/', include('controlling.urls')),
    path('', include('todo.urls')),
    
    # 2FA URLs - alle optional
    path('2fa/verify/', twofa_views.two_factor_verify, name='2fa_verify'),
    path('2fa/setup/', twofa_views.setup_2fa, name='2fa_setup'),
    path('2fa/disable/', twofa_views.disable_2fa, name='2fa_disable'),
    path('2fa/backup-codes/regenerate/', twofa_views.regenerate_backup_codes, name='2fa_regenerate_backup'),
    path('2fa/settings/', twofa_views.two_factor_settings, name='2fa_settings'),
    path('2fa/reset-request/', twofa_views.two_factor_reset_request, name='2fa_reset_request'),
    path('2fa/reset-confirm/', twofa_views.two_factor_reset_confirm, name='2fa_reset_confirm'),
]
