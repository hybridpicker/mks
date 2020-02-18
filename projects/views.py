from django.views.generic import View
from django.shortcuts import render
from projects.models import Project
from django.shortcuts import get_object_or_404

# Create your views here.

def project_view(request):
    project = Project.objects.all()
    context = {
        'project': project
    }
    return render(request, 'projects/project.html', context)

class ProjectView(View):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        context = {'project': project}
        return render(request, 'projects/project.html', context)
