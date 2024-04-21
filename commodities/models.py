# Commodities App Models
# This app will handle everything related to commodities and commodity types.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CommodityType(models.Model):
    type_name = models.CharField(max_length=255)

class Commodity(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.ForeignKey(CommodityType, on_delete=models.CASCADE)   

class FoodType(models.TextChoices):
    VEGAN = 'V', 'Vegan'
    VEGETARIAN = 'VE', 'Vegetarian'
    MEAT = 'M', 'Meat'

class GuestHouse(models.Model):
    name = models.CharField(max_length=255)
    location_address = models.CharField(max_length=255)
    location_coordinates_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_coordinates_long = models.DecimalField(max_digits=9, decimal_places=6)
    category = models.CharField(max_length=100)
    description = models.TextField()
    number_of_bathrooms = models.IntegerField(default=1)
    number_of_bedrooms = models.IntegerField(default=1)
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    accessibility = models.BooleanField(default=False)
    food_type = models.CharField(max_length=2, choices=FoodType.choices)
    images = models.ImageField(upload_to='guesthouses_images/', blank=True, null=True)

class Attraction(models.Model):
    name = models.CharField(max_length=255)
    location_address = models.CharField(max_length=255)
    location_coordinates_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_coordinates_long = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField()
    images = models.ImageField(upload_to='attractions_images/', blank=True, null=True)
