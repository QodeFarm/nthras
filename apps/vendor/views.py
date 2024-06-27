import logging
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import render,get_object_or_404
from django.http import  Http404
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from .models import Vendor, VendorCategory, VendorPaymentTerms, VendorAgent, VendorAttachment, VendorAddress
from .serializers import VendorSerializer, VendorCategorySerializer, VendorPaymentTermsSerializer, VendorAgentSerializer, VendorAttachmentSerializer, VendorAddressSerializer
from config.utils_methods import create_multi_instance, delete_multi_instance, get_object_or_none, list_all_objects, create_instance, update_instance, build_response, update_multi_instance, update_ordereddicts_with_ids

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get an instance of a logger
logger = logging.getLogger(__name__)

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

class VendorViewSet(APIView):
    """
    API ViewSet for handling vendor creation and related data.
    """
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            logger.warning(f"Vendor with ID {pk} does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        
    def get(self, request,  *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(self, request, *args, **kwargs)
        try:
            instance = Vendor.objects.all()
        except Vendor.DoesNotExist:
            logger.error("Vendor does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        else:
            serializer = VendorSerializer(instance, many=True)
            logger.info("Vendor data retrieved successfully.")
            return build_response(instance.count(), "Success", serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a vendor and its related data (attachments, and addresses).
        """
        try:
            pk = kwargs.get('pk')
            if not pk:
                logger.error("Primary key not provided in request.")
                return build_response(0, "Primary key not provided", [], status.HTTP_400_BAD_REQUEST)

            # Retrieve the Vendor instance
            vendor = get_object_or_404(Vendor, pk=pk)
            vendor_serializer = VendorSerializer(vendor)

            # Retrieve related data
            attachments_data = self.get_related_data(VendorAttachment, VendorAttachmentSerializer, 'vendor_id', pk)
            addresses_data = self.get_related_data(VendorAddress, VendorAddressSerializer, 'vendor_id', pk)

            # Customizing the response data
            custom_data = {
                "vendor": vendor_serializer.data,
                "vendor_attachments": attachments_data,
                "vendor_addresses": addresses_data
            }
            logger.info("Vendor and related data retrieved successfully.")
            return build_response(1, "Success", custom_data, status.HTTP_200_OK)

        except Http404:
            logger.error("Vendor with pk %s does not exist.", pk)
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("An error occurred while retrieving vendor with pk %s: %s", pk, str(e))
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
        Handles the deletion of a vendor and its related attachments, and addresses.
        """
        try:
            # Get the SaleOrder instance
            instance = Vendor.objects.get(pk=pk)

            # Delete the main SaleOrder instance
            instance.delete()

            logger.info(f"Vendor with ID {pk} deleted successfully.")
            return build_response(1, "Record deleted successfully", [], status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            logger.warning(f"Vendor with ID {pk} does not exist.")
            return build_response(0, "Record does not exist", [], status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting Vendor with ID {pk}: {str(e)}")
            return build_response(0, "Record deletion failed due to an error", [], status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Handling POST requests for creating
    def post(self, request, *args, **kwargs):   #To avoid the error this method should be written [error : "detail": "Method \"POST\" not allowed."]
        return self.create(request, *args, **kwargs)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Handles the creation of vendor, vendor attachments, and vendor addresses.
        vendor , vendor attachments and vendor addresses are mandatory.
        """
        given_data = request.data

        # Extracting data from the request
        vendors_data = given_data.pop('vendor_data', None)
        vendor_attachments_data = given_data.pop('vendor_attachments', None)
        vendor_addresses_data = given_data.pop('vendor_addresses', None)

        # Ensure mandatory vendor data is present
        if not vendors_data or not vendor_attachments_data or not vendor_addresses_data:
            logger.error("Vendor data , vendor_attachments_data and vendor_addresses_data are mandatory but not provided.")
            return build_response(0, "Vendor data , vendor_attachments_data and vendor_addresses_data are mandatory", [], status.HTTP_400_BAD_REQUEST)

        response_data = {}
        errors = []

        try:
            # Create vendor
            vendor_data = self.create_vendor(vendors_data)
            if not vendor_data:
                logger.error("Vendor creation failed.")
                return build_response(0, "Vendor creation failed", [], status.HTTP_400_BAD_REQUEST)

            vendor_id = vendor_data.get('vendor_id')
            self.add_vendor_id_to_attachments(vendor_attachments_data, vendor_id)
            self.add_vendor_id_to_addresses(vendor_addresses_data, vendor_id)
 
            # Create Vendor Attachment
            attachments_data, attachments_errors = create_multi_instance(vendor_attachments_data, VendorAttachmentSerializer)
            if not attachments_data:
                logger.error("Vendor Attachment creation failed.")
                return build_response(0, "Vendor Attachment creation failed", [], status.HTTP_400_BAD_REQUEST, attachments_errors)

             # Create Vendor Address
            addresses_data, addresses_errors = create_multi_instance(vendor_addresses_data, VendorAddressSerializer)
            if not addresses_data:
                logger.error("Vendor Address creation failed.")
                return build_response(0, "Vendor Address creation failed", [], status.HTTP_400_BAD_REQUEST, addresses_errors)

            response_data = [
                {"vendor_data": vendor_data},
                {"vendor_attachments": attachments_data},
                {"vendor_addresses":addresses_data}
            ]
            error = attachments_errors + addresses_errors
            errors.extend(error)

            if errors:
                logger.warning("Record created with some errors: %s", errors)
                return build_response(1, "Record created with errors", response_data, status.HTTP_201_CREATED, errors)

            logger.info("Record created successfully.")
            return build_response(1, "Record created successfully", response_data, status.HTTP_201_CREATED)

        except Exception as e:
            logger.error("Error creating vendor: %s", str(e))
            return build_response(0, "Record creation failed due to an error", [], status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_vendor(self, vendors_data):
        """
        Creates a vendor in the database.
        """
        serializer = VendorSerializer(data=vendors_data)
        try:
            serializer.is_valid(raise_exception=True)  # Validate vendor data
            serializer.save()  # Save valid vendor to the database
            logger.debug("Vendor created with data: %s", serializer.data)
            return serializer.data
        except ValidationError as e:
            logger.error("Validation error on vendor: %s", str(e))  # Log validation error
            return None
        
    def add_vendor_id_to_attachments(self, vendor_attachments_data, vendor_id):
        """
        Adds the vendor_id to each attachments in the vendor_attachments_data list.
        """
        update_ordereddicts_with_ids(vendor_attachments_data, 'vendor_id', vendor_id)

    def add_vendor_id_to_addresses(self, vendor_addresses_data, vendor_id):
        """
        Adds the vendor_id to each addresses in the vendor_addresses_data list.
        """
        update_ordereddicts_with_ids(vendor_addresses_data, 'vendor_id', vendor_id)
        

    def put(self, request, pk, *args, **kwargs):
        vendors_data = attachments_data = addresses_data =  response_data = None
        errors = []

        partial = kwargs.pop('partial', False)
        instance = self.get_object(pk)
        serializer = VendorSerializer(instance, data=request.data['vendor_data'], partial=partial)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        except Exception as e:
            logger.error("Validation error: %s", str(e))  # Log validation errors
            errors.append(str(e))  # Collect validation errors
        else:
            vendors_data = serializer.data

            # Update vendor_attachments
            vendor_attachments_data = request.data.pop('vendor_attachments')
            attachments_data, attachments_errors= update_multi_instance(pk, vendor_attachments_data, VendorAttachment, VendorAttachmentSerializer, filter_field_1='vendor_id')
            errors.extend(attachments_errors)

            # Update vendor_addresses
            vendor_addresses_data = request.data.pop('vendor_addresses')
            addresses_data, addresses_errors= update_multi_instance(pk, vendor_addresses_data, VendorAddress, VendorAddressSerializer, filter_field_1='vendor_id')
            errors.extend(addresses_errors)
            if errors:
                logger.warning("Record created with some errors: %s", errors)
                return build_response(1, "Record created with errors", response_data, status.HTTP_201_CREATED, errors)

        #  Here 'or' operator is used becaused data can be either empty list or filled with data. so that all the model data can be represented on output
        if vendors_data or attachments_data or addresses_data :  
            custom_data = {
                "vendor_data": vendors_data,
                "vendor_attachments": attachments_data,
                "vendor_addresses":addresses_data
            }
            response_data = build_response(1, "Record updated successfully", custom_data, status.HTTP_200_OK)
        else:
            logger.error("Error in VendorViewSet")
            response_data = build_response(0, "Record updation failed", [serializer.errors], status.HTTP_400_BAD_REQUEST)
        
        return response_data