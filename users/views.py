import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from users.models import Type
from users.serializers import TypeSerializer

@api_view(['GET'])
def test(request):
    if request.method == 'GET':
        data = {
            'user': str(request.user)
        }
        return Response(data, status=status.HTTP_200_OK)

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    def getTypes(self, request):
        types = Type.objects.all()
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data)