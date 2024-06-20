from django.shortcuts import render
from rest_framework import viewsets,generics,status,mixins as mi
from rest_framework.response import Response
from .models import Vendor, VendorCategory, VendorPaymentTerms, VendorAgent, VendorAttachment, VendorAddress
from .serializers import VendorSerializer, VendorCategorySerializer, VendorPaymentTermsSerializer, VendorAgentSerializer, VendorAttachmentSerializer, VendorAddressSerializer
from config.utils_methods import list_all_objects,create_instance,update_instance
#from config.utils_methods import add_key_value_to_all_ordereddicts, create_multi_instance, delete_multi_instance, list_all_objects,create_instance,update_instance, update_multi_instance

# Create your views here.

class VendorsView(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class VendorCategoryView(viewsets.ModelViewSet):
    queryset = VendorCategory.objects.all()
    serializer_class = VendorCategorySerializer 

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class VendorPaymentTermsView(viewsets.ModelViewSet):
    queryset = VendorPaymentTerms.objects.all()
    serializer_class = VendorPaymentTermsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)    

class VendorAgentView(viewsets.ModelViewSet):
    queryset = VendorAgent.objects.all()
    serializer_class = VendorAgentSerializer   

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class VendorAttachmentView(viewsets.ModelViewSet):
    queryset = VendorAttachment.objects.all()
    serializer_class = VendorAttachmentSerializer   

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class VendorAddressView(viewsets.ModelViewSet):
    queryset = VendorAddress.objects.all()
    serializer_class = VendorAddressSerializer   

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

#=======================CRUD_Operations==============================
def add_key_value_to_all_ordereddicts(od_list, key, value):
    for od in od_list:
        od[key] = value

def create_multi_instance(data_set,serializer_name):
    data_list = []
    for item_data in data_set:
        serializer = serializer_name(data=item_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            data_list.append(data)
    return data_list

def update_multi_instance(data_set,pk,main_model_name,current_model_name,serializer_name,main_model_field_name=None):
    data_list = []
    for data in data_set:
        # main model PK Field name
        main_model_pk_field_name = main_model_name._meta.pk.name
        # current model PK Field name
        current_model_field_name = current_model_name._meta.pk.name
        # Get the value of current model's PK field

        val = data.get(f'{current_model_field_name}')
        # Arrange arguments to filter
        if main_model_field_name is not None: # use external value if provided
            filter_kwargs = {main_model_field_name: pk, current_model_field_name:val}
        else:
            filter_kwargs = {main_model_pk_field_name: pk, current_model_field_name:val}
            
        instance = current_model_name.objects.filter(**filter_kwargs).first()
        serializer = serializer_name(instance, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data_list.append(data)
    return data_list

class VendorOneView(generics.GenericAPIView,mi.ListModelMixin, mi.CreateModelMixin,mi.RetrieveModelMixin,mi.UpdateModelMixin,mi.DestroyModelMixin):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get(self, request, *args, **kwargs):
            if 'pk' in kwargs:
                return self.retrieve(request, *args, **kwargs)  # Retrieve a single instance
            return self.list(request, *args, **kwargs)  # List all instances   
  

    # Handling POST requests for creating
    def post(self, request, *args, **kwargs):   #To avoid the error this method should be written "detail": "Method \"POST\" not allowed."
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        given_data = request.data
	
        vendors_data = given_data.pop('vendor_data')
        vendor_attachments_data = given_data.pop('vendor_attachments')
        vendor_addresses_data = given_data.pop('vendor_addresses')
		
        # create data in 'vendor' model
        serializer = self.get_serializer(data=vendors_data)
        if serializer.is_valid(raise_exception=True):
            # self.perform_create(serializer)
            serializer.save()
            data_1 = serializer.data

            vendor_id = serializer.data.get('vendor_id', None)          
            # create data in 'vendor_attachments' model
            add_key_value_to_all_ordereddicts(vendor_attachments_data,'vendor_id',vendor_id)
            data_2 =create_multi_instance(vendor_attachments_data,VendorAttachmentSerializer)

            # create data in 'vendor_addresses' model
            add_key_value_to_all_ordereddicts(vendor_addresses_data,'vendor_id',vendor_id)
            data_3 =create_multi_instance(vendor_addresses_data,VendorAddressSerializer)

            if data_1 and data_2 and data_3 :  
                custom_data = {
                    "vendor_data": data_1,
                    "vendor_attachments": data_2,
                    "vendor_addresses":data_3
                }
                return Response({
                    'status': True,
                    'message': 'Record created successfully',
                    'data': custom_data
                },status=status.HTTP_201_CREATED)
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

        # Query VendorAttachment model using the pk
        related_data = VendorAttachment.objects.filter(vendor_id=pk)  # Assuming 'sale_order_id' is the FK field
        attachments_serializer = VendorAttachmentSerializer(related_data, many=True)

        # Query VendorAddress model using the pk
        related_data = VendorAddress.objects.filter(vendor_id=pk)  # Assuming 'sale_order_id' is the FK field
        addresses_serializer = VendorAddressSerializer(related_data, many=True)

        # Customizing the response data
        custom_data = {
            "vendor_data": serializer.data,
            "vendor_attachments": attachments_serializer.data,
            "vendor_addresses":addresses_serializer.data,
        }
        return Response(custom_data)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data['vendor_data'], partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data_1 = serializer.data

        vendor_attachments_data = request.data.pop('vendor_attachments')
        pk = request.data['vendor_data'].get('vendor_id')
        data_2 = update_multi_instance(vendor_attachments_data,pk,Vendor,VendorAttachment,VendorAttachmentSerializer)

        vendor_addresses_data = request.data.pop('vendor_addresses')
        pk = request.data['vendor_data'].get('vendor_id')
        data_3 = update_multi_instance(vendor_addresses_data,pk,Vendor,VendorAddress,VendorAddressSerializer)

        if data_1 and data_2 and data_3:  
            custom_data = {
                "vendor_data": data_1,
                "vendor_attachments": data_2,
                "vendor_addresses":data_3
            }
            return Response({
                'status': True,
                'message': 'Update successful',
                'data': custom_data
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'message': 'Form validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            instance = Vendor.objects.get(pk=pk)
            instance.delete()
            return Response({'***Data Deleted Successfully***'}, status=status.HTTP_204_NO_CONTENT)

        except Vendor.DoesNotExist:
            return Response({'error': 'Instance not found.'}, status=status.HTTP_404_NOT_FOUND)