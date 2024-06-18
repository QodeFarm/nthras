from django.shortcuts import render
# from requests import Response
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from config.utils_methods import list_all_objects,create_instance,update_instance
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import OrderingFilter
#from .filters import SaleOrderFilter,InvoicesFilter,PaymentTransactionsFilter,OrderItemsFilter,ShipmentsFilter,SalesPriceListFilter,SaleOrderReturnsFilter
# Create your views here.

#================================================CHETAN STUFF====================================================
from rest_framework import generics
from .models import SaleOrder
from .serializers import SaleOrderSerializer


def add_key_value_to_all_ordereddicts(od_list, key, value):
    for od in od_list:
        od[key] = value

def create_multi_instance(data_set,serializer_name):
    for item_data in data_set:
        serializer = serializer_name(data=item_data)
        if serializer.is_valid():
            serializer.save()
        model_name = str(serializer_name.__class__.__name__)
    
class SaleOrderCreateView(generics.CreateAPIView):
    queryset = SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer

    def create(self, request, *args, **kwargs):
        given_data = request.data

        sale_order_data = given_data.pop('sale_order')
        sale_order_items_data = given_data.pop('sale_order_items')
        order_attachments_data = given_data.pop('order_attachments')
        order_shipments_data = given_data.pop('order_shipments')
        
        # create data in 'saleorder' model
        serializer = self.get_serializer(data=sale_order_data)
        if serializer.is_valid():
            serializer.save()
            print('***SaleOrder-successful***')
    
            # create data in 'saleorder_items' model
            sale_order_id = serializer.data.get('sale_order_id', None) # from Saleorder instance id is fetched
            add_key_value_to_all_ordereddicts(sale_order_items_data,'sale_order_id',sale_order_id)
            create_multi_instance(sale_order_items_data,SaleOrderItemsSerializer)
            print('***SaleOrderItems-successful***')

            # create data in 'order_attachments' model
            create_multi_instance(order_attachments_data,OrderAttachmentsSerializer)
            print('***OrderAttachments-successful***')

            # create data in 'order_shipments' model
            serializer = OrderShipmentsSerializer(data=order_shipments_data)
            if serializer.is_valid():
                serializer.save()        
            print('***\tAll Instances are Created***')

            return Response({'***data ceated successfully***'})

#================================================CHETAN STUFF====================================================
    

class SaleOrderView(viewsets.ModelViewSet):
    queryset = SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer
    # filter_backends = [DjangoFilterBackend,OrderingFilter]
    # filterset_class = SaleOrderFilter
    # ordering_fields = ['num_employees', 'created_at', 'updated_at', 'name']

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
    # filter_backends = [DjangoFilterBackend,OrderingFilter]
    # filterset_class = PaymentTransactionsFilter
    # ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SaleInvoiceItemsView(viewsets.ModelViewSet):
    queryset = SaleInvoiceItems.objects.all()
    serializer_class = SaleInvoiceItemsSerializer
    # filter_backends = [DjangoFilterBackend,OrderingFilter]
    # filterset_class = OrderItemsFilter
    # ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SalesPriceListView(viewsets.ModelViewSet):
    queryset = SalesPriceList.objects.all()
    serializer_class = SalesPriceListSerializer
    # filter_backends = [DjangoFilterBackend,OrderingFilter]
    # filterset_class = SalesPriceListFilter
    # ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SaleOrderItemsView(viewsets.ModelViewSet):
    queryset = SaleOrderItems.objects.all()
    serializer_class = SaleOrderItemsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class SaleInvoiceOrdersView(viewsets.ModelViewSet):
    queryset = SaleInvoiceOrders.objects.all()
    serializer_class = SaleInvoiceOrdersSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class SaleReturnOrdersView(viewsets.ModelViewSet):
    queryset = SaleReturnOrders.objects.all()
    serializer_class = SaleReturnOrdersSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SaleReturnItemsView(viewsets.ModelViewSet):
    queryset = SaleReturnItems.objects.all()
    serializer_class = SaleReturnItemsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class OrderAttachmentsView(viewsets.ModelViewSet):
    queryset = OrderAttachments.objects.all()
    serializer_class = OrderAttachmentsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class OrderShipmentsView(viewsets.ModelViewSet):
    queryset = OrderShipments.objects.all()
    serializer_class = OrderShipmentsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)