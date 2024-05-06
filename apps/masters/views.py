from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from utils_methods import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import *

# Create your views here.
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)


class StatusesViewset(viewsets.ModelViewSet):
    queryset = Statuses.objects.all()
    serializer_class = StatusesSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class LedgerGroupsViews(viewsets.ModelViewSet):
    queryset = LedgerGroups.objects.all()
    serializer_class = LedgerGroupsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = LedgerGroupsFilters
    ordering_fields = ['name', 'created_at', 'updated_at']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class FirmStatusesViews(viewsets.ModelViewSet):
    queryset = FirmStatuses.objects.all()
    serializer_class = FirmStatusesSerializers
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = FirmStatusesFilters
    ordering_fields = ['name', 'created_at', 'updated_at']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class TerritoryViews(viewsets.ModelViewSet):
    queryset = Territory.objects.all()
    serializer_class = TerritorySerializers
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = TerritoryFilters
    ordering_fields = ['name', 'created_at', 'updated_at']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class CustomerCategoriesViews(viewsets.ModelViewSet):
    queryset = CustomerCategories.objects.all()
    serializer_class = CustomerCategoriesSerializers
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = CustomerCategoriesFilters
    ordering_fields = ['name', 'created_at', 'updated_at']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class GstCategoriesViews(viewsets.ModelViewSet):
    queryset = GstCategories.objects.all()
    serializer_class = GstCategoriesSerializers
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = GstCategoriesFilters
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

  
class CustomerPaymentTermsViews(viewsets.ModelViewSet):
    queryset = CustomerPaymentTerms.objects.all()
    serializer_class = CustomerPaymentTermsSerializers
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = CustomerPaymentTermsFilters
    ordering_fields = ['name', 'created_at', 'updated_at']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
 

class PriceCategoriesViews(viewsets.ModelViewSet):
    queryset = PriceCategories.objects.all()
    serializer_class = PriceCategoriesSerializers
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = PriceCategoriesFilters
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)


class TransportersViews(viewsets.ModelViewSet):
    queryset = Transporters.objects.all()
    serializer_class = TransportersSerializers
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = TransportersFilters
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class ProductTypesViewSet(viewsets.ModelViewSet):
    queryset = ProductTypes.objects.all()
    serializer_class = ProductTypesSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = ProductTypesFilter
    ordering_fields = ['type_name']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
	
class ProductUniqueQuantityCodesViewSet(viewsets.ModelViewSet):
    queryset = ProductUniqueQuantityCodes.objects.all()
    serializer_class = ProductUniqueQuantityCodesSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = ProductUniqueQuantityCodesFilter
    ordering_fields = ['quantity_code_name']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
	
class UnitOptionsViewSet(viewsets.ModelViewSet):
    queryset = UnitOptions.objects.all()
    serializer_class = UnitOptionsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = UnitOptionsFilter
    ordering_fields = ['unit_name']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class ProductDrugTypesViewSet(viewsets.ModelViewSet):
    queryset = ProductDrugTypes.objects.all()
    serializer_class = ProductDrugTypesSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = ProductDrugTypesFilter
    ordering_fields = ['drug_type_name']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class ProductItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductItemType.objects.all()
    serializer_class = ProductItemTypeSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = ProductItemTypeFilter
    ordering_fields = ['item_name']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
	
class BrandSalesmanViewSet(viewsets.ModelViewSet):
    queryset = BrandSalesman.objects.all()
    serializer_class = BrandSalesmanSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = BrandSalesmanFilter
    ordering_fields = ['code','name']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
	
class ProductBrandsViewSet(viewsets.ModelViewSet):
    queryset = ProductBrands.objects.all()
    serializer_class = ProductBrandsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = ProductBrandsFilter
    ordering_fields = ['brand_name','code','brand_salesman_id']

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class PurchaseTypesViewSet(viewsets.ModelViewSet):
    queryset = PurchaseTypes.objects.all()
    serializer_class = PurchaseTypesSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class ShippingCompaniesView(viewsets.ModelViewSet):
    queryset = ShippingCompanies.objects.all()
    serializer_class = ShippingCompaniesSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)


class SaleTypesView(viewsets.ModelViewSet):
    queryset = SaleTypes.objects.all()
    serializer_class = SaleTypesSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class GstTypesView(viewsets.ModelViewSet):
    queryset = GstTypes.objects.all()
    serializer_class = GstTypesSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class ShippingModesView(viewsets.ModelViewSet):
    queryset = ShippingModes.objects.all()
    serializer_class = ShippingModesSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)