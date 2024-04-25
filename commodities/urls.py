from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuestHouseViewSet, AttractionViewSet, CommodityViewSet

router = DefaultRouter()
router.register(r'guesthouses', GuestHouseViewSet)
router.register(r'attractions', AttractionViewSet)
router.register(r'commodities', CommodityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
