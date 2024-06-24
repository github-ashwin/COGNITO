"""
Serializers are classes that converts the necessary django models to JSON data
"""

from rest_framework.serializers import ModelSerializer
from main.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'