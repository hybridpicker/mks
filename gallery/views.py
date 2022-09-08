import json
from django.shortcuts import render, redirect
from gallery.models import Photo, PhotoCategory

# Create your views here.
def gallery_view (request):
    from django.utils.datastructures import MultiValueDictKeyError
    try:
        category_id = int(request.GET['category'])
    except MultiValueDictKeyError:
        if PhotoCategory.objects.all().first() is not None:
            category_id = PhotoCategory.objects.all().order_by('ordering').first().id
        else:
            from django.http import Http404
            raise Http404
    photos = Photo.objects.filter(category_id=category_id)
    category = PhotoCategory.objects.all().exclude(title="E-Learning")

    json_photo = {}

    for photo in photos:
        photo_dict = {}
        photo_dict["title"] = photo.title
        photo_dict["description"] = photo.description
        photo_dict["image"] = photo.image.url
        json_photo[photo.id] = photo_dict

    gallery_json_data = json.dumps(json_photo)

    context = {
            'gallery_json_data': gallery_json_data,
            'category': category,
            'photos': photos,
            'category_id': category_id,
    }
    return render(request, 'gallery/gallery.html', context)
