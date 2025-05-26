from tinymce.widgets import TinyMCE
from django.utils.translation import gettext as _
from django import forms
from django.utils.text import slugify  # Hinzugefügt
from .models import Author, BlogPost, GalleryImage
from teaching.subject import Subject

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
        label=_("Title")
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
        help_text=_("Leave blank to auto-generate from title")
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
        required=False
    )
    
    meta_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('SEO title (appears in search results)'),
            'maxlength': '60'
        }),
        label=_("SEO Title"),
        required=False,
        help_text=_("60 characters max. If blank, will use blog title.")
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
        help_text=_("160 characters max. If blank, will use lead paragraph.")
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

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            slug = slugify(self.cleaned_data.get('title', ''))
        else:
            slug = slugify(slug)
        
        # Check for duplicate slugs
        qs = BlogPost.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_("This slug is already in use."))
        
        return slug
    
    def clean_meta_title(self):
        meta_title = self.cleaned_data.get('meta_title')
        if not meta_title:
            meta_title = self.cleaned_data.get('title', '')
        return meta_title[:60]  # Ensure it's not too long
    
    def clean_meta_description(self):
        meta_description = self.cleaned_data.get('meta_description')
        if not meta_description:
            meta_description = self.cleaned_data.get('lead_paragraph', '')
        return meta_description[:160]  # Ensure it's not too long
        
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
                'placeholder': _('Caption (optional)')
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Alt text for accessibility (optional)')
            })
        }
        
GalleryImageFormSet = forms.inlineformset_factory(
    BlogPost, 
    GalleryImage, 
    form=GalleryImageForm,
    extra=3,
    can_delete=True,
    max_num=10
)