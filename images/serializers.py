from rest_framework import serializers
from django.db import models

from images.models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image']

    def to_representation(self, instance):
        return instance.image.url
    def to_internal_value(self, data):
        try:
            return Image.objects.get(id=data)
        except Image.DoesNotExist:
            raise serializers.ValidationError("No image exists with the given ID.")

class ImageModelSerializer(serializers.ModelSerializer):
    # use image serializer for image field automatically
    image = ImageSerializer()
    