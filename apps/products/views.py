from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.
class ProductGroupsViewSet(viewsets.ModelViewSet):
    queryset = ProductGroups.objects.all()
    serializer_class = ProductGroupsSerializer

class ProductCategoriesViewSet(viewsets.ModelViewSet):
    queryset = ProductCategories.objects.all()
    serializer_class = ProductCategoriesSerializer

class ProductStockUnitsViewSet(viewsets.ModelViewSet):
    queryset = ProductStockUnits.objects.all()
    serializer_class = ProductStockUnitsSerializer
	
class ProductGstClassificationsViewSet(viewsets.ModelViewSet):
    queryset = ProductGstClassifications.objects.all()
    serializer_class = ProductGstClassificationsSerializer

class ProductSalesGlViewSet(viewsets.ModelViewSet):
    queryset = ProductSalesGl.objects.all()
    serializer_class = ProductSalesGlSerializer
	
class ProductPurchaseGlViewSet(viewsets.ModelViewSet):
    queryset = ProductPurchaseGl.objects.all()
    serializer_class = ProductPurchaseGlSerializer
		
class productsViewSet(viewsets.ModelViewSet):
    queryset = products.objects.all()
    serializer_class = productsSerializer