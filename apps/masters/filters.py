from django_filters import rest_framework as filters

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