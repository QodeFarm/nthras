import datetime
from django.db.models import Value, CharField
from django.utils import timezone
from django_filters import rest_framework as filters, FilterSet, CharFilter, NumberFilter, RangeFilter,BooleanFilter
from apps.company.models import Companies
from django.db.models import Q,Sum,Max,Min
from rest_framework.response import Response
from django.shortcuts import render
import  django_filters
from .models import *

class VendorCategoryFilter(FilterSet): #verified
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = VendorCategory
        fields = ['code','name']

class VendorPaymentTermsFlter(FilterSet): #verified
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = VendorPaymentTerms
        fields = ['code','name']

class VendorAgentFlter(FilterSet): #verified
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    amount_type = filters.ChoiceFilter(choices=VendorAgent.AMOUNT_TYPE_CHOICES, field_name='amount_type')
    rate_on = filters.ChoiceFilter(choices=VendorAgent.RATE_ON_CHOICES, field_name='rate_on')

    class Meta:
        model = VendorAgent
        fields = ['code','name','amount_type','rate_on']

class VendorFlter(FilterSet): #verified
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    gst_no = filters.CharFilter(field_name='gst_no', lookup_expr='icontains')
    contact_person = filters.CharFilter(field_name='contact_person', lookup_expr='icontains')
    cin = filters.CharFilter(field_name='cin', lookup_expr='icontains')
    pan = filters.CharFilter(field_name='pan', lookup_expr='icontains')
    rtgs_ifsc_code = filters.CharFilter(field_name='rtgs_ifsc_code', lookup_expr='icontains')
    bank_name = filters.CharFilter(field_name='bank_name', lookup_expr='icontains')
    branch = filters.CharFilter(field_name='branch', lookup_expr='icontains')

    #Foreign keys
    ledger_account_id = filters.NumberFilter()
    name = CharFilter(field_name='ledger_account_id__name', lookup_expr='exact')

    firm_status_id = filters.NumberFilter()
    name = CharFilter(field_name='firm_status_id__name', lookup_expr='exact')

    territory_id = filters.NumberFilter()
    name = CharFilter(field_name='territory_id__name', lookup_expr='exact')

    vendor_category_id = filters.NumberFilter()
    name = CharFilter(field_name='vendor_category_id__name', lookup_expr='exact')

    gst_category_id = filters.NumberFilter()
    name = CharFilter(field_name='gst_category_id__name', lookup_expr='exact')

    class Meta:
        model = Vendor
        fields = ['code','name','gst_no','contact_person','cin','pan','rtgs_ifsc_code','bank_name','branch']

class VendorAttachmentFilter(FilterSet):
    vendor_id = filters.NumberFilter()
    name = CharFilter(field_name='vendor_id__name', lookup_expr='exact')
    attachment_name = filters.CharFilter(field_name='attachment_name', lookup_expr='icontains')

    class Meta:
        model = VendorAttachment
        fields = ['vendor_id','attachment_name']

class VendorAddressFilter(FilterSet):
    vendor_id = filters.NumberFilter()
    name = CharFilter(field_name='vendor_id__name', lookup_expr='exact')

    address_type = filters.ChoiceFilter(choices=VendorAddress.ADDRESS_TYPE_CHOICES, field_name='address_type')
    address = filters.CharFilter(lookup_expr='icontains')
    pin_code = filters.CharFilter(lookup_expr='exact')
    phone = filters.CharFilter(lookup_expr='exact')
    email = filters.CharFilter(lookup_expr='exact')

    city_id = filters.NumberFilter()
    city_name = CharFilter(field_name='city_id__city_name', lookup_expr='exact')

    state_id = filters.NumberFilter()
    state_name = CharFilter(field_name='city_id__state_id__state_name', lookup_expr='exact')

    country_id = filters.NumberFilter()
    country_name = CharFilter(field_name='city_id__state_id__country_id__country_name', lookup_expr='exact')

    class Meta:
        model = VendorAddress
        fields = ['vendor_id','name','address_type','address','pin_code','phone','email']
