from django.contrib import admin
from django.utils.html import format_html
from blog.models import Author, BlogPost

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
    list_display = ('title', 'author', 'category', 'date', 'published', 'updated_at')
    list_filter = ('published', 'category', 'author', 'date')
    search_fields = ('title', 'lead_paragraph', 'content', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date',)
    
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