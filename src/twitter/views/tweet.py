from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from twitter.models import Profile, Tweet, Hashtag
from twitter.forms import TweetForm
import re


def get_all_profiles_mentioned_in_tweet(content:str):
    mentions = re.findall(r'@(\w+)', content)
    
    if mentions:
        profiles = Profile.objects.filter(handler__in=mentions)
    else:
        profiles = []
    
    return profiles


def get_all_hashtags_in_tweet(content:str):
    hashtags = re.findall(r'#(\w+)', content)
    results = []

    if hashtags:
        for hashtag in hashtags:
            h, _ = Hashtag.objects.get_or_create(name=hashtag)
            results.append(h)
    else:
        results = []

    return results


@login_required
@api_view(['POST'])
def post_tweet(request):
    form = TweetForm(request.data)
    if form.is_valid():
        tweet = form.save()
        mentions = get_all_profiles_mentioned_in_tweet(request.data.get('content'))
        hashtags = get_all_hashtags_in_tweet(request.data.get('content'))
        tweet.mentions.set(mentions)
        tweet.hashtags.set(hashtags)

    return Response(data={}, status=status.HTTP_201_CREATED)


@login_required
@api_view(['GET'])
def search_handlers(request, query):
    queryset = Profile.objects.filter(handler__icontains=query)
    data = queryset.values_list('handler', flat=True)

    return Response(data, status=status.HTTP_200_OK)


@login_required
@api_view(['GET'])
def search_hashtags(request, query):
    queryset = Hashtag.objects.filter(name__icontains=query)
    data = queryset.values_list('name', flat=True)

    return Response(data, status=status.HTTP_200_OK)


def get_tweet_content_with_links(content:str):
    content = content.split()
    
    for i in range(len(content)):
        word = content[i]
        
        if word.startswith('@'):
            profile = get_all_profiles_mentioned_in_tweet(word)
            if profile:
                content[i] = f"<a href='/profile/{profile[0].id}/'>@{profile[0].handler}</a>"
        
        if word.startswith('#'):
            hashtag = get_all_hashtags_in_tweet(word)
            if hashtag:
                content[i] = f"<a href='#'>#{hashtag[0].name}</a>"

    return ' '.join(content)
    

def get_data_from_tweets(request, tweets):
    data = []
    
    for tweet in tweets:
        d = {}
        d['id'] = tweet.id
        d['content'] = get_tweet_content_with_links(tweet.content)
        d['author_id'] = tweet.author.id
        d['author_handler'] = tweet.author.handler
        d['author_user_username'] = tweet.author.user.username
        d['author_image'] = tweet.author.image.url
        d['author_url'] = reverse('profile', args=(tweet.author.id,))
        d['retweeters_count'] = tweet.retweeters.count()
        d['likers_count'] = tweet.likers.count()
        d['is_liked'] = request.user.profile in tweet.likers.all()
        d['is_retweeted'] = request.user.profile in tweet.retweeters.all()
        data.append(d)
    
    return data


@login_required
@api_view(['GET'])
def get_home_tweets(request):
    profile = request.user.profile
    tweets = profile.mentions.all()
    following_tweets = profile.get_following_tweets()
    
    if following_tweets:
        tweets = (tweets | following_tweets).order_by('-created_at')

    data = get_data_from_tweets(request, tweets)

    return Response(data, status=status.HTTP_200_OK)


@login_required
@api_view(['GET'])
def get_my_tweets(request):
    tweets = request.user.profile.tweets.all()    
    retweets = request.user.profile.retweets.all()
    tweets = tweets.union(retweets).order_by('-created_at')

    data = get_data_from_tweets(request, tweets)

    return Response(data, status=status.HTTP_200_OK)


@login_required
@api_view(['GET'])
def get_profile_tweets(request, id):
    try:
        profile = Profile.objects.get(id=id)
        tweets = profile.tweets.all()
        retweets = profile.retweets.all()
        tweets = tweets.union(retweets).order_by('-created_at')
        
        data = get_data_from_tweets(request, tweets)
        
        return Response(data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def retweet(request):
    try:
        tweet = Tweet.objects.get(id=request.data.get('id'))
        tweet.retweeters.add(request.user.profile)
        return Response({}, status=status.HTTP_201_CREATED)
    except Tweet.DoesNotExist:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def like(request):
    try:
        tweet = Tweet.objects.get(id=request.data.get('id'))
        tweet.likers.add(request.user.profile)
        return Response({}, status=status.HTTP_201_CREATED)
    except Tweet.DoesNotExist:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
