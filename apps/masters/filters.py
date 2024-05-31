from django_filters import rest_framework as filters, FilterSet, CharFilter, NumberFilter
import datetime
from django.utils import timezone
from .models import BrandSalesman,Country, State, City
import django_filters

class CountryFilters(django_filters.FilterSet):
    country_name = django_filters.CharFilter(field_name='country_name', lookup_expr='icontains')
    country_code = django_filters.CharFilter(field_name='country_code', lookup_expr='exact')

    class Meta:
        model = Country
        fields = ['country_name', 'country_code']

class StateFilters(django_filters.FilterSet):
    state_name = django_filters.CharFilter(field_name='state_name', lookup_expr='icontains')
    state_code = django_filters.CharFilter(field_name='state_code', lookup_expr='exact')
    country_name = django_filters.CharFilter(field_name='country_id__country_name', lookup_expr='icontains')

    class Meta:
        model = State
        fields = ['state_name', 'state_code', 'country_name']

class CityFilters(django_filters.FilterSet):
    city_name = django_filters.CharFilter(field_name='city_name', lookup_expr='icontains')
    city_code = django_filters.CharFilter(field_name='city_code', lookup_expr='exact')
    state_name = django_filters.CharFilter(field_name='state_id__state_name', lookup_expr='icontains')
    country_name = django_filters.CharFilter(field_name='state_id__country_id__country_name', lookup_expr='icontains')

    class Meta:
        model = City
        fields = ['city_name', 'city_code', 'state_name', 'country_name']


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


