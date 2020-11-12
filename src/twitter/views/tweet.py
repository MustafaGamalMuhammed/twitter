from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from twitter.models import Profile


@api_view(['POST'])
def post_tweet(request):
    print(request.data)

    return Response(data={}, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_handlers(request, query):
    queryset = Profile.objects.filter(handler__icontains=query)
    data = queryset.values_list('handler')

    return Response(data, status=status.HTTP_200_OK)