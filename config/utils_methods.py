#utils_methods file
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

def list_all_objects(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    serializer = self.get_serializer(queryset, many=True)
    message = "NO RECORDS INSERTED" if not serializer.data else None
    response_data = {
        'count': queryset.count(),
        'msg': message,
        'data': serializer.data
    }
    return Response(response_data)

def create_instance(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': True,
            'message': 'Record created successfully',
            'data': serializer.data
        })
    else:
        return Response({
            'status': False,
            'message': 'Form validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

def update_instance(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response({
        'status': True,
        'message': 'Update successful',
        'data': serializer.data,
    })

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

##---------- ONE API - MULTIPLE API CALLS (CRUD OPERATIONS) ---------------
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

def delete_multi_instance(del_value,main_model_name,current_model_name,main_model_field_name=None):
    # main model PK Field name
    main_model_pk_field_name = main_model_name._meta.pk.name

    # Arrange arguments to filter
    if main_model_field_name is not None: # use external value if provided
        filter_kwargs = {main_model_field_name: del_value}
    else:
        filter_kwargs = {main_model_pk_field_name: del_value}
        
    deleted_count, _ = current_model_name.objects.filter(**filter_kwargs).delete()

    if deleted_count > 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({f'***error: {current_model_name} not found or already deleted.***'})            