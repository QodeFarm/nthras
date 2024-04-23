from rest_framework import serializers
from .models import *
from apps.masters.serializers import *
from apps.customer.serializers import *

class WarehousesSerializer(serializers.ModelSerializer):
    item_type = ProductItemTypeSerializer(source='item_type_id',read_only=True)
    customer = ModCustomersSerializer(source='customer_id',read_only=True)
    city = ModCitySerializer(source='city_id', read_only = True)
    class Meta:
        model = Warehouses
        fields = '__all__'