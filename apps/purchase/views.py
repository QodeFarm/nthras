from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from utils_methods import *
from utils_variables import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import PurchaseOrdersFilter,PurchaseorderItemsFilter,PurchaseShipmentsFilter,PurchasePriceListFilter,PurchaseOrderReturnsFilter

# Create your views here.
class PurchaseOrdersViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrdersSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = PurchaseOrdersFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class PurchaseorderItemsViewSet(viewsets.ModelViewSet):
    queryset = PurchaseorderItems.objects.all()
    serializer_class = PurchaseorderItemsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = PurchaseorderItemsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class PurchaseShipmentsViewSet(viewsets.ModelViewSet):
    queryset = PurchaseShipments.objects.all()
    serializer_class = PurchaseShipmentsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = PurchaseShipmentsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class PurchasePriceListViewSet(viewsets.ModelViewSet):
    queryset = PurchasePriceList.objects.all()
    serializer_class = PurchasePriceListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = PurchasePriceListFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
		
class PurchaseOrderReturnsViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderReturns.objects.all()
    serializer_class = PurchaseOrderReturnsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = PurchaseOrderReturnsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)