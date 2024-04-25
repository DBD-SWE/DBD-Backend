from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import GuestHouse, Attraction, Commodity, District
from .serializers import GuestHouseSerializer, AttractionSerializer, CommoditiesSerializer, DistrictSerializer

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class CommodityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditiesSerializer

class GuestHouseViewSet(viewsets.ModelViewSet):
    queryset = GuestHouse.objects.all()
    serializer_class = GuestHouseSerializer 
    
class AttractionViewSet(viewsets.ModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
