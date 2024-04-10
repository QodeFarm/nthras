from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.

class LedgerGroupsViews(viewsets.ModelViewSet):
    queryset = LedgerGroups.objects.all()
    serializer_class = LedgerGroupsSerializer

class FirmStatusesViews(viewsets.ModelViewSet):
    queryset = FirmStatuses.objects.all()
    serializer_class = FirmStatusesSerializers
    
class TerritoryViews(viewsets.ModelViewSet):
    queryset = Territory.objects.all()
    serializer_class = TerritorySerializers
    
class CustomerCategoriesViews(viewsets.ModelViewSet):
    queryset = CustomerCategories.objects.all()
    serializer_class = CustomerCategoriesSerializers

class GstCategoriesViews(viewsets.ModelViewSet):
    queryset = GstCategories.objects.all()
    serializer_class = GstCategoriesSerializers
    
class CustomerPaymentTermsViews(viewsets.ModelViewSet):
    queryset = CustomerPaymentTerms.objects.all()
    serializer_class = CustomerPaymentTermsSerializers
    
class PriceCategoriesViews(viewsets.ModelViewSet):
    queryset = PriceCategories.objects.all()
    serializer_class = PriceCategoriesSerializers

class TransportersViews(viewsets.ModelViewSet):
    queryset = Transporters.objects.all()
    serializer_class = TransportersSerializers