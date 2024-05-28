import django_filters
from .models import Companies, Branches, BranchBankDetails

class CompaniesFilters(django_filters.FilterSet):
    company_id = django_filters.NumberFilter(field_name='company_id', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = django_filters.CharFilter(field_name='code', lookup_expr='exact')
    num_branches = django_filters.NumberFilter(field_name='num_branches', lookup_expr='exact')
    num_employees = django_filters.RangeFilter(field_name='num_employees')
    
    class Meta:
        model = Companies
        fields = ['company_id','name', 'code', 'num_branches', 'num_employees']

class BranchesFilters(django_filters.FilterSet):
    branch_id = django_filters.NumberFilter(field_name='branch_id', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = django_filters.CharFilter(field_name='code', lookup_expr='exact')
    city = django_filters.CharFilter(field_name='city_id__city_name', lookup_expr='exact')
    state = django_filters.CharFilter(field_name='state_id__state_name', lookup_expr='exact')
    status = django_filters.CharFilter(field_name='status_id__status_name', lookup_expr='exact')
    country = django_filters.CharFilter(field_name='country_id__country_name', lookup_expr='exact')

    class Meta:
        model = Branches
        fields = ['branch_id','name','code','city','state','status','country']

class BranchBankDetailsFilters(django_filters.FilterSet):
    bank_detail_id = django_filters.NumberFilter(field_name='bank_detail_id', lookup_expr='exact')
    bank_name = django_filters.CharFilter(field_name='bank_name', lookup_expr='icontains')
    branch_id = django_filters.NumberFilter(field_name='branch_id', lookup_expr='exact')
    branch_name = django_filters.CharFilter(field_name='bank_name', lookup_expr='icontains')
    class Meta:
        model = BranchBankDetails
        fields = ['bank_detail_id','bank_name', 'branch_id','branch_name']
