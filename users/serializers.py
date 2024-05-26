from django.urls import get_resolver
from rest_framework import serializers
from .models import Permission, Type
from django.db import transaction
import logging
logger = logging.getLogger(__name__)

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'identifier')

class TypeSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())

    class Meta:
        model = Type
        fields = ('id', 'name', 'permissions')
    
    def create(self, validated_data):
        permission_data = validated_data.pop('permissions')
        type_instance = Type.objects.create(**validated_data)
        type_instance.permissions.set(permission_data)
        return type_instance
    
    def update(self, instance, validated_data):
        permission_data = validated_data.pop('permissions')
        update = super().update(instance, validated_data)
        update.permissions.set(permission_data)
        return update
        
    def to_representation(self, instance):
        representation = super().to_representation(instance) 
        permissions = PermissionSerializer(instance.permissions.all(), many=True).data
        representation['permissions'] = permissions
        return representation