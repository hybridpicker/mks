from django.contrib import admin
from django.urls import path
from faq import views

urlpatterns = [
    path('faq', views.faq_view, name='faq_view'),
    path('edit/get-all-faqs', views.get_all_faqs, name='get_all_faqs'),
    path('edit/get-faq', views.get_faq, name='get_faq'),
    path('edit/create-faq', views.create_faq, name='create_faq'),
]