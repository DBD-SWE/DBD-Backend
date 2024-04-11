from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

# test route that return test json
def test(request):
    return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)
