from rest_framework import serializers
from .models import GuestHouse

'''
class GuestHouse(models.Model):
    name = models.CharField(max_length=255)
    location_address = models.CharField(max_length=255)
    location_coordinates_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_coordinates_long = models.DecimalField(max_digits=9, decimal_places=6)
    category = models.CharField(max_length=100)
    description = models.TextField()
    number_of_bathrooms = models.IntegerField(default=1)
    number_of_bedrooms = models.IntegerField(default=1) 
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    accessibility = models.BooleanField(default=False)
    food_type = models.CharField(max_length=2, choices=FoodType.choices)
    images = models.URLField(max_length=2000, blank=True, null=True) 
'''

class GuestHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestHouse
        fields = '__all__'