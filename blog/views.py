from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse
import json
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.core.exceptions import ValidationError
import logging

from blog.models import BlogPost, GalleryImage
from blog.forms import ArticleForm, GalleryImageFormSet

from slugify import slugify
import uuid

# Setup logging
logger = logging.getLogger(__name__)

def blog_summary(request):
    all_blogs = BlogPost.objects.filter(published=True).exclude(category__category__name="Kunstschule")
    context = {
        'all_blogs': all_blogs
        }
    return render(request, "blog/summary.html", context)

def youtube_id(url):
    o = urlparse(url)
    if o.netloc == 'youtu.be':
        return o.path[1:]
    elif o.netloc in ('www.youtube.com', 'youtube.com'):
        if o.path == '/watch':
            id_index = o.query.index('v=')
            return o.query[id_index+2:id_index+13]
        elif o.path[:7] == '/embed/':
            return o.path.split('/')[2]
        elif o.path[:3] == '/v/':
            return o.path.split('/')[2]
    return None  # fail?

def check_youtube_link(content):
    if content.find('>https://www.youtube'):
        first_position = content.find('>https://www.youtube') + 1
        last_postion = content.find('</a>', first_position)
        url = content[first_position:last_postion]
        return youtube_id(url)
    else:
        return False

@login_required(login_url='/team/login/')
def blog_thanks(request):
    return render(request, "blog/form_thanks.html")

@login_required(login_url='/team/login/')
def show_blogs_editing(request):
    all_blogs = BlogPost.objects.all().order_by("date").reverse()
    context = {
        'all_blogs': all_blogs
        }
    return render(request, "blog/edit/show_blog_editing.html", context)

def create_slug_text(title):
    """Safe slug creation with fallback"""
    try:
        if not title:
            return f"blog-post-{uuid.uuid4().hex[:8]}"
            
        title = title.lower()
        chars = {'ö':'oe','ä':'ae','ü':'ue', 'ß':'ss'}
        for char in chars:
            title = title.replace(char, chars[char])
        slug = slugify(title)
        if not slug:
            slug = f"blog-post-{uuid.uuid4().hex[:8]}"
        return slug
    except Exception as e:
        logger.error(f"Error creating slug from title '{title}': {e}")
        return f"blog-post-{uuid.uuid4().hex[:8]}"

@login_required(login_url='/team/login/')
def create_blog(request):
    if request.method == 'POST':
        logger.info(f"POST request received from user: {request.user}")
        logger.info(f"POST data keys: {list(request.POST.keys())}")
        logger.info(f"FILES data keys: {list(request.FILES.keys())}")
        
        # Auto-save request
        if request.POST.get('auto-save'):
            logger.info("Processing auto-save request")
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        blog_post = form.save(commit=False)
                        if not blog_post.slug:
                            blog_post.slug = create_slug_text(blog_post.title)
                        
                        # Ensure meta fields are filled
                        if not blog_post.meta_title:
                            blog_post.meta_title = blog_post.title[:60] if blog_post.title else "Blog Post"
                        if not blog_post.meta_description and blog_post.lead_paragraph:
                            blog_post.meta_description = blog_post.lead_paragraph[:160]
                        elif not blog_post.meta_description:
                            blog_post.meta_description = f"Blog post about {blog_post.title}"[:160] if blog_post.title else "Blog post"
                        
                        blog_post.save()
                        logger.info(f"Auto-save successful: {blog_post.id}")
                        return JsonResponse({'success': True, 'id': blog_post.id})
                except Exception as e:
                    logger.error(f"Auto-save error: {e}")
                    return JsonResponse({'success': False, 'error': str(e)})
            else:
                logger.warning(f"Auto-save form invalid: {form.errors}")
                return JsonResponse({'success': False, 'errors': form.errors})
        
        # Normal save
        logger.info("Processing normal save request")
        form = ArticleForm(request.POST, request.FILES)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES)
        
        logger.info(f"Form is valid: {form.is_valid()}")
        if not form.is_valid():
            logger.error(f"Form errors: {form.errors}")
        
        logger.info(f"Gallery formset is valid: {gallery_formset.is_valid()}")
        if not gallery_formset.is_valid():
            logger.error(f"Gallery formset errors: {gallery_formset.errors}")
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    blog_post = form.save(commit=False)
                    logger.info(f"Blog post created (not saved yet): {blog_post.title}")
                    
                    # Log image info
                    if blog_post.image:
                        logger.info(f"Image attached: {blog_post.image.name}")
                    else:
                        logger.info("No image attached")
                    
                    # Ensure slug exists
                    if not blog_post.slug:
                        blog_post.slug = create_slug_text(blog_post.title)
                    
                    # Ensure meta fields are filled
                    if not blog_post.meta_title:
                        blog_post.meta_title = blog_post.title[:60] if blog_post.title else "Blog Post"
                    if not blog_post.meta_description and blog_post.lead_paragraph:
                        blog_post.meta_description = blog_post.lead_paragraph[:160]
                    elif not blog_post.meta_description:
                        blog_post.meta_description = f"Blog post about {blog_post.title}"[:160] if blog_post.title else "Blog post"
                    
                    # Handle save & publish
                    if 'save-publish' in request.POST:
                        blog_post.published = True
                        logger.info("Set to published")
                    elif 'save-draft' in request.POST:
                        blog_post.published = False
                        logger.info("Set to draft")
                    
                    # Save main blog post
                    blog_post.save()
                    logger.info(f"Blog post saved successfully: {blog_post.id}")
                    
                    # Log final image info
                    if blog_post.image:
                        logger.info(f"Final image URL: {blog_post.image.url}")
                        logger.info(f"Final image path: {blog_post.image.path}")
                    
                    # Process gallery formset
                    if gallery_formset.is_valid():
                        gallery_formset.instance = blog_post
                        gallery_formset.save()
                        logger.info(f"Gallery images saved for blog post: {blog_post.title}")
                    else:
                        logger.warning(f"Gallery formset errors: {gallery_formset.errors}")
                
                messages.success(request, f"Blog post '{blog_post.title}' was created successfully!")
                logger.info("Redirecting to blog_thanks")
                return redirect('blog_thanks')
                
            except IntegrityError as e:
                logger.error(f"Database integrity error: {e}")
                if 'slug' in str(e):
                    form.add_error('slug', 'This URL slug is already in use. Please choose a different one.')
                else:
                    form.add_error(None, 'A database error occurred. Please try again.')
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                form.add_error(None, f'Validation error: {e}')
            except Exception as e:
                logger.error(f"Unexpected error creating blog post: {e}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                form.add_error(None, 'An unexpected error occurred. Please try again.')
        else:
            logger.warning(f"Form validation errors: {form.errors}")
            if gallery_formset.errors:
                logger.warning(f"Gallery formset errors: {gallery_formset.errors}")
    else:
        logger.info("GET request - showing empty form")
        form = ArticleForm()
        gallery_formset = GalleryImageFormSet()
    
    context = {
        'form': form,
        'gallery_formset': gallery_formset
    }
    logger.info("Rendering form template")
    return render(request, "blog/edit/form.html", context)

class BlogPostView(View):
    def get(self, request, *args, **kwargs):
        try:
            blog_post = get_object_or_404(BlogPost, slug=kwargs['slug'], date__year=kwargs['published_year'])
            
            # If not published and user is not authenticated, return 404
            if not blog_post.published and not request.user.is_authenticated:
                raise Http404("Blog post not found")
                
            # Prefetch gallery images to optimize queries
            blog_post.gallery_images.all()
                
            youtube = check_youtube_link(blog_post.content)
            if youtube:
                context = {'blog_post': blog_post, 'youtube': youtube}
            else:
                context = {'blog_post': blog_post}
            return render(request, 'blog/blog_post.html', context)
        except Exception as e:
            logger.error(f"Error displaying blog post: {e}")
            raise Http404("Blog post not found")

@login_required(login_url='/team/login/')
def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == "POST":
        # Auto-save request
        if request.POST.get('auto-save'):
            form = ArticleForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                try:
                    form.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    logger.error(f"Auto-save error for post {pk}: {e}")
                    return JsonResponse({'success': False, 'error': str(e)})
            return JsonResponse({'success': False, 'errors': form.errors})
        
        # Normal save
        form = ArticleForm(request.POST, request.FILES, instance=post)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES, instance=post)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    blog_post = form.save(commit=False)
                    
                    # Handle save & publish
                    if 'save-publish' in request.POST:
                        blog_post.published = True
                    elif 'save-draft' in request.POST:
                        blog_post.published = False
                        
                    blog_post.save()
                    
                    # Process gallery formset
                    if gallery_formset.is_valid():
                        gallery_formset.save()
                        
                messages.success(request, f"Blog post '{blog_post.title}' was updated successfully!")
                return redirect('show_blogs_editing')
                
            except Exception as e:
                logger.error(f"Error updating blog post {pk}: {e}")
                form.add_error(None, 'An error occurred while saving. Please try again.')
        else:
            logger.warning(f"Form validation errors for post {pk}: {form.errors}")
    else:
        form = ArticleForm(instance=post)
        gallery_formset = GalleryImageFormSet(instance=post)
        
    return render(request, 'blog/edit/form.html', {
        'form': form,
        'gallery_formset': gallery_formset
    })

@login_required(login_url='/team/login/')
def delete_blog_post(request, pk):
    try:
        post = get_object_or_404(BlogPost, pk=pk)
        title = post.title
        post.delete()
        messages.success(request, f"Blog post '{title}' was deleted successfully!")
        logger.info(f"Blog post deleted: {title}")
    except Exception as e:
        logger.error(f"Error deleting blog post {pk}: {e}")
        messages.error(request, "An error occurred while deleting the blog post.")
    
    return redirect('show_blogs_editing')
