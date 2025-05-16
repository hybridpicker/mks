from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse
import json
from django.db import transaction

from blog.models import BlogPost, GalleryImage
from blog.forms import ArticleForm, GalleryImageFormSet

from slugify import slugify

# Create your views here.

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
    # Remove space and make every character low #
    title =  title.lower()
    # Checking for special characters and transform #
    chars = {'ö':'oe','ä':'ae','ü':'ue', 'ß':'ss',}
    for char in chars:
        title = title.replace(char,chars[char])
    # Check for other special characters #
    title = slugify(title)
    return title

@login_required(login_url='/team/login/')
def create_blog(request):
    form = ArticleForm(request.POST)
    gallery_formset = GalleryImageFormSet()
    
    if request.method == 'POST':
        # Auto-save request
        if request.POST.get('auto-save'):
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                blog_post = form.save(commit=False)
                if not blog_post.slug:
                    blog_post.slug = create_slug_text(blog_post.title)
                blog_post.save()
                return JsonResponse({'success': True, 'id': blog_post.id})
            return JsonResponse({'success': False, 'errors': form.errors})
        
        # Normal save
        form = ArticleForm(request.POST, request.FILES)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES)
        
        if form.is_valid():
            with transaction.atomic():
                blog_post = form.save(commit=False)
                if not blog_post.slug:
                    blog_post.slug = create_slug_text(blog_post.title)
                
                # Handle save & publish
                if 'save-publish' in request.POST:
                    blog_post.published = True
                elif 'save-draft' in request.POST:
                    blog_post.published = False
                    
                blog_post.save()
                
                # Process gallery formset
                if gallery_formset.is_valid():
                    gallery_formset.instance = blog_post
                    gallery_formset.save()
                
            return redirect('blog_thanks')
    else:
        form = ArticleForm()
        gallery_formset = GalleryImageFormSet()
    
    context = {
        'form': form,
        'gallery_formset': gallery_formset
    }
    return render(request, "blog/edit/form.html", context)

class BlogPostView(View):
    def get(self, request, *args, **kwargs):
        blog_post = get_object_or_404(BlogPost, slug=kwargs['slug'], date__year=kwargs['published_year'])
        # If not published and user is not authenticated, return 404
        if not blog_post.published and not request.user.is_authenticated:
            raise Http404("Blog post not found")
            
        # Prefetch gallery images to optimize queries
        blog_post.gallery_images.all()
            
        youtube = check_youtube_link(blog_post.content)
        if youtube:
            context = {'blog_post': blog_post, 'youtube':youtube}
        else:
            context = {'blog_post': blog_post}
        return render(request, 'blog/blog_post.html', context)

@login_required(login_url='/team/login/')
def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == "POST":
        # Auto-save request
        if request.POST.get('auto-save'):
            form = ArticleForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors})
        
        # Normal save
        form = ArticleForm(request.POST, request.FILES, instance=post)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES, instance=post)
        
        if form.is_valid():
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
                
            return redirect('show_blogs_editing')
    else:
        form = ArticleForm(instance=post)
        gallery_formset = GalleryImageFormSet(instance=post)
        
    return render(request, 'blog/edit/form.html', {
        'form': form,
        'gallery_formset': gallery_formset
    })

@login_required(login_url='/team/login/')
def delete_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('show_blogs_editing')