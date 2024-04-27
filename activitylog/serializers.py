from rest_framework import serializers

from .models import ActivityLog

from django.contrib.contenttypes.models import ContentType

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'
        ordering = ['-action_time']

class ActivityLogSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all(),
        required=False
    )
    object_id = serializers.IntegerField(required=False)
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = ['id', 'actor', 'actor_ip', 'action_type', 'action_time', 'remarks', 'status', 'content_type', 'object_id', 'content_object']
        ordering = ['-action_time']
    def get_content_object(self, obj):
        if obj.content_object:
            return str(obj.content_object)
        return None