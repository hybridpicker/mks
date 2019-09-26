from django.urls import path, include
from . import views
from .views import HomePageView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('home', HomePageView.as_view(), name='home'),
]
