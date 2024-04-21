from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuestHouseViewSet

router = DefaultRouter()
router.register(r'guesthouses', GuestHouseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
