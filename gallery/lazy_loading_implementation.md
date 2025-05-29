# Lazy Loading Implementation für Gallery

## 1. Änderungen in templates/gallery/gallery.html

### Im `{% block extra_head %}` nach dem bestehenden CSS hinzufügen:
```html
<link rel="stylesheet" href="{% static 'gallery/css/lazy-loading.css' %}">
```

### Ersetze jeden img Tag in der Gallery mit folgendem Pattern:

#### Vorher:
```html
<img src="{{ photo.image.url }}" 
    alt="{{ photo.title|default:'Gallery Image' }}"
    style="width: 100%; height: 100%; object-fit: cover; display: block;">
```

#### Nachher:
```html
<img class="lazy" 
    src="{% if photo.image_lazy %}{{ photo.image_lazy.url }}{% else %}data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjIwIiBoZWlnaHQ9IjIyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjIwIiBoZWlnaHQ9IjIyMCIgZmlsbD0iI2YwZjBmMCIvPjwvc3ZnPg=={% endif %}"
    data-src="{{ photo.image.url }}" 
    alt="{{ photo.title|default:'Gallery Image' }}"
    style="width: 100%; height: 100%; object-fit: cover; display: block;">
<noscript>
    <img src="{{ photo.image.url }}" alt="{{ photo.title|default:'Gallery Image' }}" style="width: 100%; height: 100%; object-fit: cover; display: block;">
</noscript>
```

### Füge die "loading" Klasse zu jedem gallery-item div hinzu:

#### Vorher:
```html
<div class="landscape gallery-item" onclick="showImg({{photo.id}})" style="...">
```

#### Nachher:
```html
<div class="landscape gallery-item loading" onclick="showImg({{photo.id}})" style="...">
```

### Im `{% block footer %}` vor dem schließenden script Tag hinzufügen:
```html
<script src="{% static 'gallery/js/lazy-loading.js' %}"></script>
```

## 2. Änderungen in gallery/views.py (Optional aber empfohlen)

Stelle sicher, dass lazy images generiert werden beim Upload:
```python
# In gallery/views.py die gallery_view Funktion erweitern:

def gallery_view(request):
    # Alle Fotos aus allen Kategorien laden (außer von E-Learning)
    all_photos = Photo.objects.exclude(category__title="E-Learning").order_by('-ordering')
    
    # Filterung der Fotos, um sicherzustellen, dass die Bilddateien existieren
    photos = []
    for photo in all_photos:
        # Prüfen, ob Bilddatei existiert
        image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
        if os.path.exists(image_path):
            photos.append(photo)
            
            # Prüfe ob lazy image existiert, wenn nicht, generiere es
            if photo.image and not photo.image_lazy:
                try:
                    from gallery.image_utils import create_lazy_image
                    lazy_image = create_lazy_image(photo.image)
                    if lazy_image:
                        photo.image_lazy.save(lazy_image.name, lazy_image, save=True)
                        logger.info(f"Lazy image erstellt für Photo ID: {photo.id}")
                except Exception as e:
                    logger.error(f"Fehler beim Erstellen des Lazy Images: {e}")
        else:
            logger.warning(f"Bild nicht gefunden: {photo.image.name} (ID: {photo.id})")
    
    # Rest des Codes bleibt gleich...
```

## 3. Änderungen in gallery/admin.py (für automatische Lazy Image Generierung)

```python
# In der save_model Methode des Photo Admin:

from gallery.image_utils import process_uploaded_image

def save_model(self, request, obj, form, change):
    if 'image' in form.changed_data and obj.image:
        # Verarbeite das hochgeladene Bild
        processed = process_uploaded_image(obj.image)
        
        if processed['main']:
            obj.image = processed['main']
        
        if processed['thumbnail']:
            obj.image_thumbnail = processed['thumbnail']
        
        if processed['lazy']:
            obj.image_lazy = processed['lazy']
    
    super().save_model(request, obj, form, change)
```

## 4. Management Command zum Generieren von Lazy Images für existierende Bilder

Erstelle: gallery/management/commands/generate_lazy_images.py