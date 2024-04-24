from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import GuestHouse, Attraction
from .serializers import GuestHouseSerializer, AttractionSerializer

class GuestHouseViewSet(viewsets.ModelViewSet):
    queryset = GuestHouse.objects.all()
    serializer_class = GuestHouseSerializer
    
class AttractionViewSet(viewsets.ModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
