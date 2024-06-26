from django.http import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, generics, mixins as mi
from apps.customer.filters import LedgerAccountsFilters, CustomerFilters, CustomerAddressesFilters, CustomerAttachmentsFilters
from .models import *
from .serializers import *
from config.utils_methods import create_multi_instance, list_all_objects, create_instance, update_instance, build_response, update_ordereddicts_with_ids
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
import logging
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError

# Create your views here.

class LedgerAccountsViews(viewsets.ModelViewSet):
    queryset = LedgerAccounts.objects.all()
    serializer_class = LedgerAccountsSerializers
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = LedgerAccountsFilters
    ordering_fields = ['name', 'created_at', 'updated_at']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class CustomerViews(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = CustomerFilters
    ordering_fields = ['name', 'created_at', 'updated_at']

    def list(self, request, *args, **kwargs):
        summary = request.query_params.get('summary', 'false').lower() == 'true'
        if summary:
            customers = self.filter_queryset(self.get_queryset())
            data = CustomerOptionSerializer.get_customer_summary(customers)
            
            Result = Response(data, status=status.HTTP_200_OK)
        else:
            Result = list_all_objects(self, request, *args, **kwargs)
        
        return Result

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
    
class CustomerAddressesViews(viewsets.ModelViewSet):
    queryset = CustomerAddresses.objects.all()
    serializer_class = CustomerAddressesSerializers
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = CustomerAddressesFilters 
    ordering_fields = ['created_at', 'updated_at']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class CustomerAttachmentsViews(viewsets.ModelViewSet):
    queryset = CustomerAttachments.objects.all()
    serializer_class = CustomerAttachmentsSerializers
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = CustomerAttachmentsFilters 
    ordering_fields = ['attachment_name', 'created_at', 'updated_at']
    
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
#==========================================================================   
logger = logging.getLogger(__name__)   

class CustomerCreateViews(APIView):
    
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            logger.warning(f"Customer with ID {pk} does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        
    def get(self, request,  *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(self, request, *args, **kwargs)
        try:
            instance = Customer.objects.all()
        except Customer.DoesNotExist:
            logger.error("Customer does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        else:
            serializer = CustomerSerializer(instance, many=True)
            logger.info("Customer data retrieved successfully.")
            return build_response(instance.count(), "Success", serializer.data, status.HTTP_200_OK)
            
    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not pk:
                logger.error("Primary key not provided in request.")
                return build_response(0, "Primary key not provided", [], status.HTTP_400_BAD_REQUEST)

            # Retrieve the SaleOrder instance
            customer = get_object_or_404(Customer, pk=pk)
            customer_serializer = CustomerSerializer(customer)

            # Retrieve related data            
            attachments_data = self.get_related_data(CustomerAttachments, CustomerAttachmentsSerializers, 'customer_id', pk)
            addresses_data = self.get_related_data(CustomerAddresses, CustomerAddressesSerializers, 'customer_id', pk)

            # Customizing the response data
            custom_data = {
                "customer_data": customer_serializer.data,
                "customer_attachments": attachments_data,
                "customer_addresses": addresses_data
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

    # Handling POST requests for creating
    def post(self, request, *args, **kwargs):   #To avoid the error this method should be written [error : "detail": "Method \"POST\" not allowed."]
        return self.create(request, *args, **kwargs)
   
    @transaction.atomic
    def create(self, request, *args, **kwargs):

        given_data = request.data
 
        # Extracting data from the request
        customer_data = given_data.pop('customer_data', None)
        customer_attachments_data = given_data.pop('customer_attachments', None)
        customer_addresses_data = given_data.pop('customer_addresses', None)
 
        # Ensure mandatory customer data is present
        if not customer_data or not customer_attachments_data or not customer_addresses_data:
            logger.error("Customer data , Customer attachments_data and Customer Addresses are mandatory but not provided.")
            return build_response(0, "Customer data , Customer attachments data and Customer Addresses data  are mandatory", [], status.HTTP_400_BAD_REQUEST)
 
        response_data = {}
        errors = []
 
        try:
            # Create customer
            customer_data = self.create_customer(customer_data)
            if not customer_data:
                logger.error("customer creation failed.")
                return build_response(0, "customer creation failed", [], status.HTTP_400_BAD_REQUEST)
 
            customer_id = customer_data.get('customer_id')
            self.add_customer_id_to_attachments(customer_attachments_data, customer_id)
 
            # Create customer Attachment
            attachments_data, attachments_errors = create_multi_instance(customer_attachments_data, CustomerAttachmentsSerializers)
            if not attachments_data:
                logger.error("customer Attachment creation failed.")
                return build_response(0, "customer Attachment creation failed", [], status.HTTP_400_BAD_REQUEST, attachments_errors)
 
            self.add_customer_id_to_addresses(customer_addresses_data, customer_id)
 
            # Create customer Address
            addresses_data, addresses_errors = create_multi_instance(customer_addresses_data, CustomerAddressesSerializers)
            if not addresses_data:
                logger.error("customer Address creation failed.")
                return build_response(0, "customer Address creation failed", [], status.HTTP_400_BAD_REQUEST, addresses_errors)
 
            response_data = [
                {"customer_data": customer_data},
                {"customer_attachments": attachments_data},
                {"customer_addresses":addresses_data}
            ]
            error = attachments_errors + addresses_errors
            errors.extend(error)
 
            if errors:
                logger.warning("Record created with some errors: %s", errors)
                return build_response(1, "Record created with errors", response_data, status.HTTP_201_CREATED, errors)
 
            logger.info("Record created successfully.")
            return build_response(1, "Record created successfully", response_data, status.HTTP_201_CREATED)
 
        except Exception as e:
            logger.error("Error creating customer: %s", str(e))
            return build_response(0, "Record creation failed due to an error", [], status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create_customer(self, customer_data):
        """
        Creates a customer in the database.
        """
        serializer = CustomerSerializer(data=customer_data)
        try:
            serializer.is_valid(raise_exception=True)  # Validate sale order data
            serializer.save()  # Save valid sale order to the database
            logger.debug("customer created with data: %s", serializer.data)
            return serializer.data
        except ValidationError as e:
            logger.error("Validation error on customer: %s", str(e))  # Log validation error
            return None
       
    def add_customer_id_to_attachments(self, customer_attachments_data, customer_id):
        """
        Adds the customer_id to each attachments in the customer_attachments_data list.
        """
        update_ordereddicts_with_ids(customer_attachments_data, 'customer_id', customer_id)
 
    def add_customer_id_to_addresses(self, customer_addresses_data, customer_id):
        """
        Adds the customer_id to each addresses in the customer_addresses_data list.
        """
        update_ordereddicts_with_ids(customer_addresses_data, 'customer_id', customer_id)

    @transaction.atomic
    def delete(self, request, pk, *args, **kwargs):
        """
        Handles the deletion of a sale order and its related attachments and shipments.
        """
        try:
            # Get the SaleOrder instance
            instance = Customer.objects.get(pk=pk)
 
            # Delete the main SaleOrder instance
            instance.delete()
 
            logger.info(f"Customer with ID {pk} deleted successfully.")
            return build_response(1, "Record deleted successfully", [], status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            logger.warning(f"Customer with ID {pk} does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting Customer with ID {pk}: {str(e)}")
            return build_response(0, "Record deletion failed due to an error", [], status.HTTP_500_INTERNAL_SERVER_ERROR)