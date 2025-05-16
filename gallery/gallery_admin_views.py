import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db.models import Max
import os
from django.conf import settings
from .models import Photo, PhotoCategory

# Size limit for uploads (3MB)
MAX_FILE_SIZE = 3 * 1024 * 1024
# Maximum number of files per upload
MAX_FILES = 100

@login_required
def gallery_admin_view(request):
    """
    Admin view for gallery management with drag and drop functionality.
    """
    # Get all categories
    categories = PhotoCategory.objects.all().order_by('ordering')
    
    # Get category ID from request, or use the first category if none is specified
    category_id = request.GET.get('category')
    if not category_id and categories.exists():
        category_id = categories.first().id
    
    # Get photos for the selected category
    photos = []
    if category_id:
        photos = Photo.objects.filter(category_id=category_id).order_by('-ordering')
        
        # Ensure image files exist (clean up database if images are missing)
        for photo in list(photos):
            image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
            if not os.path.exists(image_path):
                # Option 1: Delete the database entry if image doesn't exist
                # photo.delete()
                
                # Option 2: Mark that the image is missing
                photo.missing_image = True
    
    context = {
        'categories': categories,
        'selected_category_id': int(category_id) if category_id else None,
        'photos': photos,
    }
    
    return render(request, 'gallery/gallery_admin.html', context)

@csrf_exempt
@login_required
def upload_photo(request):
    """
    AJAX endpoint for uploading photos with drag and drop.
    Supports multiple file uploads.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        # Check if single or multiple upload
        is_multiple = request.POST.get('is_multiple') == 'true'
        
        if is_multiple:
            return handle_multiple_uploads(request)
        else:
            return handle_single_upload(request)
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def handle_single_upload(request):
    """
    Handle a single file upload
    """
    # Check if a file was uploaded
    if 'image' not in request.FILES:
        return JsonResponse({'status': 'error', 'message': 'No image provided'}, status=400)
    
    uploaded_file = request.FILES['image']
    
    # Check file size (3MB limit)
    if uploaded_file.size > MAX_FILE_SIZE:
        return JsonResponse({
            'status': 'error', 
            'message': f'Die Datei ist zu groß (max. 3MB). Ihre Datei ist {(uploaded_file.size / 1024 / 1024):.2f}MB.'
        }, status=400)
    
    # Get other form data
    title = request.POST.get('title', '')
    description = request.POST.get('description', '')
    copyright_by = request.POST.get('copyright_by', '')
    category_id = request.POST.get('category_id')
    
    # Validate category
    try:
        category = PhotoCategory.objects.get(id=category_id)
    except PhotoCategory.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid category'}, status=400)
    
    # Determine ordering (put new photos at the top)
    max_ordering = Photo.objects.filter(category=category).aggregate(Max('ordering'))['ordering__max']
    ordering = (max_ordering + 1) if max_ordering else 1
    
    # Create new photo
    photo = Photo(
        title=title,
        image=uploaded_file,
        description=description,
        copyright_by=copyright_by,
        category=category,
        ordering=ordering
    )
    photo.save()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Photo uploaded successfully',
        'photo': {
            'id': photo.id,
            'title': photo.title,
            'image_url': photo.image.url,
            'description': photo.description,
            'copyright_by': photo.copyright_by,
            'ordering': photo.ordering
        }
    })

def handle_multiple_uploads(request):
    """
    Handle multiple file uploads
    """
    # Get files from request
    files = request.FILES.getlist('images')
    
    # Debug log
    print(f"Multiple upload received: {len(files)} files")
    
    # Check if any files were uploaded
    if not files:
        return JsonResponse({'status': 'error', 'message': 'No images provided'}, status=400)
    
    # Check number of files
    if len(files) > MAX_FILES:
        return JsonResponse({
            'status': 'error', 
            'message': f'Zu viele Dateien. Maximal {MAX_FILES} Bilder pro Upload erlaubt.'
        }, status=400)
    
    # Get category
    category_id = request.POST.get('category_id')
    try:
        category = PhotoCategory.objects.get(id=category_id)
    except PhotoCategory.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid category'}, status=400)
    
    # Process each file
    uploaded_photos = []
    errors = []
    
    # Get max ordering to start from
    max_ordering = Photo.objects.filter(category=category).aggregate(Max('ordering'))['ordering__max'] or 0
    
    for i, uploaded_file in enumerate(files):
        try:
            # Check file size
            if uploaded_file.size > MAX_FILE_SIZE:
                errors.append(f'{uploaded_file.name}: Zu groß (max. 3MB). Datei ist {(uploaded_file.size / 1024 / 1024):.2f}MB.')
                continue
            
            # Extract filename as title (without extension)
            filename = os.path.splitext(uploaded_file.name)[0]
            title = filename[:50]  # Limit to model field length
            
            # Create photo with incremented ordering
            ordering = max_ordering + i + 1
            photo = Photo(
                title=title,
                image=uploaded_file,
                description='',  # Can be updated later
                copyright_by='',  # Can be updated later
                category=category,
                ordering=ordering
            )
            photo.save()
            
            uploaded_photos.append({
                'id': photo.id,
                'title': photo.title,
                'image_url': photo.image.url,
                'ordering': photo.ordering
            })
            
        except Exception as e:
            errors.append(f'{uploaded_file.name}: {str(e)}')
    
    # Return response
    if uploaded_photos:
        return JsonResponse({
            'status': 'success',
            'message': f'{len(uploaded_photos)} Bilder erfolgreich hochgeladen' + 
                       (f' ({len(errors)} Fehler)' if errors else ''),
            'photos': uploaded_photos,
            'errors': errors
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Keine Bilder konnten hochgeladen werden',
            'errors': errors
        }, status=400)

@login_required
def delete_photo(request, photo_id):
    """
    Delete a photo.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        photo = get_object_or_404(Photo, id=photo_id)
        photo.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Photo deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def edit_photo(request, photo_id):
    """
    Edit a photo's metadata.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        photo = get_object_or_404(Photo, id=photo_id)
        
        # Update fields from form data
        data = json.loads(request.body)
        
        if 'title' in data:
            photo.title = data['title']
        
        if 'description' in data:
            photo.description = data['description']
        
        if 'copyright_by' in data:
            photo.copyright_by = data['copyright_by']
        
        photo.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Photo updated successfully',
            'photo': {
                'id': photo.id,
                'title': photo.title,
                'description': photo.description,
                'copyright_by': photo.copyright_by
            }
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def update_order(request):
    """
    Update the order of photos.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        photo_order = data.get('photos', [])
        
        # Update each photo's ordering
        for index, photo_id in enumerate(photo_order):
            # Higher index = higher position in the list (ordering is DESC)
            ordering = len(photo_order) - index
            Photo.objects.filter(id=photo_id).update(ordering=ordering)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Photo order updated successfully'
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def create_category(request):
    """
    Create a new photo category.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        
        if not title:
            return JsonResponse({'status': 'error', 'message': 'Category title is required'}, status=400)
        
        # Get the highest ordering value
        max_ordering = PhotoCategory.objects.order_by('-ordering').first()
        ordering = (max_ordering.ordering + 1) if max_ordering else 1
        
        category = PhotoCategory(title=title, ordering=ordering)
        category.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Category created successfully',
            'category': {
                'id': category.id,
                'title': category.title,
                'ordering': category.ordering
            }
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def delete_category(request, category_id):
    """
    Delete a photo category and all its photos.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        category = get_object_or_404(PhotoCategory, id=category_id)
        
        # Check if this is the last category
        if PhotoCategory.objects.count() <= 1:
            return JsonResponse({
                'status': 'error',
                'message': 'Cannot delete the last category'
            }, status=400)
        
        category.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Category deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def edit_category(request, category_id):
    """
    Edit a category's title.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        category = get_object_or_404(PhotoCategory, id=category_id)
        
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        
        if not title:
            return JsonResponse({'status': 'error', 'message': 'Category title is required'}, status=400)
        
        category.title = title
        category.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Category updated successfully',
            'category': {
                'id': category.id,
                'title': category.title
            }
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
