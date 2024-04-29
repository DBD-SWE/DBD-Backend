# Generated by Django 4.2.10 on 2024-04-29 15:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('commodities', '0002_alter_district_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attraction',
            name='images',
        ),
        migrations.RemoveField(
            model_name='guesthouse',
            name='images',
        ),
        migrations.AddField(
            model_name='attraction',
            name='custom_attribute',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
