from rest_framework import serializers
from .models import *

class ModCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_id','country_name']

class ModStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['state_id','state_name']

class ModCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_id','city_name']
        
class ModStatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statuses
        fields = ['status_id','status_name']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    country = ModCountrySerializer(source='country_id', read_only = True)
    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    state = ModStateSerializer(source='state_id', read_only = True)
    class Meta:
        model = City
        fields = '__all__'
        
class StatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statuses 
        fields = '__all__'