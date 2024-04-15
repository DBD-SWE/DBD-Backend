from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import TypeViewSet, test

router = DefaultRouter()
router.register(r'types', TypeViewSet)

urlpatterns = [
    path('test/', test)
]