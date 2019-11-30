from django.urls import path, include
from . import views
from .views import HomePageView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', HomePageView.as_view(), name='user_home'),
    path('events', views.eventView, name='event_managing_view'),
    path('password/', views.change_password, name='change_password'),
    path('controlling/', include('controlling.urls')),
]
