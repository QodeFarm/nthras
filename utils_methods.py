#utils_methods file
from rest_framework.response import Response
from rest_framework import status
from django.db import models
import uuid,django_filters
from django.db.models import Q
from uuid import uuid4
import base64
import os

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
# utils_methods.py
import os
import json
from django.utils import timezone

SEQUENCE_FILE_PATH = 'order_sequences.json'

def load_sequences():
    if not os.path.exists(SEQUENCE_FILE_PATH):
        return {}
    with open(SEQUENCE_FILE_PATH, 'r') as file:
        return json.load(file)

def save_sequences(sequences):
    with open(SEQUENCE_FILE_PATH, 'w') as file:
        json.dump(sequences, file)

def generate_order_number(order_type_prefix):
    current_date = timezone.now()
    date_str = current_date.strftime('%d%m')  # Format DDMM
    
    sequences = load_sequences()
    
    # Generate a key for the order type and date
    key = f"{order_type_prefix}-{date_str}"
    
    # Get the current sequence number from the dictionary, default to 0 if not found
    sequence_number = sequences.get(key, 0)
    
    # Increment the sequence number
    sequence_number += 1
    
    # Store the updated sequence number back in the dictionary
    sequences[key] = sequence_number
    save_sequences(sequences)
    
    # Format the sequence number with leading zeros to ensure it is 5 digits
    sequence_number_str = f"{sequence_number:05d}"
    
    # Construct the order number
    order_number = f"{order_type_prefix}-{date_str}-{sequence_number_str}"
    return order_number



class OrderNumberMixin(models.Model):
    order_no_prefix = ''
    order_no_field = 'order_no'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not getattr(self, self.order_no_field):
            setattr(self, self.order_no_field, generate_order_number(self.order_no_prefix))
        super().save(*args, **kwargs)
