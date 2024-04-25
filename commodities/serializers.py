from rest_framework import serializers
from .models import GuestHouse, Attraction, Commodity, District 

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class CommoditiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'

class GuestHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestHouse
        fields = (
            "id", "name", "description", 
            "district_id", "location_coordinates_lat", "location_coordinates_long", 
            "category", "number_of_bathrooms", "number_of_bedrooms", 
            "rating", "accessibility", "food_type", "images"
        )  

    def create(self, validated_data):
        validated_data['type'] = "GuestHouse"
        return super().create(validated_data)
            
class AttractionSerializer(serializers.ModelSerializer):
    type = "Attraction"
    class Meta:
        model = Attraction
        fields = (
            "id", "name", "description", 
            "district_id", "location_coordinates_lat", "location_coordinates_long",
            "images"
        )
    
    def create(self, validated_data):
        validated_data['type'] = "Attraction"
        return super().create(validated_data)