from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from blog.models import BlogPost
from blog.forms import ArticleForm

from slugify import slugify

# Create your views here.

def blog_summary(request):
    all_blogs = BlogPost.objects.all()
    context = {
        'all_blogs': all_blogs
        }
    return render(request, "blog/summary.html", context)

@login_required(login_url='/team/login/')
def blog_thanks(request):
    return render(request, "blog/form_thanks.html")

@login_required(login_url='/team/login/')
def show_blogs_editing(request):
    all_blogs = BlogPost.objects.all()
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
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ArticleForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            title = form.cleaned_data['title']
            lead_paragraph = form.cleaned_data['lead_paragraph']
            content = form.cleaned_data['content']
            title = request.POST['title']
            lead_paragraph = request.POST['lead_paragraph']
            image = request.FILES['image']
            content = request.POST['content']
            #create slug from title-input
            slug = create_slug_text(title)
            new_article = BlogPost(title=title,
                                   lead_paragraph=lead_paragraph,
                                   image=image,
                                   slug=slug,
                                   meta_title=title,
                                   meta_description=lead_paragraph,
                                   content=content)
            new_article.save()
            # redirect to a blog_post_url:
            return redirect('blog_thanks')
            # if a GET (or any other method) we'll create a blank form
        else:
            form = ArticleForm()
    context = {
        'form': form
        }
    return render(request, "blog/edit/form.html", context)

class BlogPostView(View):
    def get(self, request, *args, **kwargs):
        blog_post = get_object_or_404(BlogPost, slug=kwargs['slug'], published_year=kwargs['published_year'])
        context = {'blog_post': blog_post}
        return render(request, 'blog/blog_post.html', context)

class BlogPostEditView(View):
    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(BlogPost, id=kwargs['id'])
        if request.method == "POST":
            form = ArticleForm(request.POST, instance=blog)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.save()
                return redirect('post_detail', pk=blog.pk)
        else:
            form = ArticleForm(instance=blog)
        return render(request, 'blog/edit/form.html', {'form': form})
