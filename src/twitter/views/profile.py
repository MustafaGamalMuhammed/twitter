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


def get_search_data(profiles):
    data = []

    for profile in profiles:
        d = {}
        d['id'] = profile.id
        d['url'] = profile.get_absolute_url()
        d['user_username'] = profile.user.username
        d['handler'] = profile.handler
        data.append(d)

    return data

@login_required
@api_view(['GET'])
def search(request, query):
    q1 = Profile.objects.filter(user__username__icontains=query)
    q2 = Profile.objects.filter(handler__icontains=query)
    q = q1.union(q2)

    data = get_search_data(q)

    return Response(data, status=status.HTTP_200_OK)
