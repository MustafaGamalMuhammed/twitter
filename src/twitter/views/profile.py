from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from twitter.models import Profile


@login_required
def profile_view(request, id=None):
    context = {}
    
    if id and id != request.user.profile.id:
        context['other_profile'] = True
        context['profile'] = get_object_or_404(Profile, id=id)
    else:
        context['other_profile'] = False


    return render(request, 'twitter/profile.html', context=context)


@login_required
@api_view(['POST'])
def follow_view(request):
    profile = get_object_or_404(Profile, id=request.data.get('id'))

    request.user.profile.follow(profile)

    return Response(data={}, status=status.HTTP_200_OK)