from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from authentication.models import User
from .models import GuestHouse, Attraction, Commodity, District
from .serializers import GuestHouseSerializer, AttractionSerializer, CommoditiesSerializer, DistrictSerializer

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class CommodityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditiesSerializer
    
    def commoditiesPerEachDistrict(self, request):
        data = []
        for district in District.objects.all():
            commodities = Commodity.objects.filter(district=district)
            data.append({
                'district': district.name,
                'commodities': CommoditiesSerializer(commodities, many=True).data
            })
        return Response(data, status=status.HTTP_200_OK)
    
    def commoditiesPerDistrict(self, request, pk=None):
        district = District.objects.get(pk=pk)
        commodities = Commodity.objects.filter(district=district)
        data = {
            'district': district.name,
            'commodities': CommoditiesSerializer(commodities, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)

class GuestHouseViewSet(viewsets.ModelViewSet):
    queryset = GuestHouse.objects.all()
    serializer_class = GuestHouseSerializer 
    
class AttractionViewSet(viewsets.ModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
    
class DashboardData(viewsets.ViewSet):
    def list(self, request):
        data = {
            'districts_count': District.objects.count(),
            'commodities_count': Commodity.objects.count(),
            'users_count': User.objects.count(),
            'attractions_count': Attraction.objects.count(),
            'guest_houses_count': GuestHouse.objects.count(),
        }
        return Response(data, status=status.HTTP_200_OK)
