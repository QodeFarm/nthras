from django_filters import rest_framework as filters, FilterSet, CharFilter, NumberFilter
import datetime
from django.utils import timezone
from .models import BrandSalesman

class ProductTypesFilter(FilterSet):
    type_name = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()

class ProductUniqueQuantityCodesFilter(FilterSet):
    quantity_code_name = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()
	
class UnitOptionsFilter(FilterSet):
    unit_name = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()
	
class ProductDrugTypesFilter(FilterSet):
    drug_type_name = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()
	
class ProductItemTypeFilter(FilterSet):
    item_name = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()
	
class BrandSalesmanFilter(FilterSet):
    code = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    rate_on = filters.ChoiceFilter(choices=BrandSalesman.RATE_ON_CHOICES, field_name='rate_on')
    created_at = filters.DateFromToRangeFilter()

class ProductBrandsFilter(FilterSet):
    brand_name = filters.CharFilter(lookup_expr='icontains')
    code = filters.CharFilter(lookup_expr='icontains')
    brand_salesman_id = filters.NumberFilter()
    name = CharFilter(field_name='brand_salesman_id__name', lookup_expr='exact')
    created_at = filters.DateFromToRangeFilter()
