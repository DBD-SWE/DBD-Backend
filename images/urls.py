from django.urls import path
from django.conf.urls.static import static

from BackendDBD import settings

from .views import upload_image

urlpatterns = [
    path('upload/', upload_image, name='upload_image')
] 
