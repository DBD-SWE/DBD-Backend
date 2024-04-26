from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from activitylog.mixins import ActivityLogMixin
from authentication.models import User
from .models import GuestHouse, Attraction, Commodity, District
from .serializers import GuestHouseSerializer, AttractionSerializer, CommoditiesSerializer, DistrictSerializer

class DistrictViewSet(ActivityLogMixin, viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class CommodityViewSet(ActivityLogMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditiesSerializer

class GuestHouseViewSet(ActivityLogMixin, viewsets.ModelViewSet):
    queryset = GuestHouse.objects.all()
    serializer_class = GuestHouseSerializer 
    
class AttractionViewSet(ActivityLogMixin, viewsets.ModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
    
class DashboardData(ActivityLogMixin, viewsets.ViewSet):
    def list(self, request):
        data = {
            'districts_count': District.objects.count(),
            'commodities_count': Commodity.objects.count(),
            'users_count': User.objects.count(),
            'attractions_count': Attraction.objects.count(),
            'guest_houses_count': GuestHouse.objects.count(),
            'districts_data': [],
            'commodities': CommoditiesSerializer(Commodity.objects.all(), many=True).data
        }
        for district in District.objects.all():
            commodity_count = Commodity.objects.filter(district=district).count()
            data['districts_data'].append({
                'district': district.name,
                'commodities_count': commodity_count
            })
        return Response(data, status=status.HTTP_200_OK)
