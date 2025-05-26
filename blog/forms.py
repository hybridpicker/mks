from tinymce.widgets import TinyMCE
from django.utils.translation import gettext as _
from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .models import Author, BlogPost, GalleryImage
from teaching.subject import Subject
import uuid
import logging

logger = logging.getLogger(__name__)

class ArticleForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        label=_("Content")
    )
    
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter blog title'),
        }),
        label=_("Title"),
        max_length=120
    )
    
    lead_paragraph = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': _('Enter lead paragraph - this will appear as preview text'),
        }),
        label=_("Lead Paragraph"),
        required=False
    )
    
    slug = forms.SlugField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('leave-blank-to-auto-generate')
        }),
        label=_("Slug (URL)"),
        required=False,
        help_text=_("Leave blank to auto-generate from title"),
        max_length=200
    )
    
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label=_("Featured Image"),
        required=False
    )
    
    image_alt_text = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Describe the image for accessibility'),
        }),
        label=_("Image Alt Text"),
        required=False,
        max_length=255
    )
    
    meta_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('SEO title (appears in search results)'),
            'maxlength': '60'
        }),
        label=_("SEO Title"),
        required=False,
        help_text=_("60 characters max. If blank, will use blog title."),
        max_length=60
    )
    
    meta_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': _('SEO description (appears in search results)'),
            'maxlength': '160'
        }),
        label=_("SEO Description"),
        required=False,
        help_text=_("160 characters max. If blank, will use lead paragraph."),
        max_length=160
    )
    
    category = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_("Category"),
        required=False
    )
    
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_("Author"),
        required=False
    )
    
    published = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label=_("Publish"),
        required=False,
        help_text=_("Check to make this post public")
    )
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'lead_paragraph', 'content', 'image', 'image_alt_text',
            'category', 'author', 'slug', 'published', 'meta_title', 'meta_description'
        ]

    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError(_("Title is required."))
        if len(title.strip()) < 3:
            raise ValidationError(_("Title must be at least 3 characters long."))
        return title.strip()

    def clean_slug(self):
        """Generate and validate slug"""
        slug = self.cleaned_data.get('slug')
        title = self.cleaned_data.get('title', '')
        
        # Generate slug if not provided
        if not slug and title:
            slug = slugify(title)
        elif slug:
            slug = slugify(slug)
        
        # Fallback if slug generation fails
        if not slug:
            slug = f"blog-post-{uuid.uuid4().hex[:8]}"
            logger.warning(f"Generated fallback slug: {slug}")
        
        # Check for duplicate slugs
        qs = BlogPost.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            # Try to make it unique
            counter = 1
            original_slug = slug
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.instance.pk if self.instance.pk else 0).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
                if counter > 100:  # Prevent infinite loop
                    slug = f"{original_slug}-{uuid.uuid4().hex[:8]}"
                    break
        
        return slug
    
    def clean_meta_title(self):
        """Auto-generate meta title if not provided"""
        meta_title = self.cleaned_data.get('meta_title')
        if not meta_title:
            title = self.cleaned_data.get('title', '')
            meta_title = title[:60] if title else 'Blog Post'
        return meta_title
    
    def clean_meta_description(self):
        """Auto-generate meta description if not provided"""
        meta_description = self.cleaned_data.get('meta_description')
        if not meta_description:
            lead_paragraph = self.cleaned_data.get('lead_paragraph', '')
            if lead_paragraph:
                meta_description = lead_paragraph[:160]
            else:
                title = self.cleaned_data.get('title', '')
                meta_description = f"Blog post about {title}"[:160] if title else "Blog post"
        return meta_description

    def clean_content(self):
        """Validate content"""
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 10:
            raise ValidationError(_("Content must be at least 10 characters long."))
        return content

    def clean_image(self):
        """Validate image file"""
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 10MB)
            if image.size > 10 * 1024 * 1024:
                raise ValidationError(_("Image file too large (max 10MB)."))
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise ValidationError(_("Invalid image format. Please use JPG, PNG, GIF, or WebP."))
        
        return image

    def save(self, commit=True):
        """Override save to ensure required fields are populated"""
        instance = super().save(commit=False)
        
        # Ensure meta fields are populated
        if not instance.meta_title:
            instance.meta_title = instance.title[:60] if instance.title else 'Blog Post'
        if not instance.meta_description and instance.lead_paragraph:
            instance.meta_description = instance.lead_paragraph[:160]
        elif not instance.meta_description:
            instance.meta_description = f"Blog post about {instance.title}"[:160] if instance.title else "Blog post"
        
        if commit:
            try:
                instance.save()
            except Exception as e:
                logger.error(f"Error saving blog post: {e}")
                raise ValidationError(f"Error saving blog post: {e}")
        
        return instance
        
class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'caption', 'alt_text']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control gallery-image-input',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Caption (optional)'),
                'maxlength': '255'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Alt text for accessibility (optional)'),
                'maxlength': '255'
            })
        }

    def clean_image(self):
        """Validate gallery image"""
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 10MB)
            if image.size > 10 * 1024 * 1024:
                raise ValidationError(_("Image file too large (max 10MB)."))
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise ValidationError(_("Invalid image format. Please use JPG, PNG, GIF, or WebP."))
        
        return image

# Custom formset with better error handling
class BaseGalleryImageFormSet(forms.BaseInlineFormSet):
    def clean(self):
        """Add custom validation for the entire formset"""
        if any(self.errors):
            return
        
        # Check that we don't have too many images
        valid_forms = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                valid_forms += 1
        
        if valid_forms > 10:  # Max 10 gallery images
            raise ValidationError(_("Maximum 10 gallery images allowed."))

GalleryImageFormSet = forms.inlineformset_factory(
    BlogPost, 
    GalleryImage, 
    form=GalleryImageForm,
    formset=BaseGalleryImageFormSet,
    extra=3,
    can_delete=True,
    max_num=10,
    validate_max=True
)