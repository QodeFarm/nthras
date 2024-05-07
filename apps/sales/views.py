from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from utils_methods import list_all_objects,create_instance,update_instance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import SaleOrderFilter,InvoicesFilter,PaymentTransactionsFilter,OrderItemsFilter,ShipmentsFilter,SalesPriceListFilter,SaleOrderReturnsFilter
# Create your views here.

    

class SaleOrderView(viewsets.ModelViewSet):
    queryset = SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SaleOrderFilter
    ordering_fields = ['num_employees', 'created_at', 'updated_at', 'name']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     print(queryset.query)
    #     return queryset
    
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    


class PaymentTransactionsView(viewsets.ModelViewSet):
    queryset = PaymentTransactions.objects.all()
    serializer_class = PaymentTransactionsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = PaymentTransactionsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class InvoicesView(viewsets.ModelViewSet):
    queryset = Invoices.objects.all()
    serializer_class = InvoicesSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = InvoicesFilter
    ordering_fields = []


    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class OrderItemsView(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = OrderItemsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class ShipmentsView(viewsets.ModelViewSet):
    queryset = Shipments.objects.all()
    serializer_class = ShipmentsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = ShipmentsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SalesPriceListView(viewsets.ModelViewSet):
    queryset = SalesPriceList.objects.all()
    serializer_class = SalesPriceListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SalesPriceListFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SaleOrderReturnsView(viewsets.ModelViewSet):
    queryset = SaleOrderReturns.objects.all()
    serializer_class = SaleOrderReturnsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SaleOrderReturnsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    