from django.shortcuts import render, get_object_or_404
from twitter.models import Profile


def profile_view(request, id=None):
    context = {}
    
    if id:
        context['other_profile'] = True
        context['profile'] = get_object_or_404(Profile, id=id)


    return render(request, 'twitter/profile.html', context=context)