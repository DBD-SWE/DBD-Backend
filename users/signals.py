# users/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

@receiver(post_migrate)
def populate_permissions(sender, **kwargs):
    from django.apps import apps
    app_config = apps.get_app_config('users')
    if sender == app_config:
        call_command('populate_permissions')
