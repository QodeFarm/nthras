from rest_framework import serializers
from .models import *

class Mod_StatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statuses
        fields = ['status_name']

class StatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statuses 
        fields = '__all__'