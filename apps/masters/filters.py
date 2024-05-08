from django_filters import rest_framework as filters, FilterSet, CharFilter, NumberFilter
import datetime
from django.utils import timezone
from .models import BrandSalesman

class LedgerGroupsFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    under_group = filters.CharFilter(lookup_expr='exact')
    nature = filters.CharFilter(lookup_expr='exact')

class FirmStatusesFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

class TerritoryFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    code = filters.CharFilter(lookup_expr='exact')

class CustomerCategoriesFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    code = filters.CharFilter(lookup_expr='exact')

class GstCategoriesFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

class CustomerPaymentTermsFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    code = filters.CharFilter(lookup_expr='exact')
    fixed_days = filters.NumberFilter(lookup_expr='exact')
    no_of_fixed_days = filters.RangeFilter(lookup_expr='exact')
    payment_cycle = filters.CharFilter(lookup_expr='icontains')
    run_on = filters.CharFilter(lookup_expr='icontains')      
    
class PriceCategoriesFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    code = filters.CharFilter(lookup_expr='exact')
    
class TransportersFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    code = filters.CharFilter(lookup_expr='exact')
    gst_no = filters.CharFilter(lookup_expr='exact')



class ProductTypesFilter(FilterSet):
    type_name = filters.CharFilter(lookup_expr='icontains')

class ProductUniqueQuantityCodesFilter(FilterSet):
    quantity_code_name = filters.CharFilter(lookup_expr='icontains')
	
class UnitOptionsFilter(FilterSet):
    unit_name = filters.CharFilter(lookup_expr='icontains')
	
class ProductDrugTypesFilter(FilterSet):
    drug_type_name = filters.CharFilter(lookup_expr='icontains')
	
class ProductItemTypeFilter(FilterSet):
    item_name = filters.CharFilter(lookup_expr='icontains')
	
class BrandSalesmanFilter(FilterSet):
    code = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    rate_on = filters.ChoiceFilter(choices=BrandSalesman.RATE_ON_CHOICES, field_name='rate_on')

class ProductBrandsFilter(FilterSet):
    brand_name = filters.CharFilter(lookup_expr='icontains')
    code = filters.CharFilter(lookup_expr='icontains')
    brand_salesman_id = filters.NumberFilter()
    name = CharFilter(field_name='brand_salesman_id__name', lookup_expr='exact')


class PurchaseTypesFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
