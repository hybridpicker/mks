from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from blog.models import Author, BlogPost, GalleryImage

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ('image', 'caption', 'alt_text', 'order')
    ordering = ('order',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'has_bio', 'has_image')
    search_fields = ('first_name', 'last_name')
    list_filter = ('last_name',)
    
    def has_bio(self, obj):
        return bool(obj.bio)
    has_bio.boolean = True
    has_bio.short_description = 'Has Bio'
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'date', 'published', 'image_preview', 'image_info')
    list_filter = ('published', 'category', 'author', 'date')
    search_fields = ('title', 'lead_paragraph', 'content', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'image_width', 'image_height', 'image_focus_controls')
    ordering = ('-date',)
    inlines = [GalleryImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'lead_paragraph', 'content')
        }),
        ('Banner Image', {
            'fields': ('image', 'image_alt_text', 'image_focus_controls'),
            'description': 'Upload a banner image and set the focus point by clicking on the preview.'
        }),
        ('Image Settings (Auto-filled)', {
            'fields': ('image_focus_x', 'image_focus_y', 'image_width', 'image_height'),
            'classes': ('collapse',)
        }),
        ('Organization', {
            'fields': ('category', 'author', 'date', 'ordering')
        }),
        ('SEO', {
            'fields': ('slug', 'meta_title', 'meta_description')
        }),
        ('Publishing', {
            'fields': ('published',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        """Shows a small preview of the banner image"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 60px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;">',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Preview"
    
    def image_info(self, obj):
        """Shows image dimensions and aspect ratio info"""
        if obj.image_width and obj.image_height:
            ratio = obj.image_aspect_ratio
            if ratio > 1.2:
                orientation = "Landscape"
                color = "#10b981"  # green
            elif ratio < 0.8:
                orientation = "Portrait"
                color = "#f59e0b"  # amber
            else:
                orientation = "Square"
                color = "#6b7280"  # gray
            
            return format_html(
                '<span style="color: {}; font-weight: 500;">{} ({}×{})</span><br>'
                '<span style="font-size: 11px; color: #6b7280;">Ratio: {:.2f}</span>',
                color, orientation, obj.image_width, obj.image_height, ratio
            )
        return "Unknown"
    image_info.short_description = "Image Info"
    
    def image_focus_controls(self, obj):
        """Interactive focus point selector"""
        if not obj.image:
            return "Upload an image first"
        
        focus_x_percent = (obj.image_focus_x or 0.5) * 100
        focus_y_percent = (obj.image_focus_y or 0.5) * 100
        
        return mark_safe(f'''
            <div style="max-width: 500px;">
                <div id="focus-point-selector" style="position: relative; border: 2px solid #e5e7eb; border-radius: 8px; overflow: hidden; cursor: crosshair; background: #f9fafb;">
                    <img src="{obj.image.url}" style="width: 100%; height: 250px; object-fit: cover; display: block;" id="focus-image">
                    <div id="focus-indicator" style="position: absolute; width: 16px; height: 16px; background: #ef4444; border: 3px solid white; border-radius: 50%; transform: translate(-50%, -50%); left: {focus_x_percent}%; top: {focus_y_percent}%; cursor: move; box-shadow: 0 2px 8px rgba(0,0,0,0.3); z-index: 10;"></div>
                    <div style="position: absolute; top: 8px; right: 8px; background: rgba(0,0,0,0.7); color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px;">
                        Click to set focus point
                    </div>
                </div>
                <div style="margin-top: 12px; font-size: 12px; color: #6b7280; display: flex; justify-content: space-between;">
                    <span>Focus: X={obj.image_focus_x:.3f}, Y={obj.image_focus_y:.3f}</span>
                    <span>Banner will crop around this point</span>
                </div>
            </div>
            <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const container = document.getElementById('focus-point-selector');
                const indicator = document.getElementById('focus-indicator');
                const xField = document.getElementById('id_image_focus_x');
                const yField = document.getElementById('id_image_focus_y');
                
                if (container && indicator && xField && yField) {{
                    container.addEventListener('click', function(e) {{
                        const rect = this.getBoundingClientRect();
                        const x = (e.clientX - rect.left) / rect.width;
                        const y = (e.clientY - rect.top) / rect.height;
                        
                        // Constrain to 0-1 range
                        const clampedX = Math.max(0, Math.min(1, x));
                        const clampedY = Math.max(0, Math.min(1, y));
                        
                        // Update form fields
                        xField.value = clampedX.toFixed(3);
                        yField.value = clampedY.toFixed(3);
                        
                        // Move indicator
                        indicator.style.left = (clampedX * 100) + '%';
                        indicator.style.top = (clampedY * 100) + '%';
                        
                        // Visual feedback
                        indicator.style.transform = 'translate(-50%, -50%) scale(1.2)';
                        setTimeout(() => {{
                            indicator.style.transform = 'translate(-50%, -50%) scale(1)';
                        }}, 200);
                    }});
                }}
            }});
            </script>
        ''')
    image_focus_controls.short_description = "Focus Point"
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'lead_paragraph', 'content')
        }),
        ('Media', {
            'fields': ('image', 'image_alt_text')
        }),
        ('Organization', {
            'fields': ('category', 'author', 'date', 'ordering')
        }),
        ('SEO', {
            'fields': ('slug', 'meta_title', 'meta_description')
        }),
        ('Publishing', {
            'fields': ('published',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_published', 'make_unpublished']
    
    def make_published(self, request, queryset):
        updated = queryset.update(published=True)
        self.message_user(request, f'{updated} posts were published.')
    make_published.short_description = 'Publish selected posts'
    
    def make_unpublished(self, request, queryset):
        updated = queryset.update(published=False)
        self.message_user(request, f'{updated} posts were unpublished.')
    make_unpublished.short_description = 'Unpublish selected posts'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author', 'category')