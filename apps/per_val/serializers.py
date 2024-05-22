# myapp/serializers.py
from rest_framework import serializers

class CartItemSerializer(serializers.Serializer):
    last_cart_items_text = serializers.CharField()

class CartItemSerializer(serializers.Serializer):
    last_cart_items = serializers.CharField()

class ProductSerializer(serializers.Serializer):
    ProductRetailerId = serializers.IntegerField()
    Name = serializers.CharField(max_length=100)
    Quantity = serializers.IntegerField()
    Price = serializers.FloatField()
    Currency = serializers.CharField(max_length=3)
