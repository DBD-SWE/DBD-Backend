from rest_framework import serializers
from .models import Permission, Type
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('name', 'identifier')

    def create(self, validated_data):
        return Permission.objects.create(**validated_data)

class TypeSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)
    class Meta:
        model = Type
        fields = ('id', 'name', 'permissions')
    
    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions', [])
        type_instance = Type.objects.create(**validated_data)
        type_instance.permissions.set(permissions_data)  # Assign permissions
        return type_instance
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.permissions = validated_data.get('permissions', instance.permissions)
    #     instance.save()
    #     return instance
    
    # def delete(self, instance):
    #     instance.delete()