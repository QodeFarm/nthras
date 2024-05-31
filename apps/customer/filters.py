from django_filters import rest_framework as filters
import uuid
from django.db.models import Q
from utils_methods import filter_uuid

class LedgerAccountsFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    type = filters.CharFilter(lookup_expr='exact')
    ledger_group_id = filters.CharFilter(field_name='ledger_group_id__name', lookup_expr='exact')
    account_no = filters.CharFilter(lookup_expr='exact')
    pan = filters.CharFilter(lookup_expr='exact')

class CustomerFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    identification = filters.CharFilter(lookup_expr='exact')
    contact_person = filters.CharFilter(lookup_expr='exact')
    cin = filters.CharFilter(lookup_expr='exact')
    pan = filters.CharFilter(lookup_expr='exact')
    tax_type = filters.CharFilter(lookup_expr='exact')
    ledger_account_id = filters.CharFilter(field_name='ledger_account_id__name', lookup_expr='exact')
    gst_category_id = filters.CharFilter(field_name='gst_category_id__name', lookup_expr='exact')
    max_credit_days = filters.RangeFilter(lookup_expr='exact')
    
class CustomerAttachmentsFilters(filters.FilterSet):
    customer_id = filters.CharFilter(field_name='customer_id__name', lookup_expr='exact')
    attachment_name = filters.CharFilter(lookup_expr='exact')

class CustomerAddressesFilters(filters.FilterSet):
    customer_id = filters.CharFilter(method=filter_uuid)
    city_id = filters.CharFilter(field_name='city_id__city_name', lookup_expr='exact')
    state_id = filters.CharFilter(field_name='state_id__state_name', lookup_expr='exact')
    country_id = filters.CharFilter(field_name='country_id__country_name', lookup_expr='exact')
    pin_code = filters.CharFilter(lookup_expr='exact')
    phone = filters.CharFilter(lookup_expr='exact')
    email = filters.CharFilter(lookup_expr='exact')

    def filter_customer_id(self, queryset, name, value):
        try:
            uuid.UUID(value)
        except ValueError:
            # If the UUID is invalid, return an empty queryset
            return queryset.none()
        return queryset.filter(Q(bank_detail_id=value))