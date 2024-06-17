import json
from django.http import HttpResponse # type: ignore
from django.shortcuts import render # type: ignore
# from requests import Response
from rest_framework.response import Response # type: ignore
from rest_framework import viewsets, status # type: ignore
from .serializers import *
from config.utils_methods import list_all_objects,create_instance,update_instance
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from rest_framework.filters import OrderingFilter # type: ignore
from .filters import OrderAttachmentsFilter, OrderShipmentsFilter, PaymentTransactionsFilter, SaleInvoiceItemsFilter, SaleInvoiceOrdersFilter, SaleOrderFilter, SaleOrderItemsFilter, SaleReturnItemsFilter, SaleReturnOrdersFilter, SalesPriceListFilter
# Create your views here.

from rest_framework.decorators import action, api_view # type: ignore
    

class SaleOrderView(viewsets.ModelViewSet):
    queryset = SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SaleOrderFilter
    ordering_fields = ['num_employees', 'created_at', 'updated_at', 'name']

    # def create(self, request, *args, **kwargs):
    #     given_data = request.data
    #     print()
    #     print('--------------GIVEN DATA FRONT END-------------')
    #     # for key, value in given_data.items():
    #     #     print(f'{key}: {value}')
    #     # print()
    #     saleorder = request.data['sale_order_data']
    #     saleorder_items = request.data['sale_order_items']
    #     print('------------------SALE_ORDER DATA----------------')
    #     for key, value in saleorder.items():
    #         print(f'{key}: {value}')
    #     print()
    #     serializer = self.get_serializer(data=request.data['sale_order_data'])

    #     #get product ID's
    #     product_ids = []
    #     for product in given_data.get('product_data', []):
    #         product_id = product.get('product_id')
    #         if product_id:
    #             product_ids.append(product_id)

        
    #     if serializer.is_valid():
    #         serializer.save()   # sale order data is saved 
    #         sale_order_id = serializer.data.get('sale_order_id', None) # from new instance id is fetched
    #         print('sale_order_id ----->>',sale_order_id)
    #         for product_id in product_ids:
    #             given_data['sale_order_items']['sale_order_id'] = sale_order_id # asign the sale_order_id to the sale_order_items json data
    #             given_data['sale_order_items']['product_id'] = product_id # asign the sale_order_id to the sale_order_items json data

    #             print('\n--------------SALE_ORDER_ITEMS_AFTER----------\n')
    #             for key, value in saleorder_items.items():
    #                 print(f'{key}: {value}')
    #             serializer = SaleOrderItemsSerializer(data=saleorder_items)
    #             if serializer.is_valid():
    #                 instance = serializer.save()
    #             # return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
    #         return Response({
    #             'status': True,
    #             'message': 'Record created successfully',
    #             'data': serializer.data
    #         })
    #     else:
    #         return Response({
    #             'status': False,
    #             'message': 'Form validation failed',
    #             'errors': serializer.errors
    #         }, status=status.HTTP_400_BAD_REQUEST)
    
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
    ordering_fields = ['reference_number','created_at']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SaleInvoiceItemsView(viewsets.ModelViewSet):
    queryset = SaleInvoiceItems.objects.all()
    serializer_class = SaleInvoiceItemsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SaleInvoiceItemsFilter
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

class SaleOrderItemsView(viewsets.ModelViewSet):
    queryset = SaleOrderItems.objects.all()
    serializer_class = SaleOrderItemsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SaleOrderItemsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class SaleInvoiceOrdersView(viewsets.ModelViewSet):
    queryset = SaleInvoiceOrders.objects.all()
    serializer_class = SaleInvoiceOrdersSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SaleInvoiceOrdersFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class SaleReturnOrdersView(viewsets.ModelViewSet):
    queryset = SaleReturnOrders.objects.all()
    serializer_class = SaleReturnOrdersSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SaleReturnOrdersFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SaleReturnItemsView(viewsets.ModelViewSet):
    queryset = SaleReturnItems.objects.all()
    serializer_class = SaleReturnItemsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SaleReturnItemsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class OrderAttachmentsView(viewsets.ModelViewSet):
    queryset = OrderAttachments.objects.all()
    serializer_class = OrderAttachmentsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = OrderAttachmentsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class OrderShipmentsView(viewsets.ModelViewSet):
    queryset = OrderShipments.objects.all()
    serializer_class = OrderShipmentsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = OrderShipmentsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)