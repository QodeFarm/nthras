from datetime import timedelta, timezone
from django_filters import rest_framework as filters
from .models import *
from config.utils_methods import filter_uuid
from rest_framework.decorators import action

class SaleOrderFilter(filters.FilterSet):
    sale_order_id = filters.CharFilter(method=filter_uuid)
    customer_id = filters.CharFilter(method=filter_uuid)
    customer_name = filters.CharFilter(field_name='customer_id__name', lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='exact')
    delivery_date = filters.DateFromToRangeFilter()
    order_date = filters.DateFromToRangeFilter()
    order_no = filters.CharFilter(lookup_expr='icontains')
    ref_no = filters.CharFilter(lookup_expr='icontains')
    ref_date = filters.DateFromToRangeFilter()
    remarks = filters.CharFilter(lookup_expr='icontains')
    sale_type_id = filters.CharFilter(method=filter_uuid)
    sales_type_name = filters.CharFilter(field_name='sale_type_id__name', lookup_expr='icontains')
    advance_amount = filters.RangeFilter()
    item_value = filters.RangeFilter()
    doc_amount = filters.RangeFilter()
    order_status_id = filters.CharFilter(method=filter_uuid)
    status_name = filters.CharFilter(field_name='order_status_id__status_name', lookup_expr='icontains')  
    created_at = filters.DateFromToRangeFilter()

    # # http://127.0.0.1:8000/api/v1/sales/sale_order/?last_six_orders_for_customer=2
    # # http://127.0.0.1:8000/api/v1/sales/sale_order/?last_six_orders_for_customer=2&limit=3
    # # http://127.0.0.1:8000/api/v1/sales/sale_order/?last_six_orders_for_customer=1&months=7
    
    last_six_orders_for_customer = filters.CharFilter(method='get_last_six_orders')
    @action(detail=False, methods=['get'])
    def get_last_six_orders(self, queryset,name,value,months=None,limit=None,year=None):
        limit = self.request.query_params.get('limit',None)  # limited = no of orders
        year = self.request.query_params.get('year',None)
        months = self.request.query_params.get('months',None)

        if limit:
            limit = int(limit)
            # Filter by customer_id and limit the number of results
            return queryset.filter(customer_id=value).order_by('-order_date')[:limit]
        
        if year:
            # Filter by year & customer ID
            queryset =  queryset.filter(order_date__year=year)
            queryset = queryset.filter(customer_id=value)
            return queryset
       
        if months:
            month = int(months)
            six_months_ago = timezone.now() - timedelta(days=month*30)
            queryset = queryset.filter(customer_id=value)
            queryset = queryset.filter(order_date__gte=six_months_ago)
            return queryset
        else:
            return queryset.filter(customer_id=value).order_by('-order_date')

    class Meta:
        model = SaleOrder
        fields =['customer_id']

class SalesPriceListFilter(filters.FilterSet):
    sales_price_list_id = filters.CharFilter(method=filter_uuid)
    customer_category_id = filters.CharFilter(method=filter_uuid)
    customer_category_name = filters.CharFilter(field_name='customer_category_id__name',lookup_expr='icontains')
    brand_id = filters.CharFilter(method=filter_uuid)
    brand_name = filters.CharFilter(field_name='brand_id__brand_name',lookup_expr='icontains')
    effective_From = filters.DateFilter()
    effective_range = filters.DateFromToRangeFilter(field_name='effective_From')

    class Meta:
        model = SalesPriceList
        fields =[]

class SaleOrderItemsFilter(filters.FilterSet):
    sale_order_item_id = filters.CharFilter(method=filter_uuid)
    sale_order_id = filters.CharFilter(method=filter_uuid)
    product_id = filters.CharFilter(method=filter_uuid)
    product_name = filters.CharFilter(field_name='product_id__name',lookup_expr='icontains')
    quantity = filters.RangeFilter(field_name='quantity') #Ex: ?quantity_min=2&quantity_max=2
    unit_price = filters.RangeFilter()
    rate= filters.RangeFilter()
    amount = filters.RangeFilter()

    class Meta:
        model = SaleOrderItems
        fields = []

class SaleInvoiceOrdersFilter(filters.FilterSet):
    sale_invoice_id = filters.CharFilter(method=filter_uuid)
    bill_type = filters.CharFilter(lookup_expr='exact')
    invoice_date = filters.DateFilter()  
    invoice_no = filters.CharFilter(lookup_expr='icontains')
    customer_id = filters.CharFilter(method=filter_uuid)
    customer_name = filters.CharFilter(field_name='customer_id__name', lookup_expr='icontains')	
    gst_type_id = filters.CharFilter(method=filter_uuid)
    gst_type_name = filters.CharFilter(field_name='gst_type_id__name', lookup_expr='icontains')   
    email = filters.CharFilter(lookup_expr='exact')
    ref_no = filters.CharFilter(lookup_expr='icontains') 
    ref_date = filters.DateFromToRangeFilter() #Ex :  sales/sale_invoice_order/?ref_date_after=2023-01-01&ref_date_before=2024-06-08
    order_salesman_id = filters.CharFilter(method=filter_uuid)
    order_salesman_name = filters.CharFilter(field_name='order_salesman_id__name', lookup_expr='icontains') 	
    due_date = filters.DateFromToRangeFilter()    
    remarks = filters.CharFilter(lookup_expr='icontains')
    advance_amount = filters.RangeFilter()
    item_value = filters.RangeFilter()
    total_amount = filters.RangeFilter()
    order_status_id = filters.CharFilter(method=filter_uuid)
    status_name = filters.CharFilter(field_name='order_status_id__status_name', lookup_expr='icontains')   
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = SaleInvoiceOrders
        fields = []

class PaymentTransactionsFilter(filters.FilterSet):
    transaction_id = filters.CharFilter(method=filter_uuid)
    sale_invoice_id = filters.CharFilter(method=filter_uuid)
    payment_date = filters.RangeFilter()
    amount = filters.RangeFilter()
    payment_method = filters.CharFilter(lookup_expr='icontains')
    payment_status =filters.CharFilter(lookup_expr='icontains')
    reference_number = filters.CharFilter(lookup_expr='icontains')
    transaction_type =filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = PaymentTransactions
        fields = []

class SaleInvoiceItemsFilter(filters.FilterSet):
    sale_invoice_item_id = filters.CharFilter(method=filter_uuid)
    sale_invoice_id = filters.CharFilter(method=filter_uuid)
    product_id = filters.CharFilter(method=filter_uuid)
    product_name = filters.CharFilter(field_name='product_id__name',lookup_expr='icontains')
    quantity = filters.RangeFilter()
    unit_price = filters.RangeFilter()
    rate= filters.RangeFilter()
    amount = filters.RangeFilter()
    tax_code = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = SaleInvoiceItems
        fields = []

class SaleReturnOrdersFilter(filters.FilterSet):
    sale_return_id = filters.CharFilter(method=filter_uuid)
    bill_type = filters.CharFilter(lookup_expr='exact')
    return_date = filters.DateFilter()  
    return_no = filters.CharFilter(lookup_expr='icontains')
    customer_id = filters.CharFilter(method=filter_uuid)
    customer_name = filters.CharFilter(field_name='customer_id__name', lookup_expr='icontains')	
    gst_type_id = filters.CharFilter(method=filter_uuid)
    gst_type_name = filters.CharFilter(field_name='gst_type_id__name', lookup_expr='icontains')   
    email = filters.CharFilter(lookup_expr='exact')
    ref_no = filters.CharFilter(lookup_expr='icontains')
    ref_date = filters.DateFromToRangeFilter()
    order_salesman_id = filters.CharFilter(method=filter_uuid)
    order_salesman_name = filters.CharFilter(field_name='order_salesman_id__name', lookup_expr='icontains') 
    against_bill = filters.CharFilter(lookup_expr='exact')
    against_bill_date = filters.DateFilter()  
    due_date = filters.DateFromToRangeFilter()    
    return_reason = filters.CharFilter(lookup_expr='icontains')
    remarks = filters.CharFilter(lookup_expr='icontains')
    item_value = filters.RangeFilter()	
    transport_charges = filters.RangeFilter()    
    total_amount = filters.RangeFilter()	
    order_status_id = filters.CharFilter(method=filter_uuid)
    status_name = filters.CharFilter(field_name='order_status_id__status_name', lookup_expr='icontains')   
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = SaleReturnOrders
        fields = []

class SaleReturnItemsFilter(filters.FilterSet):
    sale_return_item_id = filters.CharFilter(method=filter_uuid)
    sale_return_id = filters.CharFilter(method=filter_uuid)
    product_id = filters.CharFilter(method=filter_uuid)
    product_name = filters.CharFilter(field_name='product_id__name',lookup_expr='icontains')
    quantity = filters.RangeFilter()
    unit_price = filters.RangeFilter()
    rate= filters.RangeFilter()
    amount = filters.RangeFilter()

    class Meta:
        model = SaleReturnItems
        fields = []

class OrderAttachmentsFilter(filters.FilterSet):
    attachment_id = filters.CharFilter(method=filter_uuid)
    order_id = filters.NumberFilter()
    attachment_name = filters.CharFilter(lookup_expr='exact')
    attachment_path = filters.CharFilter(lookup_expr='exact')
    order_type_id = filters.CharFilter(method=filter_uuid)
    order_type_name = filters.CharFilter(field_name='order_type_id__name', lookup_expr='icontains') 

    class Meta:
        model = OrderAttachments
        fields = []
		
class OrderShipmentsFilter(filters.FilterSet):
    shipment_id = filters.CharFilter(method=filter_uuid)
    order_id = filters.NumberFilter()
    shipping_mode_id = filters.CharFilter(method=filter_uuid)
    shipping_mode_name = filters.CharFilter(field_name='shipping_mode_id__name', lookup_expr='icontains')
    shipping_company_id = filters.CharFilter(method=filter_uuid)
    shipping_company_name = filters.CharFilter(field_name='shipping_company_id__name', lookup_expr='icontains')
    shipping_tracking_no = filters.CharFilter(field_name='shipping_tracking_no', lookup_expr='icontains')
    shipping_date = filters.DateFilter()
    order_type_id = filters.CharFilter(method=filter_uuid)
    order_type_name = filters.CharFilter(field_name='order_type_id__name', lookup_expr='icontains') 

    class Meta:
        model = OrderShipments
        fields = []