from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from activitylog.mixins import ActivityLogMixin
from authentication.models import User
from .models import GuestHouse, Attraction, Commodity, District
from .serializers import GuestHouseSerializer, AttractionSerializer, CommoditiesSerializer, DistrictSerializer
from activitylog.models import ActivityLog
from activitylog.serializers import ActivityLogSerializer
from django.db.models import Count

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
            'districts_data': 
                District.objects.annotate(
                    commodities_count = Count('commodity')
                ).values('name', 'commodities_count'),
            'commodities': 
                CommoditiesSerializer(
                    Commodity.objects.all(), many=True
                ).data,
            'recent_activities': 
                ActivityLogSerializer(
                    ActivityLog.objects.all().order_by('-action_time')[:5], many=True
                ).data
        }
        return Response(data, status=status.HTTP_200_OK)
