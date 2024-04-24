from django.urls import get_resolver
from rest_framework import serializers
from .models import Permission, Type
from django.db import transaction
import logging
logger = logging.getLogger(__name__)
from django.urls import URLResolver, URLPattern, get_resolver
from django.urls.resolvers import RegexPattern, RoutePattern

def get_all_url_patterns(resolver, base_path=''):
    url_patterns = []
    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLResolver):
            # Recursively fetch patterns from included URLconf
            next_level = f"{base_path}{pattern.pattern.regex.pattern}" if hasattr(pattern.pattern, 'regex') else f"{base_path}{pattern.pattern._route}"
            url_patterns.extend(get_all_url_patterns(pattern, base_path=next_level))
        elif isinstance(pattern, URLPattern):
            # Handle different types of patterns
            if hasattr(pattern.pattern, 'regex'):
                full_pattern = f"{base_path}{pattern.pattern.regex.pattern}"
                # Remove regex characters and the end of string regex symbol
                full_pattern = full_pattern.replace('^', '').replace('$', '').replace('\\Z', '')
                url_patterns.append(full_pattern)
            else:
                # Standard route patterns, remove the end of string symbol
                full_pattern = f"{base_path}{pattern.pattern._route}".replace('\\Z', '')
                url_patterns.append(full_pattern)
    return url_patterns

def validate_route(value):
    all_urls = get_all_url_patterns(get_resolver())
    if value not in all_urls:
        raise serializers.ValidationError({
            "error": f"The path '{value}' is not a valid route.",
            "valid_routes": all_urls
        })
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