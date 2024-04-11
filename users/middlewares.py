from django.http import JsonResponse, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
map_request_method = {
    'GET': 'R',
    'POST': 'C',
    'PUT': 'U',
    'DELETE': 'D'
}


class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
      
        if request.path.startswith('/auth') or request.path.startswith('/admin'):
            return None
        request.user = JWTAuthentication().authenticate(request)[0]
        
        # Check if the user is authenticated
        if not request.user:
            return JsonResponse({"message": "You are not authenticated."}, status=401)

        # Access user type and check permissions
        user_type = getattr(request.user, 'type', None)
        if user_type and user_type.permissions.filter(
            name=request.path, 
            identifier=map_request_method[request.method]
        ).exists():
            return None
        else:
            return JsonResponse({"message": "You are forbidden to view this route."}, status=401)

