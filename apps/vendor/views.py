from django.shortcuts import render,get_object_or_404
from django.http import  Http404
from rest_framework import viewsets,generics,status,mixins as mi
from rest_framework.response import Response
from .models import Vendor, VendorCategory, VendorPaymentTerms, VendorAgent, VendorAttachment, VendorAddress
from .serializers import VendorSerializer, VendorCategorySerializer, VendorPaymentTermsSerializer, VendorAgentSerializer, VendorAttachmentSerializer, VendorAddressSerializer
from config.utils_methods import add_key_value_to_all_ordereddicts, create_multi_instance, delete_multi_instance, list_all_objects,create_instance,update_instance, update_multi_instance,build_response
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

#===========ONE API - MULTIPLE API CALLS (CRUD OPERATIONS)===========
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
            vendors_data = serializer.data
		
            # create data in 'vendor_attachments' model
            vendor_id = serializer.data.get('vendor_id', None)  
            add_key_value_to_all_ordereddicts(vendor_attachments_data,'vendor_id',vendor_id)
            attachments_data =create_multi_instance(vendor_attachments_data,VendorAttachmentSerializer)

            # create data in 'vendor_addresses' model
            add_key_value_to_all_ordereddicts(vendor_addresses_data,'vendor_id',vendor_id)
            addresses_data =create_multi_instance(vendor_addresses_data,VendorAddressSerializer)
			
            if vendors_data and attachments_data and addresses_data :  
                custom_data = [
                    {"vendor_data": vendors_data},
                    {"vendor_attachments": attachments_data},
                    {"vendor_addresses":addresses_data}
                ]
                return build_response(1, "Record created successfully", custom_data, status.HTTP_201_CREATED)
            else:
                return build_response(0, "Record creation failed", [], status.HTTP_400_BAD_REQUEST)
				
    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')  # Access the pk from kwargs
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            # Query VendorAttachment model using the pk
            attachments_related_data = VendorAttachment.objects.filter(vendor_id=pk)  
            attachments_serializer = VendorAttachmentSerializer(attachments_related_data, many=True)

            # Query VendorAddress model using the pk
            addresses_related_data = VendorAddress.objects.filter(vendor_id=pk)  
            addresses_serializer = VendorAddressSerializer(addresses_related_data, many=True)

            # Customizing the response data
            custom_data = [
                {"vendor_data": serializer.data},
                {"vendor_attachments": attachments_serializer.data},
                {"vendor_addresses":addresses_serializer.data}
            ]
            return build_response(1, "Success", custom_data, status.HTTP_200_OK)

        except Http404:
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)

    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data['vendor_data'], partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        vendors_data = serializer.data

		# Update vendor_attachments
        vendor_attachments_data = request.data.pop('vendor_attachments')
        pk = request.data['vendor_data'].get('vendor_id')
        attachments_data = update_multi_instance(vendor_attachments_data,pk,Vendor,VendorAttachment,VendorAttachmentSerializer)

        # Update vendor_addresses
        vendor_addresses_data = request.data.pop('vendor_addresses')
        pk = request.data['vendor_data'].get('vendor_id')
        addresses_data = update_multi_instance(vendor_addresses_data,pk,Vendor,VendorAddress,VendorAddressSerializer)

        if vendors_data and attachments_data and addresses_data :  
            custom_data = {
                "vendor_data": vendors_data,
                "vendor_attachments": attachments_data,
                "vendor_addresses":addresses_data
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
            instance = Vendor.objects.get(pk=pk)
            instance.delete()
            # If Main model exists
            return build_response(1, "Record deleted successfully", [], status.HTTP_204_NO_CONTENT)
            
        except Vendor.DoesNotExist:
            # IF main model is not Found
            return build_response(0, "Record deletion failed", [], status.HTTP_404_NOT_FOUND)