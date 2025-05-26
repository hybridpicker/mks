from django.db import models
from tinymce.models import HTMLField
from django.template.defaultfilters import slugify
from teaching.subject import Subject
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime
from sorl.thumbnail import ImageField
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import uuid
from PIL import Image
import os

class Author(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    image = models.ImageField(
        upload_to='blog/author/images',
        default='author_imageDefault', blank=True,)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:  # pylint: disable=too-few-public-methods
        '''
        Meta class for Author
        '''
        ordering = ('last_name',)
        verbose_name = u'Author'
        verbose_name_plural = u'Authors'

#Function for generating year-slug-string in view
def current_year():
    return datetime.date.today().year

class BlogPost(models.Model):
    title = models.CharField(max_length=120)
    lead_paragraph = models.TextField(blank=True)
    category = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,  # Verhindert das Löschen von Blogposts, wenn die Kategorie entfernt wird
        blank=True, null=True
    )
    content = HTMLField()  # Changed from RichTextField to HTMLField for TinyMCE
    image = models.ImageField(upload_to='blog/posts/images/', blank=True, null=True)  # Bild optional
    image_alt_text = models.CharField(max_length=255, blank=True)  # Added for SEO/accessibility
    
    # Neue Felder für bessere Bildverwaltung
    image_focus_x = models.FloatField(default=0.5, help_text="Horizontal focus point (0-1, left to right)")
    image_focus_y = models.FloatField(default=0.5, help_text="Vertical focus point (0-1, top to bottom)")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False)
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,  # Optionaler Autor
        blank=True, null=True
    )
    date = models.DateField(_("Blog Post Date"), default=timezone.now, blank=True)
    meta_title = models.CharField(max_length=60, blank=True)  # Make optional
    meta_description = models.TextField(max_length=160, blank=True)  # Make optional
    slug = models.SlugField(_("slug"), max_length=200, unique=True, blank=True)  # Make optional
    ordering = models.IntegerField(null=True, blank=True)
    published = models.BooleanField(default=False)  # Added for draft/publish functionality
    updated_at = models.DateTimeField(auto_now=True)  # Added for tracking updates
    created_at = models.DateTimeField(auto_now_add=True)  # Added for tracking creation
    
    @property
    def published_year(self):
        return self.date.year

    def clean(self):
        """Custom validation with better error handling"""
        super().clean()
        
        # Auto-generate meta fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:60] if self.title else f"Blog Post {self.pk or 'New'}"
        
        if not self.meta_description and self.lead_paragraph:
            self.meta_description = self.lead_paragraph[:160]
        elif not self.meta_description:
            self.meta_description = f"Blog post about {self.title}"[:160] if self.title else "Blog post"
        
        # Generate unique slug
        if not self.slug:
            base_slug = slugify(self.title) if self.title else f"blog-post-{uuid.uuid4().hex[:8]}"
            if not base_slug:
                base_slug = f"blog-post-{uuid.uuid4().hex[:8]}"
            
            slug = base_slug
            counter = 1
            
            # Check for existing slugs and make unique
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                if counter > 100:  # Prevent infinite loop
                    slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                    break
            
            self.slug = slug

    def save(self, *args, **kwargs):
        # Always run clean before save
        try:
            self.full_clean()
        except ValidationError as e:
            # Log the error but don't crash - instead generate a fallback slug
            if 'slug' in str(e):
                self.slug = f"blog-post-{uuid.uuid4().hex[:8]}"
                # Set default meta fields if missing
                if not self.meta_title:
                    self.meta_title = self.title[:60] if self.title else f"Blog Post {self.pk or 'New'}"
                if not self.meta_description:
                    self.meta_description = self.lead_paragraph[:160] if self.lead_paragraph else "Blog post"
        
        # Simple save - image optimization is handled by signals
        super().save(*args, **kwargs)

    def optimize_banner_image(self):
        """Optimiert das Banner-Bild für bessere Performance und Format"""
        from PIL import ImageOps
        from django.core.files.base import ContentFile
        from io import BytesIO
        import os
        
        try:
            # Get original file path before any modifications
            original_path = self.image.path
            
            with Image.open(original_path) as img:
                # Metadaten speichern
                original_width, original_height = img.size
                self.image_width, self.image_height = original_width, original_height
                
                # EXIF-Rotation korrigieren
                img = ImageOps.exif_transpose(img)
                
                # Maximale Größe für Banner (performance optimization)
                max_width = 1920
                max_height = 1080
                
                # Nur optimieren wenn das Bild zu groß ist
                needs_resize = img.width > max_width or img.height > max_height
                
                if needs_resize:
                    # Create a copy for resizing
                    img_copy = img.copy()
                    img_copy.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    
                    # Optimiertes Bild speichern
                    output = BytesIO()
                    
                    # Format bestimmen
                    format_type = 'JPEG'
                    save_kwargs = {'format': format_type, 'optimize': True, 'quality': 85}
                    
                    # RGB Konvertierung für JPEG
                    if img_copy.mode in ('RGBA', 'LA', 'P'):
                        rgb_img = Image.new('RGB', img_copy.size, (255, 255, 255))
                        if img_copy.mode == 'RGBA':
                            rgb_img.paste(img_copy, mask=img_copy.split()[-1])
                        else:
                            rgb_img.paste(img_copy)
                        img_copy = rgb_img
                    
                    img_copy.save(output, **save_kwargs)
                    output.seek(0)
                    
                    # Get the current filename
                    current_name = os.path.basename(self.image.name)
                    
                    # Replace file content WITHOUT triggering save
                    self.image.delete(save=False)  # Remove old file
                    self.image.save(
                        current_name,
                        ContentFile(output.read()),
                        save=False  # CRITICAL: Don't trigger model save
                    )
                    
                    # Update dimensions to optimized size
                    self.image_width, self.image_height = img_copy.size
                else:
                    # Just update dimensions, no resize needed
                    self.image_width, self.image_height = img.size
                
        except Exception as e:
            # Bei Fehler nur Dimensionen speichern wenn möglich
            try:
                with Image.open(self.image.path) as img:
                    self.image_width, self.image_height = img.size
            except:
                # Set default dimensions if all else fails
                self.image_width, self.image_height = None, None

    @property
    def image_aspect_ratio(self):
        """Calculate the aspect ratio of the image"""
        if self.image_width and self.image_height:
            return self.image_width / self.image_height
        return 16/9  # Default banner aspect ratio
    
    @property
    def is_image_landscape(self):
        """Check if image is landscape oriented"""
        return self.image_aspect_ratio > 1.2
    
    @property
    def is_image_portrait(self):
        """Check if image is portrait oriented"""
        return self.image_aspect_ratio < 0.8
    
    @property
    def is_image_square(self):
        """Check if image is square oriented"""
        ratio = self.image_aspect_ratio
        return 0.8 <= ratio <= 1.2
    
    @property
    def optimal_banner_class(self):
        """Returns CSS class for optimal banner display"""
        if self.is_image_portrait:
            return "portrait-banner"
        elif self.image_aspect_ratio > 3:
            return "wide-banner"
        else:
            return "standard-banner"

    def __str__(self):
        return f"{self.title} ({self.date.year})"

    class Meta:
        ordering = ('category', '-date', 'ordering')
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

class GalleryImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(
        upload_to='blog/gallery/images/', 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
    
    def __str__(self):
        return f"{self.blog_post.title} - Image {self.order}"
