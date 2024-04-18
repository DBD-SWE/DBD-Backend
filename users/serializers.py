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
        permissions_data = validated_data.pop('permissions', [])
        with transaction.atomic():  # Use atomic transaction
            type_instance = Type.objects.create(**validated_data)
            permission_ids = []
            for perm in permissions_data:
                try:
                    permission_ids.append(perm['id'])
                except KeyError:
                    raise serializers.ValidationError({'permissions': 'Each permission must include an "id".'})
            permissions = Permission.objects.filter(id__in=permission_ids)
            if len(permissions) != len(permission_ids):
                raise serializers.ValidationError("One or more permissions not found.")
            type_instance.permissions.set(permissions)  # Link existing permissions by ID
            return type_instance


    