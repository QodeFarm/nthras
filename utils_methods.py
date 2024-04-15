#utils_methods file
from rest_framework import status
from rest_framework.response import Response
import base64
from django.db import models

#functions for demonstration purposes
def encrypt(text):
    # Encode the text using base64
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    encrypted_text = encoded_bytes.decode("utf-8")
    return encrypted_text

def decrypt(encrypted_text):
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
