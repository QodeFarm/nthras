# myapp/serializers.py
from rest_framework import serializers

class CartItemSerializer(serializers.Serializer):
    last_cart_total_value = serializers.CharField()
