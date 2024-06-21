from django.shortcuts import render,get_object_or_404
from django.http import  Http404
from rest_framework import viewsets, generics, mixins as mi
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from config.utils_methods import add_key_value_to_all_ordereddicts, create_multi_instance, delete_multi_instance, list_all_objects,create_instance,update_instance, update_multi_instance,build_response
from apps.masters.models import OrderTypes
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
            # self.perform_create(serializer)
            serializer.save()
            saleorder_data = serializer.data
    
            # create data in 'saleorder_items' model
            sale_order_id = serializer.data.get('sale_order_id', None) # from Saleorder instance id is fetched
            add_key_value_to_all_ordereddicts(sale_order_items_data,'sale_order_id',sale_order_id) #in sale_order_id replace sale_order_id from new instance
            items_data = create_multi_instance(sale_order_items_data,SaleOrderItemsSerializer)

            # Fetching the 'order_type_id' by 'order_type'
            order_type_val = order_attachments_data[0].get('order_type')
            order_type = OrderTypes.objects.get(name=order_type_val)
            order_type_id = order_type.order_type_id

            # Updated user choice with associated ID in 'name_id_dictionary'
            add_key_value_to_all_ordereddicts(order_attachments_data,'order_type_id',order_type_id)
            #in order_id replace sale_order_id from new instance
            add_key_value_to_all_ordereddicts(order_attachments_data,'order_id',sale_order_id) 
            attachments_data = create_multi_instance(order_attachments_data,OrderAttachmentsSerializer)

            # create data in 'order_shipments' model
            order_shipments_data['order_id'] = sale_order_id
            order_shipments_data['order_type_id'] = order_type_id

            serializer = OrderShipmentsSerializer(data=order_shipments_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                shipments_data = serializer.data   

            if saleorder_data and items_data and attachments_data and shipments_data:  
                custom_data = [
                    {"sale_order": saleorder_data},
                    {"sale_order_items": items_data},
                    {"order_attachments":attachments_data},
                    {"order_shipments": shipments_data}
                ]
                return build_response(1, "Record created successfully", custom_data, status.HTTP_201_CREATED)
            else:
                return build_response(0, "Record creation failed", [], status.HTTP_400_BAD_REQUEST)   

    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')  # Access the pk from kwargs
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            # Query SaleOrderItems model using the pk
            items_related_data = SaleOrderItems.objects.filter(sale_order_id=pk)  # 'sale_order_id' is the FK field
            items_related_serializer = SaleOrderItemsSerializer(items_related_data, many=True)

            # Query OrderAttachments model using the order_id
            attachments_related_data = OrderAttachments.objects.filter(order_id=str(pk))
            attachments_related_serializer = OrderAttachmentsSerializer(attachments_related_data, many=True)

            # Query OrderShipments model using the order_id
            shipments_related_data = OrderShipments.objects.filter(order_id=str(pk))
            shipments_related_serializer = OrderShipmentsSerializer(shipments_related_data, many=True)

            # Customizing the response data
            custom_data = [
                {"sale_order": serializer.data},
                {"sale_order_items": items_related_serializer.data},
                {"order_attachments":attachments_related_serializer.data},
                {"order_shipments": shipments_related_serializer.data}
            ]
            return build_response(1, "Success", custom_data, status.HTTP_200_OK)

        except Http404:
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data['sale_order'], partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        saleorder_data = serializer.data

        # Update sale_order_items 
        sale_order_items_data = request.data.pop('sale_order_items')
        pk = request.data['sale_order'].get('sale_order_id')
        items_data = update_multi_instance(sale_order_items_data,pk,SaleOrder,SaleOrderItems,SaleOrderItemsSerializer)

        # Update sale_order_attachments
        order_attachments_data = request.data.pop('order_attachments')
        pk = request.data['sale_order'].get('sale_order_id')
        attachments_data = update_multi_instance(order_attachments_data,pk,SaleOrder,OrderAttachments,OrderAttachmentsSerializer,main_model_field_name='order_id')

        # Update order_shipments
        order_shipments_data = request.data.pop('order_shipments')
        pk = request.data['sale_order'].get('sale_order_id')  # Fetch value from main model
        shipments_data = update_multi_instance(order_shipments_data,pk,SaleOrder,OrderShipments,OrderShipmentsSerializer,main_model_field_name='order_id')

        if saleorder_data and items_data and attachments_data and shipments_data:  
            custom_data = {
                "sale_order": saleorder_data,
                "sale_order_items": items_data,
                "order_attachments":attachments_data,
                "order_shipments": shipments_data
            }
            return Response({
                'count': 1,
                'message': 'Record updated successfully',
                'data': custom_data
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'count': 0,
                'message': 'Record updation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')  # Here 'pk'  is the primarykey of queried object

        try:
            instance = SaleOrder.objects.get(pk=pk)
            delete_multi_instance(pk,SaleOrder,OrderAttachments,main_model_field_name='order_id')
            delete_multi_instance(pk,SaleOrder,OrderShipments,main_model_field_name='order_id')
            instance.delete()

            # If Main model exists
            return build_response(1, "Record deleted successfully", [], status.HTTP_204_NO_CONTENT)
            
        except SaleOrder.DoesNotExist:
            # IF main model is not Found
            return build_response(0, "Record deletion failed", [], status.HTTP_404_NOT_FOUND)