from rest_framework import serializers
from .models import Permission, Type

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('name', 'permissions')
        
    def create(self, validated_data):
        return Type.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.permissions = validated_data.get('permissions', instance.permissions)
    #     instance.save()
    #     return instance
    
    # def delete(self, instance):
    #     instance.delete()
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('name', 'identifier')

    def create(self, validated_data):
        return Permission.objects.create(**validated_data)
