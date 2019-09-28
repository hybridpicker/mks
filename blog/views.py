from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from blog.models import BlogPost

# Create your views here.

def blog_summary(request):
    all_blogs = BlogPost.objects.all()
    context = {
        'all_blogs': all_blogs
        }
    return render(request, "blog/summary.html", context)


class BlogPostView(View):
    def get(self, request, *args, **kwargs):
        blog_post = get_object_or_404(BlogPost, slug=kwargs['slug'])
        context = {'blog_post': blog_post}
        return render(request, 'blog/blog_post.html', context)
