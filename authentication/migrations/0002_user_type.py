# Generated by Django 5.0.3 on 2024-04-11 18:32

import django.db.models.deletion
import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('users', '0003_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.ForeignKey(default=users.models.Type.get_default_pk, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='users.type'),
        ),
    ]
