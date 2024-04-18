from rest_framework import serializers
from .models import Permission, Type
from django.db import transaction
import logging
logger = logging.getLogger(__name__)
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('name', 'identifier')

    def create(self, validated_data):
        return Permission.objects.create(**validated_data)

class PermissionIDOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id']  

class TypeSerializer(serializers.ModelSerializer):
    permissions = PermissionIDOnlySerializer(many=True)

    class Meta:
        model = Type
        fields = ('id', 'name', 'permissions')

    def create(self, validated_data):
        logger.debug("Received validated data for type creation: %s", validated_data)
        try:
            permissions_data = validated_data.pop('permissions', [])
            with transaction.atomic():
                type_instance = Type.objects.create(**validated_data)
                permission_ids = [perm['id'] for perm in permissions_data]
                permissions = Permission.objects.filter(id__in=permission_ids)
                if len(permissions) != len(permission_ids):
                    raise serializers.ValidationError("One or more permissions not found.")
                type_instance.permissions.set(permissions)
                return type_instance
        except Exception as e:
            logger.error("Error creating type: %s", str(e))
            raise serializers.ValidationError(str(e))
    def validate(self, data):
        # Additional custom validation logic if needed
        return data

    