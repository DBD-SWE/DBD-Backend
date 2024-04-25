from rest_framework import serializers
from .models import GuestHouse, Attraction, Commodity

class CommoditiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'

class GuestHouseSerializer(serializers.ModelSerializer):
    commodity = CommoditiesSerializer(many=True)
    class Meta:
        model = GuestHouse
        fields = ('__all__')  
            
class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = '__all__'