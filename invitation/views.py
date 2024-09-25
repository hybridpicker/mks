from django.shortcuts import render, redirect
from .forms import InvitationForm
from django.contrib.auth.decorators import login_required
from .models import Invitation


def invitation_view(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invitation:thank_you')
    else:
        form = InvitationForm()
    context = {
        'form': form,
    }
    return render(request, 'invitation/invitation_form.html', context)

def thank_you_view(request):
    return render(request, 'invitation/thank_you.html')

@login_required(login_url='/team/login/')
def invitation_list_view(request):
    invitations = Invitation.objects.all()
    total_count = invitations.count()
    context = {
        'invitations': invitations,
        'total_count': total_count,
    }
    return render(request, 'invitation/invitation_list.html', context)

