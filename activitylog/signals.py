from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver

from .models import ActivityLog,  LOGIN, LOGIN_FAILED, FAILED
from .helpers import get_client_ip


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    print("HERE")
    message = f"{user} is logged in with ip:{get_client_ip(request)}"
    ActivityLog.objects.create(actor=user, action_type=LOGIN, remarks=message, actor_ip=get_client_ip(request))


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    message = f"Login Attempt Failed for email {credentials.get('email')} with ip: {get_client_ip(request)}"
    ActivityLog.objects.create(action_type=LOGIN_FAILED, remarks=message, actor_ip=get_client_ip(request)
                               , status=FAILED
                               )