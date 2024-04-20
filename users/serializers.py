from django.urls import get_resolver
from rest_framework import serializers
from .models import Permission, Type
from django.db import transaction
import logging
logger = logging.getLogger(__name__)
        
def validate_route(value):
    valid_paths = [pattern.pattern._route for pattern in get_resolver().url_patterns]
    if value not in valid_paths:
        raise serializers.ValidationError(f"The path {value} is not a valid route.")
    return value
    
class PermissionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validate_route])
    class Meta:
        model = Permission
        fields = ('id', 'name', 'identifier')

    def create(self, validated_data):
        return Permission.objects.create(**validated_data)

class PermissionIDOnlySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Permission
        fields = ['id']

class TypeSerializer(serializers.ModelSerializer):
    permissions = PermissionIDOnlySerializer(many=True, write_only=True)

    class Meta:
        model = Type
        fields = ('id', 'name', 'permissions')

    def create(self, validated_data):
        try:
            permissions_data = validated_data.pop('permissions', [""])
            with transaction.atomic():  
                type_instance = Type.objects.create(**validated_data)
                permission_ids = []
                for perm in permissions_data:
                    try:
                        permission_ids.append(perm['id'])
                    except KeyError:
                        raise serializers.ValidationError({
                            'permissions': 'Each permission must include an "id".',
                            'data': permissions_data
                        })
                permissions = Permission.objects.filter(id__in=permission_ids)
                if len(permissions) != len(permission_ids):
                    raise serializers.ValidationError("One or more permissions not found.")
                type_instance.permissions.set(permissions)  # Link existing permissions by ID
                return type_instance
        except Exception as e:
            raise serializers.ValidationError(str(e))
        
    def to_representation(self, instance):
        representation = super().to_representation(instance) 
        permissions = PermissionSerializer(instance.permissions.all(), many=True).data
        representation['permissions'] = permissions
        return representation