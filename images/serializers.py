from rest_framework import serializers
from django.db import models

from images.models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image']

    def to_representation(self, instance):
        return instance.image.url

class ImageModelSerializer(serializers.ModelSerializer):
    # use image serializer for image field automatically
    image = ImageSerializer()
    