from rest_framework import serializers
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name', 'image']

class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name', 'image']

