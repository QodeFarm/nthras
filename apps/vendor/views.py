from django.shortcuts import render
from rest_framework import viewsets

from apps.vendor.filters import *

# from apps.vendor.filters import VendorFilter
from .models import Vendor, VendorCategory, VendorPaymentTerms, VendorAgent, VendorAttachment, VendorAddress
from .serializers import VendorSerializer, VendorCategorySerializer, VendorPaymentTermsSerializer, VendorAgentSerializer, VendorAttachmentSerializer, VendorAddressSerializer
from utils_methods import list_all_objects,create_instance,update_instance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
# Create your views here.

class VendorsView(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = VendorFlter
    ordering_fields = ['name','code']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class VendorCategoryView(viewsets.ModelViewSet):
    queryset = VendorCategory.objects.all()
    serializer_class = VendorCategorySerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = VendorCategoryFilter
    ordering_fields = ['name']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class VendorPaymentTermsView(viewsets.ModelViewSet):
    queryset = VendorPaymentTerms.objects.all()
    serializer_class = VendorPaymentTermsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = VendorPaymentTermsFlter
    ordering_fields = ['name','code']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)    

class VendorAgentView(viewsets.ModelViewSet):
    queryset = VendorAgent.objects.all()
    serializer_class = VendorAgentSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = VendorAgentFlter
    ordering_fields = ['name','code']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class VendorAttachmentView(viewsets.ModelViewSet):
    queryset = VendorAttachment.objects.all()
    serializer_class = VendorAttachmentSerializer   
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = VendorAttachmentFilter
    ordering_fields = ['attachment_name','vendor_id']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class VendorAddressView(viewsets.ModelViewSet):
    queryset = VendorAddress.objects.all()
    serializer_class = VendorAddressSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = VendorAddressFilter
    ordering_fields = ['address_type','country_id','city_id','state_id']  

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
