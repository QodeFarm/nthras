# myapp/views.py
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

class TotalView(APIView):
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            last_cart_total_value = serializer.validated_data['last_cart_total_value']
            try:
                # Parse the JSON string
                data = json.loads(last_cart_total_value)
                total = data['Total']
                return Response({'Total': total}, status=status.HTTP_200_OK)
            except (json.JSONDecodeError, KeyError):
                return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailsView(APIView):
    def post(self, request):
        serializer = LastCartItemSerializer(data=request.data)
        if serializer.is_valid():
            last_cart_items_text = serializer.validated_data['last_cart_items']
            try:
                # Parse the JSON string
                last_cart_items = json.loads(last_cart_items_text)
                # Extract required fields
                products = [
                    {
                        "ProductRetailerId": item["ProductRetailerId"],
                        "Name": item["Name"],
                        "Quantity": item["Quantity"]
                    } for item in last_cart_items
                ]
                return Response(products, status=status.HTTP_200_OK)
            except (json.JSONDecodeError, KeyError):
                return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
