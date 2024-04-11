from django.db import migrations

def create_default_role(apps, schema_editor):
    Role = apps.get_model('users', 'type')
    Role.objects.create(name='user')

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_type_permissions_delete_typepermission'),
    ]

    operations = [
        migrations.RunPython(create_default_role),
    ]
