from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


User = get_user_model()

CREATE, READ, UPDATE, DELETE =  'Create', 'Read', 'Update', 'Delete'
LOGIN, LOGOUT, LOGIN_FAILED = 'Login', 'Logout', 'Login Failed'
ACTION_TYPES =[
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]

SUCCESS, FAILED = 'Success', 'Failed'
ACTION_STATUS = [
    (SUCCESS, SUCCESS),
    (FAILED, FAILED),
]

class ActivityLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    actor_ip = models.GenericIPAddressField(null=True, blank=True)
    action_type = models.CharField(max_length=15, choices=ACTION_TYPES)
    action_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=ACTION_STATUS, default=SUCCESS)
    

    # for generic relations
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    def __str__(self):
        return f"{self.action_type} by {self.actor} on {self.action_time}"