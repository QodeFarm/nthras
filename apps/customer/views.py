from django.shortcuts import render
from rest_framework import viewsets, generics, mixins as mi
from apps.customer.filters import LedgerAccountsFilters, CustomerFilters, CustomerAddressesFilters, CustomerAttachmentsFilters
from .models import *
from .serializers import *
from config.utils_methods import list_all_objects, create_instance, update_instance
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


def add_key_value_to_all_ordereddicts(od_list, key, value):
    for od in od_list:
        od[key] = value
 
def create_multi_instance(data_set,serializer_name):
    for item_data in data_set:
        serializer = serializer_name(data=item_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
 
def update_multi_instance(data_set,pk,main_model_name,current_model_name,serializer_name,main_model_field_name=None):
    for data in data_set:
        # main model PK Field name
        main_model_pk_field_name = main_model_name._meta.pk.name
        # current model PK Field name
        current_model_field_name = current_model_name._meta.pk.name
        # Get the value of current model's PK field
 
        val = data.get(f'{current_model_field_name}')
        # Arrange arguments to filter
        if main_model_field_name is not None:
            filter_kwargs = {main_model_field_name: pk, current_model_field_name:val}
        else:
            filter_kwargs = {main_model_pk_field_name: pk, current_model_field_name:val}
 
        instance = current_model_name.objects.filter(**filter_kwargs).first()
        serializer = serializer_name(instance, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
 
def delete_multi_instance(del_value,main_model_name,current_model_name,serializer_name,main_model_field_name=None):
    # main model PK Field name
    main_model_pk_field_name = main_model_name._meta.pk.name
 
    # Arrange arguments to filter
    if main_model_field_name is not None: # use external value if provided
        filter_kwargs = {main_model_field_name: del_value}
    else:
        filter_kwargs = {main_model_pk_field_name: del_value}
 
    deleted_count, _ = current_model_name.objects.filter(**filter_kwargs).delete()
 
    if deleted_count > 0:
        print(f'***Data Deleted Successfully***')
    else:
        return Response({f'***error: {current_model_name} not found or already deleted.***'})    

class TestCustomerCreateViews(generics.CreateAPIView,mi.ListModelMixin,mi.CreateModelMixin,mi.RetrieveModelMixin,mi.UpdateModelMixin,mi.DestroyModelMixin):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def get(self, request, *args, **kwargs):
        result = None
        if 'pk' in kwargs:
            result = self.retrieve(request, *args, **kwargs)
        else:
            result = list_all_objects(self, request, *args, **kwargs)
        return result
    
    # Handling POST requests for creating
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        given_data = request.data
        print(given_data)

        customer_data = given_data.pop('customer_data')
        customer_attachments_data = given_data.pop('customer_attachments')
        customer_addresses_data = given_data.pop('customer_addresses')
        
        serializer = self.get_serializer(data=customer_data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            print('***Customers-Data-successful***')
    
            customer_id = serializer.data.get('customer_id', None)
            print(customer_id)
            add_key_value_to_all_ordereddicts(customer_attachments_data,'customer_id',customer_id)
            create_multi_instance(customer_attachments_data,CustomerAttachmentsSerializers)
            print('***Customer-Attachments-successful***')

            add_key_value_to_all_ordereddicts(customer_addresses_data,'customer_id',customer_id)
            create_multi_instance(customer_addresses_data,CustomerAddressesSerializers)
            print('***Customer-Addresses-successful***')

            return Response({customer_id})
        
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Query CustomerAttachments model using the pk
        items_related_data = CustomerAttachments.objects.filter(customer_id=pk)
        items_related_serializer = CustomerAttachmentsSerializers(items_related_data, many=True)

        # get customer_id value from Customers Instance 
        customer_id = serializer.data.get('customer_id')

        # Query CustomerAddresses model using the order_id
        attachments_related_data = CustomerAddresses.objects.filter(customer_id=str(customer_id))
        attachments_related_serializer = CustomerAddressesSerializers(attachments_related_data, many=True)

        # Customizing the response data
        custom_data = {
            "customers": serializer.data,
            "customer_attachments": items_related_serializer.data,
            "customer_addresses":attachments_related_serializer.data,
        }
        return Response(custom_data)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data['customers'], partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print('***Customers updated ***')

        customer_attachments_data = request.data.pop('customer_attachments')
        pk = request.data['customers'].get('customer_id')
        update_multi_instance(customer_attachments_data,pk,Customer,CustomerAttachments,CustomerAttachmentsSerializers)
        print('***CustomerAttachements updated ***')

        customer_addresses_data = request.data.pop('customer_addresses')
        pk = request.data['customers'].get('customer_id')
        update_multi_instance(customer_addresses_data,pk,Customer,CustomerAddresses,CustomerAddressesSerializers,main_model_field_name='customer_id')
        print('***CustomerAddresses updated ***')

        return Response({'***data updated successfully***'})
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        try:
            instance = Customer.objects.get(pk=pk)
            del_value = instance.customer_id  # Fetch value from main model
            delete_multi_instance(del_value,Customer,CustomerAttachments,CustomerAttachmentsSerializers,main_model_field_name='customer_id')
            delete_multi_instance(del_value,Customer,CustomerAddresses,CustomerAddressesSerializers,main_model_field_name='customer_id')
            instance.delete()

            return Response({'***Data Deleted Successfully***'}, status=status.HTTP_204_NO_CONTENT)

        except Customer.DoesNotExist:
            return Response({'error': 'Instance not found.'}, status=status.HTTP_404_NOT_FOUND)