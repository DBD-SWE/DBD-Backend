from rest_framework import serializers

from images.models import Image
from .models import GuestHouse, Attraction, Commodity, District 
from django.db import transaction

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class CommoditiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['district']
        return data

class GuestHouseSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=Image.objects.all())
    class Meta:
        model = GuestHouse
        fields = (
            "id", "name", "description", 
            "district", "location_coordinates_lat", "location_coordinates_long", 
            "category", "number_of_bathrooms", "number_of_bedrooms", 
            "rating", "accessibility", "food_type", "images"
        )  
    
    def create(self, validated_data):
        with transaction.atomic():  
            validated_data['type'] = "GuestHouse"
            images_data = validated_data.pop('images')
            guesthouse = GuestHouse.objects.create(**validated_data)
            guesthouse.images.set(images_data)
            return guesthouse

    def update(self, instance, validated_data):
        validated_data['type'] = "GuestHouse"
        validated_data['images'] = validated_data.pop('images')
        update = super().update(instance, validated_data)
        update.images.set(validated_data['images'])
        return update
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['district'] = DistrictSerializer(instance.district).data
        data['images'] = [image.image.url for image in instance.images.all()]
        return data
            
class AttractionSerializer(serializers.ModelSerializer):
    type = "Attraction"
    class Meta:
        model = Attraction
        fields = (
            "id", "name", "description", 
            "district", "location_coordinates_lat", "location_coordinates_long",
            "images"
        )
    
    def create(self, validated_data):
        validated_data['type'] = "Attraction"
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['type'] = "Attraction"
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['district'] = DistrictSerializer(instance.district).data
        return data