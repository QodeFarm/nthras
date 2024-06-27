import logging
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import *
from .serializers import *
from config.utils_methods import *
from config.utils_variables import *
from config.utils_methods import create_multi_instance, delete_multi_instance, get_object_or_none, list_all_objects, create_instance, update_instance, build_response, update_ordereddicts_with_ids, update_multi_instance
from apps.sales.serializers import OrderAttachmentsSerializer,OrderShipmentsSerializer
from apps.sales.models import OrderAttachments,OrderShipments
from rest_framework import viewsets
from apps.masters.models import OrderTypes
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.serializers import ValidationError

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger object
logger = logging.getLogger(__name__)

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
    

class PurchaseOrderViewSet(APIView):
    """
    API ViewSet for handling purchase order creation and related data.
    """
    def get_object(self, pk):
        try:
            return PurchaseOrders.objects.get(pk=pk)
        except PurchaseOrders.DoesNotExist:
            logger.warning(f"PurchaseOrders with ID {pk} does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        try:
            instance = PurchaseOrders.objects.all()
        except PurchaseOrders.DoesNotExist:
            logger.error("Purchase order does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        else:
            serializer = PurchaseOrdersSerializer(instance, many=True)
            logger.info("Purchase order data retrieved successfully.")
            return build_response(instance.count(), "Success", serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a purchase order and its related data (items, attachments, and shipments).
        """
        try:
            pk = kwargs.get('pk')
            if not pk:
                logger.error("Primary key not provided in request.")
                return build_response(0, "Primary key not provided", [], status.HTTP_400_BAD_REQUEST)

            # Retrieve the PurchaseOrders instance
            purchase_order = get_object_or_404(PurchaseOrders, pk=pk)
            purchase_order_serializer = PurchaseOrdersSerializer(purchase_order)

            # Retrieve related data
            items_data = self.get_related_data(PurchaseorderItems, PurchaseorderItemsSerializer, 'purchase_order_id', pk)
            attachments_data = self.get_related_data(OrderAttachments, OrderAttachmentsSerializer, 'order_id', pk)
            shipments_data = self.get_related_data(OrderShipments, OrderShipmentsSerializer, 'order_id', pk)

            # Customizing the response data
            custom_data = {
                "purchase_order": purchase_order_serializer.data,
                "purchase_order_items": items_data,
                "order_attachments": attachments_data,
                "order_shipments": shipments_data
            }
            logger.info("Purchase order and related data retrieved successfully.")
            return build_response(1, "Success", custom_data, status.HTTP_200_OK)

        except Http404:
            logger.error("Purchase order with pk %s does not exist.", pk)
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("An error occurred while retrieving purchase order with pk %s: %s", pk, str(e))
            return build_response(0, "An error occurred", [], status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_related_data(self, model, serializer_class, filter_field, filter_value):
        """
        Retrieves related data for a given model, serializer, and filter field.
        """
        try:
            related_data = model.objects.filter(**{filter_field: filter_value})
            serializer = serializer_class(related_data, many=True)
            logger.debug("Retrieved related data for model %s with filter %s=%s.", model.__name__, filter_field, filter_value)
            return serializer.data
        except Exception as e:
            logger.exception("Error retrieving related data for model %s with filter %s=%s: %s", model.__name__, filter_field, filter_value, str(e))
            return []
      
    @transaction.atomic
    def delete(self, request, pk, *args, **kwargs):
        """
        Handles the deletion of a purchase order and its related attachments and shipments.
        """
        try:
            # Get the PurchaseOrders instance
            instance = PurchaseOrders.objects.get(pk=pk)

            # Delete related OrderAttachments and OrderShipments
            if not delete_multi_instance(pk, PurchaseOrders, OrderAttachments, main_model_field_name='order_id'):
                return build_response(0, "Error deleting related order attachments", [], status.HTTP_500_INTERNAL_SERVER_ERROR)
            if not delete_multi_instance(pk, PurchaseOrders, OrderShipments, main_model_field_name='order_id'):
                return build_response(0, "Error deleting related order shipments", [], status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Delete the main PurchaseOrders instance
            instance.delete()

            logger.info(f"PurchaseOrders with ID {pk} deleted successfully.")
            return build_response(1, "Record deleted successfully", [], status.HTTP_204_NO_CONTENT)
        except PurchaseOrders.DoesNotExist:
            logger.warning(f"PurchaseOrders with ID {pk} does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting PurchaseOrders with ID {pk}: {str(e)}")
            return build_response(0, "Record deletion failed due to an error", [], status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Handling POST requests for creating
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Handles the creation of purchase order, purchase order items, order attachments, and order shipments.
        Purchase order and purchase order items are mandatory. Order attachments and order shipments are optional.
        """
        given_data = request.data

        # Extracting data from the request
        purchase_order_data = given_data.pop('purchase_order', None)
        purchase_order_items_data = given_data.pop('purchase_order_items', None)
        order_attachments_data = given_data.pop('order_attachments', None)
        order_shipments_data = given_data.pop('order_shipments', None)

        # Ensure mandatory data is present
        if not purchase_order_data or not purchase_order_items_data:
            logger.error("Purchase order and purchase order items are mandatory but not provided.")
            return build_response(0, "Purchase order and purchase order items are mandatory", [], status.HTTP_400_BAD_REQUEST)

        response_data = {}
        errors = []

        try:
            # Create purchase order
            purchaseorder_data = self.create_purchase_order(purchase_order_data)
            if not purchaseorder_data:
                logger.error("Purchase order creation failed.")
                return build_response(0, "Purchase order creation failed", [], status.HTTP_400_BAD_REQUEST)

            purchase_order_id = purchaseorder_data.get('purchase_order_id')
            self.add_purchase_order_id_to_items(purchase_order_items_data, purchase_order_id)

            # Create purchase order items
            items_data, items_errors = create_multi_instance(purchase_order_items_data, PurchaseorderItemsSerializer)
            if not items_data:
                logger.error("Purchase order items creation failed.")
                return build_response(0, "Purchase order items creation failed", [], status.HTTP_400_BAD_REQUEST, items_errors)

            response_data = [
                {"purchase_order": purchaseorder_data},
                {"purchase_order_items": items_data}
            ]
            errors.extend(items_errors)

            order_type_id = None

            # Check if optional data exists and fetch order_type_id if necessary
            if order_attachments_data or order_shipments_data:
                order_type_id = self.get_order_type_id_from_purchase_order(purchase_order_data)
                logger.debug("Order type ID retrieved: %s", order_type_id)

            if order_attachments_data:
                self.update_attachments_data(order_attachments_data, purchase_order_id, order_type_id)
                attachments_data, attachments_errors = create_multi_instance(order_attachments_data, OrderAttachmentsSerializer)
                response_data.append({"order_attachments": attachments_data})
                errors.extend(attachments_errors)

            if order_shipments_data:
                shipments_data, shipment_errors = self.create_order_shipments(order_shipments_data, purchase_order_id, order_type_id)
                response_data.append({"order_shipments": shipments_data})
                errors.extend(shipment_errors)

            if errors:
                logger.warning("Record created with some errors: %s", errors)
                return build_response(1, "Record created with errors", response_data, status.HTTP_201_CREATED, errors)

            logger.info("Record created successfully.")
            return build_response(1, "Record created successfully", response_data, status.HTTP_201_CREATED)

        except Exception as e:
            logger.error("Error creating purchase order: %s", str(e))
            return build_response(0, "Record creation failed due to an error", [], status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_purchase_order(self, purchase_order_data):
        """
        Creates a purchase order in the database.
        """
        serializer = PurchaseOrdersSerializer(data=purchase_order_data)
        try:
            serializer.is_valid(raise_exception=True)  # Validate purchase order data
            serializer.save()  # Save valid purchase order to the database
            logger.debug("Purchase order created with data: %s", serializer.data)
            return serializer.data
        except ValidationError as e:
            logger.error("Validation error on purchase order: %s", str(e))  # Log validation error
            return None

    def add_purchase_order_id_to_items(self, purchase_order_items_data, purchase_order_id):
        """
        Adds the purchase_order_id to each item in the purchase_order_items_data list.
        """
        update_ordereddicts_with_ids(purchase_order_items_data, 'purchase_order_id', purchase_order_id)

    def get_order_type_id_from_purchase_order(self, purchase_order_data):
        """
        Fetches the order_type_id from the purchase_order_data.
        """
        order_type_val = purchase_order_data.get('order_type')
        order_type = get_object_or_none(OrderTypes, name=order_type_val)
        return order_type.order_type_id if order_type else None

    def update_attachments_data(self, order_attachments_data, purchase_order_id, order_type_id):
        """
        Updates order_attachments_data with order_type_id and purchase_order_id.
        """
        update_ordereddicts_with_ids(order_attachments_data, 'order_type_id', order_type_id)
        update_ordereddicts_with_ids(order_attachments_data, 'order_id', purchase_order_id)

    def create_order_shipments(self, order_shipments_data, purchase_order_id, order_type_id):
        """
        Creates an order shipment in the database.
        """
        order_shipments_data['order_id'] = purchase_order_id
        order_shipments_data['order_type_id'] = order_type_id
        serializer = OrderShipmentsSerializer(data=order_shipments_data)
        try:
            serializer.is_valid(raise_exception=True)  # Validate order shipments data
            serializer.save()  # Save valid order shipments to the database
            logger.debug("Order shipment created with data: %s", serializer.data)
            return serializer.data, []
        except ValidationError as e:
            logger.error("Validation error on order shipments: %s", str(e))  # Log validation error
            return None, [str(e)]
        
    def put(self, request, pk, *args, **kwargs):
        purchaseorder_data = items_data = attachments_data = shipments_data = response_data = None
        errors = []

        partial = kwargs.pop('partial', False)
        instance = self.get_object(pk)
        serializer = PurchaseOrdersSerializer(instance, data=request.data['purchase_order'], partial=partial)
        try:
            if serializer.is_valid(raise_exception=False):
                serializer.save()

        except Exception as e:
            logger.error("Validation error: %s", str(e))  # Log validation errors
            errors.append(str(e))  # Collect validation errors

        else:
            purchaseorder_data = serializer.data
            # Update purchase_order_items 
            purchase_order_items_data = request.data.pop('purchase_order_items')
            items_data, item_errors = update_multi_instance(pk, purchase_order_items_data, PurchaseorderItems, PurchaseorderItemsSerializer, filter_field_1='purchase_order_id')
            errors.extend(item_errors)
            # Update purchase_order_attachments
            order_attachments_data = request.data.pop('order_attachments')
            attachments_data, attachments_errors = update_multi_instance(pk, order_attachments_data, OrderAttachments, OrderAttachmentsSerializer, filter_field_1='order_id')
            errors.extend(attachments_errors)
            #  Update order_shipments
            order_shipments_data = request.data.pop('order_shipments')
            shipments_data, shipments_errors = update_multi_instance(pk, order_shipments_data, OrderShipments, OrderShipmentsSerializer, filter_field_1='order_id')
            errors.extend(shipments_errors)
            if errors:
                logger.warning("Record created with some errors: %s", errors)
                return build_response(1, "Record created with errors", response_data, status.HTTP_201_CREATED, errors)
            
        #  Here 'or' operator is used becaused data can be either empty list or filled with data. so that all the model data can be represented on output
        if purchaseorder_data or items_data or attachments_data or shipments_data:
            custom_data = {
                "purchase_order": purchaseorder_data,
                "purchase_order_items": items_data,
                "order_attachments":attachments_data,
                "order_shipments": shipments_data
            }
            response_data = build_response(1, "Record updated successfully", custom_data, status.HTTP_200_OK)
        else:
            logger.error("Error in PurchaseOrderViewSet")
            response_data = build_response(0, "Record updation failed", [serializer.errors], status.HTTP_400_BAD_REQUEST)
        
        return response_data