from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets, generics, mixins as mi
from apps.customer.filters import LedgerAccountsFilters, CustomerFilters, CustomerAddressesFilters, CustomerAttachmentsFilters
from .models import *
from .serializers import *
from config.utils_methods import add_key_value_to_all_ordereddicts, create_multi_instance, delete_multi_instance, list_all_objects,create_instance,update_instance, update_multi_instance,build_response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

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

class CustomerCreateViews(generics.CreateAPIView,mi.ListModelMixin,mi.CreateModelMixin,mi.RetrieveModelMixin,mi.UpdateModelMixin,mi.DestroyModelMixin):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return list_all_objects(self, request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)   

    def create(self, request, *args, **kwargs):
        given_data = request.data

        customer_data = given_data.pop('customer_data')
        customer_attachments = given_data.pop('customer_attachments')
        customer_addresses = given_data.pop('customer_addresses')
        
        serializer = self.get_serializer(data=customer_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            customer_data = serializer.data
    
            customer_id = serializer.data.get('customer_id', None) 
            add_key_value_to_all_ordereddicts(customer_attachments,'customer_id',customer_id)
            attachments_data = create_multi_instance(customer_attachments,CustomerAttachmentsSerializers)

            add_key_value_to_all_ordereddicts(customer_addresses,'customer_id',customer_id) 
            addresses_data = create_multi_instance(customer_addresses,CustomerAddressesSerializers)

            if customer_data and attachments_data and addresses_data:  
                custom_data = [
                    {"customer_data": customer_data},
                    {"customer_attachments": attachments_data},
                    {"customer_addresses": addresses_data}
                ]
                return build_response(1, "Record created successfully", custom_data, status.HTTP_201_CREATED)
            else:
                return build_response(0, "Record creation failed", [], status.HTTP_400_BAD_REQUEST)   

    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')  # Access the pk from kwargs
            instance = self.get_object()
            serializer = self.get_serializer(instance)
 
            # Query CustomerAttachment model using the pk
            attachments_related_data = CustomerAttachments.objects.filter(customer_id=pk)  
            attachments_serializer = CustomerAttachmentsSerializers(attachments_related_data, many=True)
 
            # Query CustomerAddress model using the pk
            addresses_related_data = CustomerAddresses.objects.filter(customer_id=pk)  
            addresses_serializer = CustomerAddressesSerializers(addresses_related_data, many=True)
 
            # Customizing the response data
            custom_data = [
                {"customer_data": serializer.data},
                {"customer_attachments": attachments_serializer.data},
                {"customer_addresses":addresses_serializer.data}
            ]
            return build_response(1, "Success", custom_data, status.HTTP_200_OK)
 
        except Http404:
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
 
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data['customer_data'], partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        customer_data = serializer.data
 
        # Update customer_attachments
        customer_attachments_data = request.data.pop('customer_attachments')
        pk = request.data['customer_data'].get('customer_id')
        attachments_data = update_multi_instance(customer_attachments_data,pk,Customer,CustomerAttachments,CustomerAttachmentsSerializers)
 
        # Update customer_addresses
        customer_addresses_data = request.data.pop('customer_addresses')
        pk = request.data['customer_data'].get('customer_id')
        addresses_data = update_multi_instance(customer_addresses_data,pk,Customer,CustomerAddresses,CustomerAddressesSerializers)
 
        if customer_data and attachments_data and addresses_data :  
            custom_data = {
                "customer_data": customer_data,
                "customer_attachments": attachments_data,
                "customer_addresses":addresses_data
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
        pk = kwargs.get('pk')
        try:
            instance = Customer.objects.get(pk=pk)
            instance.delete()
            # If Main model exists
            return build_response(1, "Record deleted successfully", [], status.HTTP_204_NO_CONTENT)
           
        except Customer.DoesNotExist:
            # IF main model is not Found
            return build_response(0, "Record deletion failed", [], status.HTTP_404_NOT_FOUND) 