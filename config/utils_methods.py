#utils_methods file
import logging
from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.db import models
import uuid,django_filters
from django.db.models import Q
from uuid import uuid4
import base64
import os
import json
from django.utils import timezone
from django.db import models
from django.core.cache import cache


# Get an instance of a logger
logger = logging.getLogger(__name__)

# -------------- File Path Handler (for Vendor model only)----------------------
def custom_upload_to(instance, filename):
    file_extension = filename.split('.')[-1]
    unique_id = uuid4().hex[:7]  # Generate a unique ID (e.g., using UUID)
    new_filename = f"{unique_id}_{filename}"
    new_filename = new_filename.replace(' ', '_')
    return os.path.join('vendor', str(instance.name), new_filename)
# ---------------------------------------------------------

#functions for demonstration purposes
def encrypt(text):
    if text is None:
        return None
    # Encode the text using base64
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    encrypted_text = encoded_bytes.decode("utf-8")
    return encrypted_text

def decrypt(encrypted_text):
    if encrypted_text is None:
        return None
    # Decode the text using base64
    decoded_bytes = base64.b64decode(encrypted_text.encode("utf-8"))
    decrypted_text = decoded_bytes.decode("utf-8")
    return decrypted_text

class EncryptedTextField(models.TextField):
    """
    A custom field to store encrypted text.
    """
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            # Attempt to decrypt the value
            return decrypt(value)
        except Exception as e:
            # Handle decryption errors gracefully
            print("Error decrypting value:", e)
            return None
        # Implement decryption logic here
        return decrypt(value)

    def to_python(self, value):
        if isinstance(value, str):
            # Implement decryption logic here
            return decrypt(value)
        return value
 
    def get_prep_value(self, value):
        # Implement encryption logic here
        return encrypt(value)


#If you want to decrypt then you can uncomment this and run... in output you will find the decrypted account number 
# # Encoded account number
encoded_account_number = ""

# Decode from base64
decoded_bytes = base64.b64decode(encoded_account_number)

# Convert bytes to string
original_account_number = decoded_bytes.decode("utf-8")

#=======================Filters for primary key===============================================
def filter_uuid(queryset, name, value):
    try:
        uuid.UUID(value)
    except ValueError:
        return queryset.none()
    return queryset.filter(Q(**{name: value}))
#======================================================================

def build_response(count, msg, data, status):
    return Response({
        'count':count,
        'message': msg,
        'data': data,
    },status=status) 

def list_all_objects(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    serializer = self.get_serializer(queryset, many=True)
    message = "NO RECORDS INSERTED" if not serializer.data else None
    return build_response(queryset.count(), message, serializer.data, status.HTTP_201_CREATED if not serializer.data else status.HTTP_200_OK)

def create_instance(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        return build_response(1, "Record created successfully", data, status.HTTP_201_CREATED)
    else:
        return build_response(0, "Form validation failed", [], status.HTTP_400_BAD_REQUEST)

def update_instance(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    data = serializer.data
    return build_response(1, "Record updated successfully", data, status.HTTP_200_OK)

def perform_update(self, serializer):
    serializer.save()  # Add any custom logic for updating if needed

#==================================================
#Patterns

def generate_order_number(order_type_prefix):
    """
    Generate an order number based on the given prefix and the current date.

    Args:
        order_type_prefix (str): The prefix for the order type.

    Returns:
        str: The generated order number.
    """
    current_date = timezone.now()
    date_str = current_date.strftime('%y%m')

    key = f"{order_type_prefix}-{date_str}"
    sequence_number = cache.get(key, 0)
    sequence_number += 1
    cache.set(key, sequence_number, timeout=None)

    sequence_number_str = f"{sequence_number:05d}"
    order_number = f"{order_type_prefix}-{date_str}-{sequence_number_str}"
    return order_number

class OrderNumberMixin(models.Model):
    order_no_prefix = ''
    order_no_field = ''

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Override the save method to generate and set the order number if it is not already set.
        """
        if not getattr(self, self.order_no_field):
            setattr(self, self.order_no_field, generate_order_number(self.order_no_prefix))
        super().save(*args, **kwargs)
#======================================================================================================
#It removes fields from role_permissions for sending Proper data to frontend team after successfully login
def remove_fields(obj):
    if isinstance(obj, dict):
        obj.pop('created_at', None)
        obj.pop('updated_at', None)
        for value in obj.values():
            remove_fields(value)
    elif isinstance(obj, list):
        for item in obj:
            remove_fields(item)

#====================================== SaleOrder-Requirements ===============================================
# If multiple instances to be updated on same model, at a single time this function helps to update all instances.
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

def create_multi_instance(data_set, serializer_class):
    """
    Creates multiple instances in the database using the provided serializer class.
    Returns a list of created data and a list of any validation errors.
    """
    data_list = []
    errors = []
    for item_data in data_set:
        serializer = serializer_class(data=item_data)
        try:
            serializer.is_valid(raise_exception=True)  # Validate each item
            serializer.save()  # Save each valid item to the database
            data_list.append(serializer.data)
        except ValidationError as e:
            logger.error("Validation error: %s", str(e))  # Log validation errors
            errors.append(str(e))  # Collect validation errors
    return data_list, errors

def build_response(success, message, data, status_code, errors=None):
    """
    Builds a standardized API response.
    """
    response = {
        'success': success,
        'message': message,
        'data': data
    }
    if errors:
        response['errors'] = errors
    return Response(response, status=status_code)

def get_object_or_none(model, **kwargs):
    """
    Fetches a single object from the database or returns None if not found.
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def update_ordereddicts_with_ids(data_list, id_key, id_value):
    """
    Updates dictionaries in a list with a key-value pair.
    """
    for data in data_list:
        data[id_key] = id_value

def delete_multi_instance(del_value, main_model_class, related_model_class, main_model_field_name=None):
    """
    Deletes instances from a related model based on a field value from the main model.

    :param del_value: Value of the main model field to filter related model instances.
    :param main_model_class: The main model class.
    :param related_model_class: The related model class from which to delete instances.
    :param main_model_field_name: The field name in the related model that references the main model.
    """
    try:
        # Get the main model's primary key field name
        main_model_pk_field_name = main_model_class._meta.pk.name

        # Arrange arguments to filter
        filter_kwargs = {main_model_field_name or main_model_pk_field_name: del_value}

        # Delete related instances
        deleted_count, _ = related_model_class.objects.filter(**filter_kwargs).delete()
        logger.info(f"Deleted {deleted_count} instances from {related_model_class.__name__} where {filter_kwargs}.")
    except Exception as e:
        logger.error(f"Error deleting instances from {related_model_class.__name__}: {str(e)}")
        return False
    return True

def update_multi_instance_new(pk, update_data, related_model_class, serializer_name, filter_field_1=None,filter_field_2=None):
    """
    Update instances from a related model based on a field value from the main model.

    :param main_model_class: The main model class.
    :param related_model_class: The related model class from which to delete instances.
    :param main_model_field: The field name in the related model that references the main model.
    """
    try:
        data_list = []
        
        for data in update_data:
            # common to both IF and Else
            field_val_2  = data.get(str(filter_field_2))

            filter_kwargs = {filter_field_1: pk, filter_field_2: field_val_2 }
            print('filter_kwargs= ',filter_kwargs)
            try:
                print('related_model_class>>',related_model_class)
                instance = related_model_class.objects.filter(**filter_kwargs).first()
                print('instance = ',instance)
            except related_model_class.DoesNotExist:
                logger.warning(f"{related_model_class} with ID {pk} does not exist.")
            serializer = serializer_name(instance, data=data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data_list.append(serializer.data)
        return data_list
    except Exception as e:
        logger.error(f"Error updating instances from {related_model_class.__name__}: {str(e)}")
        return None