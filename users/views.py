import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def test(request):
    if request.method == 'GET':
        data = {
            'user': str(request.user)
        }
        return Response(data, status=status.HTTP_200_OK)