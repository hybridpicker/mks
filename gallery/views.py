from django.shortcuts import render, redirect
from gallery.models import Photo, PhotoCategory

# Create your views here.
def gallery_view (request):
    from django.utils.datastructures import MultiValueDictKeyError
    try:
        category_id = int(request.GET['category'])
    except MultiValueDictKeyError:
            category_id = 1
    photos = Photo.objects.filter(category_id=category_id)
    category = PhotoCategory.objects.all()
    context = {
            'category': category,
            'photos': photos,
            'category_id': category_id,
    }
    return render(request, 'gallery/gallery.html', context)
