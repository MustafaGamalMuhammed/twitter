from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def post_tweet(request):
    print(request.data)

    return Response(data={}, status=status.HTTP_200_OK)