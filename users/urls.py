from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import TypeViewSet, UserViewSet, test, PermissionViewSet, AssignUserType

router = DefaultRouter()
router.register(r'types', TypeViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('test/', test),
    path('', include(router.urls)),
    path('types/assign-user-type/<int:user_id>/', AssignUserType.as_view())


]