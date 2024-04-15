from rest_framework import serializers
from .models import Type

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('name', 'permissions')
        
    def create(self, validated_data):
        return Type.objects.create(**validated_data)
