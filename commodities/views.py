from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import GuestHouse
from .serializers import GuestHouseSerializer

class GuestHouseViewSet(viewsets.ModelViewSet):
    queryset = GuestHouse.objects.all()
    serializer_class = GuestHouseSerializer
