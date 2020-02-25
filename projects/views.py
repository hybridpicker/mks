from django.views.generic import View
from django.shortcuts import render
from projects.models import Project
from django.shortcuts import get_object_or_404
from events.models import Event
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
        try:
            events = Event.objects.filter(project=project)
            context = {
                'project': project,
                'events': events}
        except Event.DoesNotExist:
            context = {
                'project': project
                }
        return render(request, 'projects/project.html', context)
