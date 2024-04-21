from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuestHouseViewSet, AttractionViewSet

router = DefaultRouter()
router.register(r'guesthouses', GuestHouseViewSet)
router.register(r'attractions', AttractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
