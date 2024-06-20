from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from config.utils_methods import *
from config.utils_variables import *
from rest_framework import generics
from config.utils_methods import add_key_value_to_all_ordereddicts, create_multi_instance, delete_multi_instance, list_all_objects,create_instance,update_instance, update_multi_instance
from apps.sales.serializers import OrderAttachmentsSerializer,OrderShipmentsSerializer
from apps.sales.models import OrderAttachments,OrderShipments
from rest_framework import viewsets, generics, mixins as mi
from apps.masters.models import OrderTypes

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
 
class PurchaseInvoiceOrdersViewSet(viewsets.ModelViewSet):
    queryset = PurchaseInvoiceOrders.objects.all()
    serializer_class = PurchaseInvoiceOrdersSerializer
 
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)
 
    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)
 
    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
 
class PurchaseInvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseInvoiceItem.objects.all()
    serializer_class = PurchaseInvoiceItemSerializer
 
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)
 
    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)
 
    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
 
class PurchaseReturnOrdersViewSet(viewsets.ModelViewSet):
    queryset = PurchaseReturnOrders.objects.all()
    serializer_class = PurchaseReturnOrdersSerializer
 
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)
 
    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)
 
    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
   
class PurchaseReturnItemsViewSet(viewsets.ModelViewSet):
    queryset = PurchaseReturnItems.objects.all()
    serializer_class = PurchaseReturnItemsSerializer
 
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)
 
    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)
 
    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
 
class PurchasePriceListViewSet(viewsets.ModelViewSet):
    queryset = PurchasePriceList.objects.all()
    serializer_class = PurchasePriceListSerializer
 
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)
 
    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)
 
    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class purchaseOrdersCreateView(generics.GenericAPIView, mi.ListModelMixin, mi.CreateModelMixin, mi.RetrieveModelMixin, mi.UpdateModelMixin, mi.DestroyModelMixin):
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrdersSerializer
 
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)  # Retrieve a single instance
        return list_all_objects(self, request, *args, **kwargs)
 
    # Handling POST requests for creating
    def post(self, request, *args, **kwargs):  # To avoid the error this method should be written
        return self.create(request, *args, **kwargs)
 
    def create(self, request, *args, **kwargs):
        given_data = request.data
        purchase_order_data = given_data.pop('purchase_order_data')
        purchase_order_items_data = given_data.pop('purchase_order_items')
        order_attachments_data = given_data.pop('order_attachments')
        order_shipments_data = given_data.pop('order_shipments')
 
        # Create data in 'purchaseorder' model
        serializer = self.get_serializer(data=purchase_order_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data_1 = serializer.data
 
            # Create data in 'purchaseorder_items' model
            purchase_order_id = serializer.data.get('purchase_order_id', None)  # from PurchaseOrder instance id is fetched
            add_key_value_to_all_ordereddicts(purchase_order_items_data, 'purchase_order_id', purchase_order_id) #in purchase_order_id replace purchase_order_id from new instance
            data_2 = create_multi_instance(purchase_order_items_data, PurchaseorderItemsSerializer)
 
            # create data in 'order_attachments' model
            add_key_value_to_all_ordereddicts(order_attachments_data, 'order_id', purchase_order_id) #in order_id replace purchase_order_id from new instance
            data_3 = create_multi_instance(order_attachments_data, OrderAttachmentsSerializer)
 
            # create data in 'order_shipments' model
            provided_val = order_shipments_data.get('order_type_id')
            get_id = OrderTypes.objects.all()
            name_id_dictionary = {}
            for obj in get_id:
                name = obj.name
                id = obj.order_type_id
                name_id_dictionary[name] = id
            order_shipments_data['order_id'] = purchase_order_id
            order_shipments_data['order_type_id'] = name_id_dictionary.get(provided_val)
        
            serializer = OrderShipmentsSerializer(data=order_shipments_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data_4 = serializer.data
 
            if data_1 and data_2 and data_3 and data_4:  
                custom_data = {
                    "purchase_order": data_1,
                    "purchase_order_items": data_2,
                    "order_attachments": data_3,
                    "order_shipments": data_4
                }
                return Response({
                    'status': True,
                    'message': 'Record created successfully',
                    'data': custom_data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': False,
                    'message': 'Form validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)       
 
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')  # Access the pk from kwargs
        instance = self.get_object()
        serializer = self.get_serializer(instance)
 
        # Query PurchaseOrderItems model using the pk
        items_related_data = PurchaseorderItems.objects.filter(purchase_order_id=pk)  # 'purchase_order_id' is the FK field
        items_related_serializer = PurchaseorderItemsSerializer(items_related_data, many=True)
 
        # Get order_id value from PurchaseOrder instance
        order_id = serializer.data.get('purchase_order_id')
 
        # Query OrderAttachments model using the order_id
        attachments_related_data = OrderAttachments.objects.filter(order_id=str(pk))
        attachments_related_serializer = OrderAttachmentsSerializer(attachments_related_data, many=True)
 
        # Query OrderShipments model using the order_id
        shipments_related_data = OrderShipments.objects.filter(order_id=str(order_id))
        shipments_related_serializer = OrderShipmentsSerializer(shipments_related_data, many=True)
 
        # Customizing the response data
        custom_data = {
            "purchase_order": serializer.data,
            "purchase_order_items": items_related_serializer.data,
            "order_attachments": attachments_related_serializer.data,
            "order_shipments": shipments_related_serializer.data,
        }
        return Response(custom_data)
 
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
 
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data['purchase_order'], partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data_1 = serializer.data
        # Update purchase_order_items
        purchase_order_items_data = request.data.pop('purchase_order_items')
        pk = request.data['purchase_order'].get('purchase_order_id')
        data_2 = update_multi_instance(purchase_order_items_data, pk, PurchaseOrders, PurchaseorderItems, PurchaseorderItemsSerializer)
 
        # Update purchase_order_attachments
        order_attachments_data = request.data.pop('order_attachments')
        pk = request.data['purchase_order'].get('purchase_order_id')
        data_3 = update_multi_instance(order_attachments_data, pk, PurchaseOrders, OrderAttachments, OrderAttachmentsSerializer, main_model_field_name='order_id')
        # Update order_shipments
        order_shipments_data = request.data.pop('order_shipments')
        pk = request.data['purchase_order'].get('purchase_order_id')  # Fetch value from main model
        data_4 = update_multi_instance(order_shipments_data, pk, PurchaseOrders, OrderShipments, OrderShipmentsSerializer, main_model_field_name='order_id')
 
        if data_1 and data_2 and data_3 and data_4:  
            custom_data = {
                "purchase_order": data_1,
                "purchase_order_items": data_2,
                "order_attachments": data_3,
                "order_shipments": data_4
            }
            return Response({
                'status': True,
                'message': 'Update successful',
                'data': custom_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'message': 'Form validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')    # Here 'pk'  is the primarykey of queried object
 
        try:
            instance = PurchaseOrders.objects.get(pk=pk)
            delete_multi_instance(pk, PurchaseOrders, OrderAttachments, main_model_field_name='order_id')
            delete_multi_instance(pk, PurchaseOrders, OrderShipments, main_model_field_name='order_id')
            instance.delete()
 
            return Response(status=status.HTTP_204_NO_CONTENT)
 
        except PurchaseOrders.DoesNotExist:
            return Response({'error': 'Instance not found.'}, status=status.HTTP_404_NOT_FOUND)
 