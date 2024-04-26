from django_filters import rest_framework as filters, FilterSet, CharFilter, NumberFilter, RangeFilter,BooleanFilter
from apps.company.models import Companies
from apps.company.models import Companies
from django.db.models import Max,Sum,Count
import datetime
from django.utils import timezone
from django.db.models import Avg, Max, Min, Count, Sum
import django_filters

class CompanyFilter(FilterSet):
    city_name = CharFilter(field_name='city_id__city_name', lookup_expr='exact')
    state_name = CharFilter(field_name='city_id__state_id__state_name', lookup_expr='exact')
    country_name = CharFilter(field_name='city_id__state_id__country_id__country_name', lookup_expr='exact')
    city = filters.CharFilter(method='filter_by_cities')
    state = filters.CharFilter(method='filter_by_states')
    country = filters.CharFilter(method='filter_by_countries')
    name = filters.CharFilter(lookup_expr='exact')
    name_icontains = filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_startswith = filters.CharFilter(field_name='name', lookup_expr='startswith')
    name_endswith = filters.CharFilter(field_name='name', lookup_expr='endswith')
    print_name = filters.CharFilter(lookup_expr='icontains')
    short_name = filters.CharFilter(lookup_expr='icontains')
    code = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')
    pin_code = filters.CharFilter(lookup_expr='exact')
    phone = filters.CharFilter(lookup_expr='exact')
    email = filters.CharFilter(lookup_expr='exact')
    print_address = filters.CharFilter(lookup_expr='icontains')
    pan = filters.CharFilter(lookup_expr='exact')
    tan = filters.CharFilter(lookup_expr='exact')
    cin = filters.CharFilter(lookup_expr='exact')
    gst_tin = filters.CharFilter(lookup_expr='exact')
    establishment_code = filters.CharFilter(lookup_expr='exact')
    esi_no = filters.CharFilter(lookup_expr='exact')
    pf_no = filters.CharFilter(lookup_expr='exact')
    authorized_person = filters.CharFilter(lookup_expr='icontains')
    iec_code = filters.CharFilter(lookup_expr='exact')
    eway_username = filters.CharFilter(lookup_expr='icontains')
    gstn_username = filters.CharFilter(lookup_expr='icontains')

    # Numerical filters
    num_branches = filters.NumberFilter()
    num_employees = filters.NumberFilter()
    num_employees_gte = NumberFilter(field_name='num_employees', lookup_expr='gte')
    num_employees_lte = NumberFilter(field_name='num_employees', lookup_expr='lte')
    num_branches_range = RangeFilter(field_name='num_branches')
    company_id_start = filters.NumberFilter(field_name='company_id', lookup_expr='gte')
    company_id_end = filters.NumberFilter(field_name='company_id', lookup_expr='lte')
    num_branches_start = filters.NumberFilter(field_name='num_branches', lookup_expr='gte')
    num_branches_end = filters.NumberFilter(field_name='num_branches', lookup_expr='lte')

    # Boolean filters
    turnover_less_than_5cr = filters.BooleanFilter()

    # Choice-based filters
    vat_gst_status = filters.MultipleChoiceFilter(choices=Companies.VAT_GST_STATUS_CHOICES, field_name='vat_gst_status')
    gst_type = filters.MultipleChoiceFilter(choices=Companies.GST_TYPE_CHOICES, field_name='gst_type')

    #Dates
    created_at_from = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_to = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte', method='filter_created_at_to')
    updated_at_from = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_at_to = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte', method='filter_updated_at_to')
    updated_within_days = NumberFilter(method='filter_recently_updated')
    created_within_days = NumberFilter(method='filter_recently_created')

    #aggregations
    max_num_employees = django_filters.BooleanFilter(method='get_max_num_employees')
    min_num_employees = django_filters.BooleanFilter(method='get_min_num_employees')
    companies_per_city = django_filters.CharFilter(method='get_companies_per_city')
    sum_employees_per_country = django_filters.CharFilter(method='get_sum_employees_per_country')

    def filter_by_cities(self, queryset, name, value):
        cities = value.split(',')
        return queryset.filter(city_id__city_name__in=cities)
    
    def filter_by_states(self, queryset, name, value):
        states = value.split(',')
        return queryset.filter(city_id__state_id__state_name__in=states)

    def filter_by_countries(self, queryset, name, value):
        countries = value.split(',')
        return queryset.filter(city_id__state_id__country_id__country_name__in=countries)
    
    def filter_created_at_to(self, queryset, name, value):
        if value:
            if isinstance(value, datetime.date):  # Check if the value is a date
                value = datetime.datetime.combine(value, datetime.time.max)
            return queryset.filter(created_at__lte=value)
        return queryset
    
    def filter_updated_at_to(self, queryset, name, value):
        if value:
            if isinstance(value, datetime.date):  # Check if the value is a date
                value = datetime.datetime.combine(value, datetime.time.max)
            return queryset.filter(updated_at__lte=value)
        return queryset

    def filter_recently_updated(self, queryset, name, value):
        try:
            # Convert the value to an integer before subtracting days
            days = int(value)
            comparison_date = timezone.now() - datetime.timedelta(days=days)
            return queryset.filter(updated_at__gte=comparison_date)
        except (ValueError, TypeError):
            # If conversion fails, return the queryset unchanged or handle as appropriate
            return queryset
        
    def filter_recently_created(self, queryset, name, value):
        try:
            days = int(value)
            comparison_date = timezone.now() - datetime.timedelta(days=days)
            return queryset.filter(created_at__gte=comparison_date)
        except (ValueError, TypeError):
            return queryset

    def get_max_num_employees(self, queryset, name, value):
        if value:
            return queryset.aggregate(Max('num_employees'))
        return queryset

    def get_min_num_employees(self, queryset, name, value):
        if value:
            return queryset.aggregate(Min('num_employees'))
        return queryset
    
    def get_companies_per_city(self, queryset, name, value):
        return queryset.filter(city_id__city_name=value).aggregate(company_count=Count('id'))

    def get_sum_employees_per_country(self, queryset, name, value):
        return queryset.filter(city_id__state_id__country_id__country_name=value).aggregate(total_employees=Sum('num_employees'))
