# urls.py
from django.urls import path, include
from .views import ActivityLogViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ActivityLogViewSet, basename='activitylog')

urlpatterns = [
path('', include(router.urls)),
] 
