# myapp/serializers.py
from rest_framework import serializers

class CartItemSerializer(serializers.Serializer):
    last_cart_total_value = serializers.CharField()

class LastCartItemSerializer(serializers.Serializer):
    ProductRetailerId = serializers.CharField(max_length=100)
    Name = serializers.CharField(max_length=100)
    Quantity = serializers.IntegerField()
    Price = serializers.FloatField()
    Currency = serializers.CharField(max_length=10)

class OrderSerializer(serializers.Serializer):
    last_cart_items = LastCartItemSerializer(many=True)
    order_id = serializers.CharField(max_length=100)
