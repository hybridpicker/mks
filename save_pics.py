import glob, os
from gallery.models import Photo
import shutil

def save_pics():

    directories = ['/Users/lukasschonsgibl/Desktop/MS St. Pölten/gallery/Ensembles',
                   '/Users/lukasschonsgibl/Desktop/MS St. Pölten/gallery/Standort',
                   '/Users/lukasschonsgibl/Desktop/MS St. Pölten/gallery/Wettbewerbe',]

    c = 1
    for dir in directories:
        os.chdir(dir)
        i = 1
        for file in sorted(glob.glob("*")):
            new_file = Photo.objects.create(title=str(file),
                                            images="gallery/images/" + file,
                                            category_id=int(c),
                                            ordering=int(i))
            new_file.save()
            i += 1
            print(new_file)
        c +=1
