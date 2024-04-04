# Commodities App Models
# This app will handle everything related to commodities and commodity types.

from django.db import models

class CommodityType(models.Model):
    type_name = models.CharField(max_length=255)

class Commodity(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.ForeignKey(CommodityType, on_delete=models.CASCADE)   

class Hotel(models.Model):
    commodity = models.OneToOneField(Commodity, on_delete=models.CASCADE)
    hotel_specific_attribute = models.CharField(max_length=255)

class Restaurant(models.Model):
    commodity = models.OneToOneField(Commodity, on_delete=models.CASCADE)
    restaurant_specific_attribute = models.CharField(max_length=255)
