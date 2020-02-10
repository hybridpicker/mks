from django.urls import path, include
from . import views
from .views import HomePageView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', HomePageView.as_view(), name='user_home'),
    path('events', views.eventView, name='event_managing_view'),
    path('password/change', views.change_password, name='change_password'),
    path('password/sucess', views.change_password_success, name='change_password_success'),
    path('controlling/', include('controlling.urls')),
    path('', include('todo.urls')),
]
