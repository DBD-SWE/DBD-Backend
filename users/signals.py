from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

@receiver(post_migrate)
def populate_permissions(sender, **kwargs):
    # Call the management command to populate permissions
    call_command('populate_permissions')
