from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from utils_methods import *
from utils_variables import *

# Create your views here.
class PurchaseOrdersViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrdersSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class PurchaseorderItemsViewSet(viewsets.ModelViewSet):
    queryset = PurchaseorderItems.objects.all()
    serializer_class = PurchaseorderItemsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class PurchaseShipmentsViewSet(viewsets.ModelViewSet):
    queryset = PurchaseShipments.objects.all()
    serializer_class = PurchaseShipmentsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)