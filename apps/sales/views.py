from django.shortcuts import render
from rest_framework import viewsets, generics, mixins as mi
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from config.utils_methods import add_key_value_to_all_ordereddicts, create_multi_instance, delete_multi_instance, list_all_objects,create_instance,update_instance, update_multi_instance
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import OrderingFilter
#from .filters import SaleOrderFilter,InvoicesFilter,PaymentTransactionsFilter,OrderItemsFilter,ShipmentsFilter,SalesPriceListFilter,SaleOrderReturnsFilter
# Create your views here.

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


#---------- ONE API - MULTIPLE API CALLS (CRUD OPERATIONS) ---------------

class SaleOrderOneView(generics.GenericAPIView,mi.ListModelMixin,mi.CreateModelMixin,mi.RetrieveModelMixin,mi.UpdateModelMixin,mi.DestroyModelMixin):
    queryset = SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer

    def get(self, request, *args, **kwargs):
            if 'pk' in kwargs:
                return self.retrieve(request, *args, **kwargs)  # Retrieve a single instance
            return list_all_objects(self, request, *args, **kwargs)
    
    # Handling POST requests for creating
    def post(self, request, *args, **kwargs):   #To avoid the error this method should be written [error : "detail": "Method \"POST\" not allowed."]
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        given_data = request.data

        sale_order_data = given_data.pop('sale_order')
        sale_order_items_data = given_data.pop('sale_order_items')
        order_attachments_data = given_data.pop('order_attachments')
        order_shipments_data = given_data.pop('order_shipments')
        
        # create data in 'saleorder' model
        serializer = self.get_serializer(data=sale_order_data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
        # if serializer.is_valid():
        #     serializer.save()
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
            if serializer.is_valid(raise_exception=True):
                serializer.save()        
            print('***\tAll Instances are Created***')

            return Response({sale_order_id})

            # return Response({'***data ceated successfully***'})

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')  # Access the pk from kwargs
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Query SaleOrderItems model using the pk
        items_related_data = SaleOrderItems.objects.filter(sale_order_id=pk)  # 'sale_order_id' is the FK field
        items_related_serializer = SaleOrderItemsSerializer(items_related_data, many=True)

        # get order_id value from SaleOrder Instance 
        order_id = serializer.data.get('order_no')

        # Query OrderAttachments model using the order_id
        attachments_related_data = OrderAttachments.objects.filter(order_id=str(order_id))
        attachments_related_serializer = OrderAttachmentsSerializer(attachments_related_data, many=True)

        # Query OrderShipments model using the order_id
        shipments_related_data = OrderShipments.objects.filter(order_id=str(order_id))
        shipments_related_serializer = OrderShipmentsSerializer(shipments_related_data, many=True)

        # Customizing the response data
        custom_data = {
            "sale_order": serializer.data,
            "sale_order_items": items_related_serializer.data,
            "order_attachments":attachments_related_serializer.data,
            "order_shipments": shipments_related_serializer.data,
        }
        return Response(custom_data)
        
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data['sale_order'], partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print('***SaleOrder updated ***')

        sale_order_items_data = request.data.pop('sale_order_items')
        pk = request.data['sale_order'].get('sale_order_id')
        update_multi_instance(sale_order_items_data,pk,SaleOrder,SaleOrderItems,SaleOrderItemsSerializer)
        print('***SaleOrderItems updated ***')

        order_attachments_data = request.data.pop('order_attachments')
        pk = request.data['sale_order'].get('order_no')
        update_multi_instance(order_attachments_data,pk,SaleOrder,OrderAttachments,OrderAttachmentsSerializer,main_model_field_name='order_id')
        print('***OrderAttachments updated ***')

        order_shipments_data = request.data.pop('order_shipments')
        pk = request.data['sale_order'].get('order_no')  # Fetch value from main model
        update_multi_instance(order_shipments_data,pk,SaleOrder,OrderShipments,OrderShipmentsSerializer,main_model_field_name='order_id')
        print('***OrderShipments updated ***')

        return Response({'***data updated successfully***'})
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        try:
            instance = SaleOrder.objects.get(pk=pk)
            del_value = instance.order_no  # Fetch value from main model
            delete_multi_instance(del_value,SaleOrder,OrderAttachments,OrderAttachmentsSerializer,main_model_field_name='order_id')
            delete_multi_instance(del_value,SaleOrder,OrderShipments,OrderShipmentsSerializer,main_model_field_name='order_id')
            instance.delete()

            return Response({'***Data Deleted Successfully***'}, status=status.HTTP_204_NO_CONTENT)

        except SaleOrder.DoesNotExist:
            return Response({'error': 'Instance not found.'}, status=status.HTTP_404_NOT_FOUND)