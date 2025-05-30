from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from . import gallery_admin_views
from . import views_optimized  # Neue optimierte Views

urlpatterns = [
    # Original Gallery Views
    path('galerie', views.gallery_view, name='gallery_view'),
    path('galerie/', views.gallery_view, name='gallery_view_slash'),
    
    # Optimierte Gallery mit Lazy Loading
    path('galerie/optimized/', views_optimized.gallery_view_optimized, name='gallery_optimized'),
    path('gallery/load-more/', views_optimized.load_more_photos, name='gallery_load_more'),
    
    # Gallery admin views
    path('galerie/admin/', gallery_admin_views.gallery_admin_view, name='gallery_admin'),
    path('galerie/admin/upload/', gallery_admin_views.upload_photo, name='gallery_upload'),
    path('galerie/admin/delete/<int:photo_id>/', gallery_admin_views.delete_photo, name='gallery_delete_photo'),
    path('galerie/admin/edit/<int:photo_id>/', gallery_admin_views.edit_photo, name='gallery_edit_photo'),
    path('galerie/admin/order/', gallery_admin_views.update_order, name='gallery_update_order'),
    path('galerie/admin/category/create/', gallery_admin_views.create_category, name='gallery_create_category'),
    path('galerie/admin/category/delete/<int:category_id>/', gallery_admin_views.delete_category, name='gallery_delete_category'),
    path('galerie/admin/category/edit/<int:category_id>/', gallery_admin_views.edit_category, name='gallery_edit_category'),
]