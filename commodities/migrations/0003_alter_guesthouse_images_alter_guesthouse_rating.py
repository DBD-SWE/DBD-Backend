# Generated by Django 4.2.10 on 2024-04-21 17:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commodities', '0002_attraction_guesthouse_remove_restaurant_commodity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guesthouse',
            name='images',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='guesthouse',
            name='rating',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
