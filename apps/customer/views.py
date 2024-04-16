from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from utils_methods import list_all_objects, create_instance, update_instance

# Create your views here.

class LedgerAccountsViews(viewsets.ModelViewSet):
    queryset = LedgerAccounts.objects.all()
    serializer_class = LedgerAccountsSerializers

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class CustomerViews(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
    
class CustomerAddressesViews(viewsets.ModelViewSet):
    queryset = CustomerAddresses.objects.all()
    serializer_class = CustomerAddressesSerializers

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class CustomerAttachmentsViews(viewsets.ModelViewSet):
    queryset = CustomerAttachments.objects.all()
    serializer_class = CustomerAttachmentsSerializers
    
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)