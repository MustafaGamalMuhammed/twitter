from django.contrib.auth.decorators import login_required
from twitter.models import Hashtag
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def get_data_from_hashtags(hashtags):
    data = []

    for hashtag in hashtags:
        d = {}
        d['id'] = hashtag.id
        d['name'] = hashtag.name
        d['usage_count'] = hashtag.usage_count
        data.append(d)

    return data

@api_view(['GET'])
def get_most_used_hashtags(request):
    query = Hashtag.objects.order_by('-usage_count')[:5]

    data = get_data_from_hashtags(query)

    return Response(data, status=status.HTTP_200_OK)