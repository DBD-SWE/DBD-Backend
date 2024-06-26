import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from rest_framework.exceptions import ValidationError

from .models import ActivityLog, READ, CREATE, UPDATE, DELETE, SUCCESS, FAILED
from .helpers import get_client_ip

class ActivityLogMixin:
    log_message = None
    
    def _get_action_type(self, request):
        return self.action_type_mapper().get(f'{request.method.upper()}')
    def _build_log_message(self, request):
        return f"User: {self._get_user(request)} -- Action Type: {self._get_action_type(request)} -- Path: {request.path} -- Path Name: {request.resolver_match.url_name}"
    def get_log_message(self,request):
        return self.log_message or self._build_log_message(request)

    @staticmethod
    def action_type_mapper():
        return {
            'GET': READ,
            'POST': CREATE,
            'PUT': UPDATE,
            'DELETE': DELETE
        }
    @staticmethod
    def _get_user(request):
        return request.user if request.user.is_authenticated else None

    def _write_log(self, request, response):
        status = SUCCESS if response.status_code < 400 else FAILED
        actor = self._get_user(request)
        if actor and not getattr(settings, 'TESTING', False):
            logging.info("Started loging entry...")
            data = {
                'actor': actor,
                'actor_ip': get_client_ip(request),
                'action_type': self._get_action_type(request),
                'status': status,
                'remarks': self.get_log_message(request),

            }
            try:
                data['content_type'] = ContentType.objects.get_for_model(self.get_queryset().model)
              
            except (AttributeError, ValidationError):
                data['content_type'] = None
            except AssertionError:
                pass
            try:
              
               data["content_object"] = self.get_object()
              
            except Exception:
                data['content_object'] = None
            except AssertionError:
                pass
            

            ActivityLog.objects.create(**data)

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        self._write_log(request, response)
        return response
