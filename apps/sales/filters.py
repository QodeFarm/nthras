# from datetime import timedelta, timezone
from datetime import timedelta
from django.utils import timezone
from django_filters import rest_framework as filters
from requests import Response
from .models import SaleOrder,Invoices,PaymentTransactions,OrderItems,Shipments,SalesPriceList,SaleOrderReturns
import django_filters

class SaleOrderFilter(filters.FilterSet):
    order_date = filters.DateFromToRangeFilter()
    delivery_date = filters.DateFromToRangeFilter()
    created_at = filters.DateFromToRangeFilter()
    order_no = filters.CharFilter(lookup_expr='icontains')
    customer_id = filters.NumberFilter()
    order_id = filters.NumberFilter()
    remarks = filters.CharFilter(lookup_expr='icontains')
    customer_name = filters.CharFilter(field_name='customer_id__name', lookup_expr='icontains')
    sale_type_id = filters.NumberFilter()
    sales_type_name = filters.CharFilter(field_name='sale_type_id__name', lookup_expr='icontains')
    item_value = filters.RangeFilter()
    advance_amount = filters.RangeFilter()
    doc_amount = filters.RangeFilter()

    
    last_six_orders_for_customer = filters.NumberFilter(method='get_last_six_orders')


        # if last_six_months is None:
        #     print('Last Six Months Executed')
        #     six_months_ago = timezone.now() - timedelta(days=6*30)  # Roughly six months
        #     queryset = queryset.filter(order_date__gte=six_months_ago)
        #     return queryset
 
    # http://127.0.0.1:8000/api/v1/sales/sale_order/?last_six_orders_for_customer=2
    # http://127.0.0.1:8000/api/v1/sales/sale_order/?last_six_orders_for_customer=2&limit=3
    # http://127.0.0.1:8000/api/v1/sales/sale_order/?last_six_orders_for_customer=1&months=7
    def get_last_six_orders(self, queryset, name,value,months=None,limit=None,year=None):  #limit is type(int)
        limit = self.request.query_params.get('limit',None)  # limited = no of orders
        year = self.request.query_params.get('year',None)
        months = self.request.query_params.get('months',None)

        if limit:
            print('Limit is Executed')
            limit = int(limit)
            # Filter by customer_id and limit the number of results
            return queryset.filter(customer_id=value).order_by('-order_date')[:limit]
        
        if year:
            print('Year is Executed')
            # Filter by year & customer ID
            queryset =  queryset.filter(order_date__year=year)
            queryset = queryset.filter(customer_id=value)
            return queryset
        
        if months:
            print('Last Six Months Executed')
            month = int(months)
            six_months_ago = timezone.now() - timedelta(days=month*30)
            queryset = queryset.filter(customer_id=value)
            queryset = queryset.filter(order_date__gte=six_months_ago)
            return queryset
        
        else: #only customer ID
            print('Else is workng')
            return queryset.filter(customer_id=value).order_by('-order_date')

    
    class Meta:
        model = SaleOrder
        fields =['customer_id']

class InvoicesFilter(filters.FilterSet):
    invoice_date = filters.DateFilter()            
    due_date = filters.DateFromToRangeFilter()     
    status = filters.CharFilter(lookup_expr='icontains')
    total_amount = filters.RangeFilter()          
    sale_type_id = filters.NumberFilter()
    sales_type_name = filters.CharFilter(field_name='sale_type_id__name', lookup_expr='icontains')
    warehouse_id = filters.NumberFilter()
    warehouse_name = filters.CharFilter(field_name ='warehouse_id__name', lookup_expr='icontains' )

    class Meta:
        model = Invoices
        fields = ['invoice_date', 'due_date', 'status', 'total_amount']

class PaymentTransactionsFilter(filters.FilterSet):
    payment_date = filters.RangeFilter()
    payment_status =filters.CharFilter(lookup_expr='icontains')
    amount = filters.RangeFilter()

    class Meta:
        model = PaymentTransactions
        fields = ['payment_date', 'payment_status', 'amount']

class OrderItemsFilter(filters.FilterSet):
    order_id = filters.NumberFilter()
    product_id = filters.NumberFilter()
    product_name = filters.CharFilter(field_name='product_id__name',lookup_expr='icontains')
    amount = filters.RangeFilter()
    rate= filters.RangeFilter()
   

    class Meta:
        model = OrderItems
        fields = ['order_id', 'product_id', 'amount','rate']

class ShipmentsFilter(filters.FilterSet):
    shipping_date = filters.DateFilter()
    order_id = filters.NumberFilter()
    shipping_tracking_no = filters.CharFilter(field_name='shipping_tracking_no', lookup_expr='icontains')

    class Meta:
        model = Shipments
        fields = ['shipping_date', 'order_id','shipping_tracking_no']

class SalesPriceListFilter(filters.FilterSet):
    effective_From = filters.DateFilter()
    effective_date = filters.DateFilter()
    effective_range = filters.DateFromToRangeFilter(field_name='effective_From')
    customer_category_id = filters.NumberFilter()
    customer_category_name = filters.CharFilter(field_name='customer_category_id__name',lookup_expr='icontains')
    brand_id = filters.NumberFilter()
    brand_name = filters.CharFilter(field_name='brand_id__name',lookup_expr='icontains')
    # group_id = filters.NumberFilter(field_name='group_id__id')

    class Meta:
        model = SalesPriceList
        fields = ['effective_From', 'effective_date']

class SaleOrderReturnsFilter(filters.FilterSet):
    sales_return_no = filters.CharFilter(lookup_expr='icontains')
    due_date = filters.DateFilter()
    sale_id = filters.NumberFilter()
    class Meta:
        model = SaleOrderReturns
        fields = ['sales_return_no', 'due_date']