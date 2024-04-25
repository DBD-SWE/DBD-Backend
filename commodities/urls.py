from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuestHouseViewSet, AttractionViewSet, CommodityViewSet, DistrictViewSet, DashboardData

router = DefaultRouter()
router.register(r'guesthouses', GuestHouseViewSet)
router.register(r'attractions', AttractionViewSet)
router.register(r'commodities', CommodityViewSet)
router.register(r'districts', DistrictViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardData.as_view({'get': 'list'}), name='dashboard'),
]
