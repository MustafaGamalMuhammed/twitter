from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from twitter.models import Profile, Tweet
import re


def get_all_profiles_mentioned_in_tweet(content:str):
    mentions = re.findall(r'@(\w+)', content)
    if mentions:
        profiles = Profile.objects.filter(handler__in=mentions)
    else:
        profiles = []
    return profiles


@login_required
@api_view(['POST'])
def post_tweet(request):
    author = request.data.get('author')
    content = request.data.get('content')
    mentions = get_all_profiles_mentioned_in_tweet(content)

    tweet = Tweet(author_id=author, content=content)
    tweet.save()
    tweet.mentions.set(mentions)

    return Response(data={}, status=status.HTTP_201_CREATED)


@login_required
@api_view(['GET'])
def search_handlers(request, query):
    queryset = Profile.objects.filter(handler__icontains=query)
    data = queryset.values_list('handler', flat=True)

    return Response(data, status=status.HTTP_200_OK)


def get_data_from_tweets(tweets):
    data = []
    
    for tweet in tweets:
        d = {}
        d['id'] = tweet.id
        d['content'] = tweet.content
        d['author'] = tweet.author.id
        data.append(d)
    
    return data


@login_required
@api_view(['GET'])
def get_tweets(request):
    tweets = request.user.profile.mentions.all()
    data = get_data_from_tweets(tweets)

    return Response(data, status=status.HTTP_200_OK)
    