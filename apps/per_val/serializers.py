# myapp/serializers.py
from rest_framework import serializers

class CartItemSerializer(serializers.Serializer):
    last_cart_total_value = serializers.CharField()

class LastCartItemSerializer(serializers.Serializer):
    last_cart_items = serializers.CharField()

class ProductSerializer(serializers.Serializer):
    ProductRetailerId = serializers.IntegerField()
    Name = serializers.CharField(max_length=100)
    Quantity = serializers.IntegerField()

