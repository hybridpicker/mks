import glob, os
from gallery.models import Photo
import shutil

def save_pics(path, gallery_id):

    os.chdir(path)
    photo_ordering = Photo.objects.all().filter(category_id=gallery_id).latest('ordering').ordering
    for file in sorted(glob.glob("*")):
        photo_ordering += 1
        new_file = Photo.objects.create(title=str(file),
                                        images="gallery/images/" + file,
                                        category_id=gallery_id,
                                        ordering=photo_ordering)
        new_file.save()
        print(new_file)
