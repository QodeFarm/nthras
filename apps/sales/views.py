import logging
from django.db import transaction
from django.forms import ValidationError
from django.http import  Http404
from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets, status
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from .serializers import *
from apps.masters.models import OrderTypes
from config.utils_methods import create_multi_instance, delete_multi_instance, get_object_or_none, list_all_objects, create_instance, update_instance, build_response, update_multi_instance, update_ordereddicts_with_ids

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger object
logger = logging.getLogger(__name__)

class SaleOrderView(viewsets.ModelViewSet):
    queryset = SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer
    
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class PaymentTransactionsView(viewsets.ModelViewSet):
    queryset = PaymentTransactions.objects.all()
    serializer_class = PaymentTransactionsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SaleInvoiceItemsView(viewsets.ModelViewSet):
    queryset = SaleInvoiceItems.objects.all()
    serializer_class = SaleInvoiceItemsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SalesPriceListView(viewsets.ModelViewSet):
    queryset = SalesPriceList.objects.all()
    serializer_class = SalesPriceListSerializer

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


class SaleOrderViewSet(APIView):
    """
    API ViewSet for handling sale order creation and related data.
    """
    def get_object(self, pk):
        try:
            return SaleOrder.objects.get(pk=pk)
        except SaleOrder.DoesNotExist:
            logger.warning(f"SaleOrder with ID {pk} does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)

    def get(self, request,  *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(self, request, *args, **kwargs)
        try:
            instance = SaleOrder.objects.all()
        except SaleOrder.DoesNotExist:
            logger.error("Sale order does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        else:
            serializer = SaleOrderSerializer(instance, many=True)
            logger.info("Sale order data retrieved successfully.")
            return build_response(instance.count(), "Success", serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a sale order and its related data (items, attachments, and shipments).
        """
        try:
            pk = kwargs.get('pk')
            if not pk:
                logger.error("Primary key not provided in request.")
                return build_response(0, "Primary key not provided", [], status.HTTP_400_BAD_REQUEST)

            # Retrieve the SaleOrder instance
            sale_order = get_object_or_404(SaleOrder, pk=pk)
            sale_order_serializer = SaleOrderSerializer(sale_order)

            # Retrieve related data
            items_data = self.get_related_data(SaleOrderItems, SaleOrderItemsSerializer, 'sale_order_id', pk)
            attachments_data = self.get_related_data(OrderAttachments, OrderAttachmentsSerializer, 'order_id', pk)
            shipments_data = self.get_related_data(OrderShipments, OrderShipmentsSerializer, 'order_id', pk)

            # Customizing the response data
            custom_data = {
                "sale_order": sale_order_serializer.data,
                "sale_order_items": items_data,
                "order_attachments": attachments_data,
                "order_shipments": shipments_data
            }
            logger.info("Sale order and related data retrieved successfully.")
            return build_response(1, "Success", custom_data, status.HTTP_200_OK)

        except Http404:
            logger.error("Sale order with pk %s does not exist.", pk)
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("An error occurred while retrieving sale order with pk %s: %s", pk, str(e))
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
        Handles the deletion of a sale order and its related attachments and shipments.
        """
        try:
            # Get the SaleOrder instance
            instance = SaleOrder.objects.get(pk=pk)

            # Delete related OrderAttachments and OrderShipments
            if not delete_multi_instance(pk, SaleOrder, OrderAttachments, main_model_field_name='order_id'):
                return build_response(0, "Error deleting related order attachments", [], status.HTTP_500_INTERNAL_SERVER_ERROR)
            if not delete_multi_instance(pk, SaleOrder, OrderShipments, main_model_field_name='order_id'):
                return build_response(0, "Error deleting related order shipments", [], status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Delete the main SaleOrder instance
            instance.delete()

            logger.info(f"SaleOrder with ID {pk} deleted successfully.")
            return build_response(1, "Record deleted successfully", [], status.HTTP_204_NO_CONTENT)
        except SaleOrder.DoesNotExist:
            logger.warning(f"SaleOrder with ID {pk} does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting SaleOrder with ID {pk}: {str(e)}")
            return build_response(0, "Record deletion failed due to an error", [], status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Handling POST requests for creating
    def post(self, request, *args, **kwargs):   #To avoid the error this method should be written [error : "detail": "Method \"POST\" not allowed."]
        return self.create(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Handles the creation of sale order, sale order items, order attachments, and order shipments.
        Sale order and sale order items are mandatory. Order attachments and order shipments are optional.
        """
        given_data = request.data

        # Extracting data from the request
        sale_order_data = given_data.pop('sale_order', None)
        sale_order_items_data = given_data.pop('sale_order_items', None)
        order_attachments_data = given_data.pop('order_attachments', None)
        order_shipments_data = given_data.pop('order_shipments', None)

        # Ensure mandatory data is present
        if not sale_order_data or not sale_order_items_data:
            logger.error("Sale order and sale order items are mandatory but not provided.")
            return build_response(0, "Sale order and sale order items are mandatory", [], status.HTTP_400_BAD_REQUEST)

        response_data = {}
        errors = []

        try:
            # Create sale order
            saleorder_data = self.create_sale_order(sale_order_data)
            if not saleorder_data:
                logger.error("Sale order creation failed.")
                return build_response(0, "Sale order creation failed", [], status.HTTP_400_BAD_REQUEST)

            sale_order_id = saleorder_data.get('sale_order_id')
            self.add_sale_order_id_to_items(sale_order_items_data, sale_order_id)

            # Create sale order items
            items_data, items_errors = create_multi_instance(sale_order_items_data, SaleOrderItemsSerializer)
            if not items_data:
                logger.error("Sale order items creation failed.")
                return build_response(0, "Sale order items creation failed", [], status.HTTP_400_BAD_REQUEST, items_errors)

            response_data = [
                {"sale_order": saleorder_data},
                {"sale_order_items": items_data}
            ]
            errors.extend(items_errors)

            order_type_id = None

            # Check if optional data exists and fetch order_type_id if necessary
            if order_attachments_data or order_shipments_data:
                order_type_id = self.get_order_type_id_from_sale_order(sale_order_data)
                logger.debug("Order type ID retrieved: %s", order_type_id)

            if order_attachments_data:
                self.update_attachments_data(order_attachments_data, sale_order_id, order_type_id)
                attachments_data, attachments_errors = create_multi_instance(order_attachments_data, OrderAttachmentsSerializer)
                response_data.append({"order_attachments": attachments_data})
                errors.extend(attachments_errors)

            if order_shipments_data:
                shipments_data, shipment_errors = self.create_order_shipments(order_shipments_data, sale_order_id, order_type_id)
                response_data.append({"order_shipments": shipments_data})
                errors.extend(shipment_errors)

            if errors:
                logger.warning("Record created with some errors: %s", errors)
                return build_response(1, "Record created with errors", response_data, status.HTTP_201_CREATED, errors)

            logger.info("Record created successfully.")
            return build_response(1, "Record created successfully", response_data, status.HTTP_201_CREATED)

        except Exception as e:
            logger.error("Error creating sale order: %s", str(e))
            return build_response(0, "Record creation failed due to an error", [], status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_sale_order(self, sale_order_data):
        """
        Creates a sale order in the database.
        """
        serializer = SaleOrderSerializer(data=sale_order_data)
        try:
            serializer.is_valid(raise_exception=True)  # Validate sale order data
            serializer.save()  # Save valid sale order to the database
            logger.debug("Sale order created with data: %s", serializer.data)
            return serializer.data
        except ValidationError as e:
            logger.error("Validation error on sale order: %s", str(e))  # Log validation error
            return None

    def add_sale_order_id_to_items(self, sale_order_items_data, sale_order_id):
        """
        Adds the sale_order_id to each item in the sale_order_items_data list.
        """
        update_ordereddicts_with_ids(sale_order_items_data, 'sale_order_id', sale_order_id)

    # def get_order_type_id_from_sale_order(self, sale_order_data):
    def get_order_type_id_from_sale_order(self, sale_order_data):
        """
        Fetches the order_type_id from the sale_order_data.
        """
        order_type_val = sale_order_data.get('order_type')
        order_type = get_object_or_none(OrderTypes, name=order_type_val)
        return order_type.order_type_id if order_type else None

    def update_attachments_data(self, order_attachments_data, sale_order_id, order_type_id):
        """
        Updates order_attachments_data with order_type_id and sale_order_id.
        """
        update_ordereddicts_with_ids(order_attachments_data, 'order_type_id', order_type_id)
        update_ordereddicts_with_ids(order_attachments_data, 'order_id', sale_order_id)

    def create_order_shipments(self, order_shipments_data, sale_order_id, order_type_id):
        """
        Creates an order shipment in the database.
        """
        order_shipments_data['order_id'] = sale_order_id
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
        saleorder_data = items_data = attachments_data = shipments_data = response_data = None
        errors = []

        partial = kwargs.pop('partial', False)
        instance = self.get_object(pk)
        serializer = SaleOrderSerializer(instance, data=request.data['sale_order'], partial=partial)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        except Exception as e:
            logger.error("Validation error: %s", str(e))  # Log validation errors
            errors.append(str(e))  # Collect validation errors
        else:
            saleorder_data = serializer.data

            # Update sale_order_items 
            sale_order_items_data = request.data.pop('sale_order_items')
            items_data, item_errors = update_multi_instance(pk, sale_order_items_data, SaleOrderItems, SaleOrderItemsSerializer, filter_field_1='sale_order_id')
            errors.extend(item_errors)

            # # Update sale_order_attachments
            order_attachments_data = request.data.pop('order_attachments')
            attachments_data, attachments_errors = update_multi_instance(pk, order_attachments_data, OrderAttachments, OrderAttachmentsSerializer, filter_field_1='order_id')
            errors.extend(attachments_errors)

            # Update order_shipments
            order_shipments_data = request.data.pop('order_shipments')
            shipments_data, shipments_errors = update_multi_instance(pk, order_shipments_data, OrderShipments, OrderShipmentsSerializer, filter_field_1='order_id')
            errors.extend(shipments_errors)

            if errors:
                logger.warning("Record created with some errors: %s", errors)
                return build_response(1, "Record created with errors", response_data, status.HTTP_201_CREATED, errors)

        #  Here 'or' operator is used becaused data can be either empty list or filled with data. so that all the model data can be represented on output
        if saleorder_data or items_data or attachments_data or shipments_data:
            custom_data = {
                "sale_order": saleorder_data,
                "sale_order_items": items_data,
                "order_attachments":attachments_data,
                "order_shipments": shipments_data
            }
            response_data = build_response(1, "Record updated successfully", custom_data, status.HTTP_200_OK)
        else:
            logger.error("Error in SaleOrderOneView")
            response_data = build_response(0, "Record updation failed", [errors], status.HTTP_400_BAD_REQUEST)
        
        return response_data