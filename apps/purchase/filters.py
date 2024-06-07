from django_filters import rest_framework as filters
from .models import PurchaseOrders,PurchaseorderItems,PurchaseInvoiceOrders,PurchaseInvoiceItem,PurchaseReturnOrders,PurchaseReturnItems,PurchasePriceList
from utils_methods import filter_uuid

class PurchaseOrdersFilter(filters.FilterSet):
    purchase_order_id = filters.CharFilter(method=filter_uuid)
    purchase_type_id = filters.CharFilter(method=filter_uuid)
    purchase_type_name = filters.CharFilter(field_name='purchase_type_id__name', lookup_expr='icontains')
    order_date = filters.DateFromToRangeFilter()
    order_no = filters.CharFilter(lookup_expr='icontains')
    gst_type_id = filters.CharFilter(method=filter_uuid)
    gst_type_name = filters.CharFilter(field_name='gst_type_id__name', lookup_expr='icontains')
    vendor_id = filters.CharFilter(method=filter_uuid)
    vendor_name = filters.CharFilter(field_name='vendor_id__name', lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='exact')
    delivery_date = filters.DateFromToRangeFilter()
    ref_no = filters.CharFilter(lookup_expr='icontains')
    ref_date = filters.DateFromToRangeFilter()
    vendor_agent_id = filters.CharFilter(method=filter_uuid)
    vendor_agent_name = filters.CharFilter(field_name='vendor_agent_id__name', lookup_expr='icontains')
    remarks = filters.CharFilter(lookup_expr='icontains')
    payment_term_id = filters.CharFilter(method=filter_uuid)
    payment_term_name = filters.CharFilter(field_name='payment_term_id__name', lookup_expr='icontains')
    advance_amount = filters.RangeFilter()
    ledger_account_id = filters.CharFilter(method=filter_uuid)
    ledger_account_name = filters.CharFilter(field_name='ledger_account_id__name', lookup_expr='icontains') 
    item_value = filters.RangeFilter()
    discount = filters.RangeFilter()
    dis_amt = filters.RangeFilter()
    total_amount = filters.RangeFilter()
    order_status_id = filters.CharFilter(method=filter_uuid)
    status_name = filters.CharFilter(field_name='order_status_id__status_name', lookup_expr='icontains')   
    created_at = filters.DateFromToRangeFilter()
	
    class Meta:
        model = PurchaseOrders
        fields =[]

class PurchaseorderItemsFilter(filters.FilterSet):
    purchase_order_item_id = filters.CharFilter(method=filter_uuid)
    purchase_order_id = filters.CharFilter(method=filter_uuid)
    product_id = filters.CharFilter(method=filter_uuid)
    product_name = filters.CharFilter(field_name='product_id__name',lookup_expr='icontains')
    quantity = filters.RangeFilter()
    unit_price = filters.RangeFilter()
    rate= filters.RangeFilter()
    amount = filters.RangeFilter()
    discount = filters.RangeFilter()
    dis_amt = filters.RangeFilter()

    class Meta:
        model = PurchaseorderItems
        fields = []

class PurchaseInvoiceOrdersFilter(filters.FilterSet):
    purchase_invoice_id = filters.CharFilter(method=filter_uuid)
    purchase_type_id = filters.CharFilter(method=filter_uuid)
    purchase_type_name = filters.CharFilter(field_name='purchase_type_id__name', lookup_expr='icontains')
    invoice_date = filters.DateFilter()  
    invoice_no = filters.CharFilter(lookup_expr='icontains')
    gst_type_id = filters.CharFilter(method=filter_uuid)
    gst_type_name = filters.CharFilter(field_name='gst_type_id__name', lookup_expr='icontains')  
    vendor_id = filters.CharFilter(method=filter_uuid)
    vendor_name = filters.CharFilter(field_name='vendor_id__name', lookup_expr='icontains')	
    email = filters.CharFilter(lookup_expr='exact')
    delivery_date = filters.DateFromToRangeFilter()  
    supplier_invoice_date = filters.DateFromToRangeFilter()  
    vendor_agent_id = filters.CharFilter(method=filter_uuid)
    vendor_agent_name = filters.CharFilter(field_name='vendor_agent_id__name', lookup_expr='icontains')
    vendor_address_id = filters.CharFilter(method=filter_uuid)
    remarks = filters.CharFilter(lookup_expr='icontains')
    payment_term_id = filters.CharFilter(method=filter_uuid)
    payment_term_name = filters.CharFilter(field_name='payment_term_id__name', lookup_expr='icontains')
    due_date = filters.DateFromToRangeFilter()    
    advance_amount = filters.RangeFilter()
    ledger_account_id = filters.CharFilter(method=filter_uuid)
    ledger_account_name = filters.CharFilter(field_name='ledger_account_id__name', lookup_expr='icontains') 
    item_value = filters.RangeFilter()	
    discount = filters.RangeFilter()
    dis_amt = filters.RangeFilter()
    total_amount = filters.RangeFilter()          
    order_status_id = filters.CharFilter(method=filter_uuid)
    status_name = filters.CharFilter(field_name='order_status_id__status_name', lookup_expr='icontains')   
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = PurchaseInvoiceOrders
        fields = []

class PurchaseInvoiceItemFilter(filters.FilterSet):
    purchase_invoice_item_id = filters.CharFilter(method=filter_uuid)
    purchase_invoice_id = filters.CharFilter(method=filter_uuid)
    product_id = filters.CharFilter(method=filter_uuid)
    product_name = filters.CharFilter(field_name='product_id__name',lookup_expr='icontains')
    quantity = filters.RangeFilter()
    unit_price = filters.RangeFilter()
    rate= filters.RangeFilter()
    amount = filters.RangeFilter()
    discount = filters.RangeFilter()
    dis_amt = filters.RangeFilter()

    class Meta:
        model = PurchaseInvoiceItem
        fields = []

    		
class PurchaseReturnOrdersFilter(filters.FilterSet):
    purchase_return_id = filters.CharFilter(method=filter_uuid)
    purchase_type_id = filters.CharFilter(method=filter_uuid)
    purchase_type_name = filters.CharFilter(field_name='purchase_type_id__name', lookup_expr='icontains')
    return_date = filters.DateFilter()  
    return_no = filters.CharFilter(lookup_expr='icontains')
    gst_type_id = filters.CharFilter(method=filter_uuid)
    gst_type_name = filters.CharFilter(field_name='gst_type_id__name', lookup_expr='icontains')  
    vendor_id = filters.CharFilter(method=filter_uuid)
    vendor_name = filters.CharFilter(field_name='vendor_id__name', lookup_expr='icontains')	  
    email = filters.CharFilter(lookup_expr='exact')
    ref_no = filters.CharFilter(lookup_expr='icontains')
    ref_date = filters.DateFromToRangeFilter()
    vendor_agent_id = filters.CharFilter(method=filter_uuid)
    vendor_agent_name = filters.CharFilter(field_name='vendor_agent_id__name', lookup_expr='icontains')
    vendor_address_id = filters.CharFilter(method=filter_uuid)
    remarks = filters.CharFilter(lookup_expr='icontains')
    payment_term_id = filters.CharFilter(method=filter_uuid)
    payment_term_name = filters.CharFilter(field_name='payment_term_id__name', lookup_expr='icontains')
    due_date = filters.DateFromToRangeFilter()    
    return_reason = filters.CharFilter(lookup_expr='icontains')
    item_value = filters.RangeFilter()	
    discount = filters.RangeFilter()
    dis_amt = filters.RangeFilter()
    transport_charges = filters.RangeFilter()    
    total_amount = filters.RangeFilter()	
    order_status_id = filters.CharFilter(method=filter_uuid)
    status_name = filters.CharFilter(field_name='order_status_id__status_name', lookup_expr='icontains')   
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = PurchaseReturnOrders
        fields = []

class PurchaseReturnItemsFilter(filters.FilterSet):
    purchase_return_item_id = filters.CharFilter(method=filter_uuid)
    purchase_return_id = filters.CharFilter(method=filter_uuid)
    product_id = filters.CharFilter(method=filter_uuid)
    product_name = filters.CharFilter(field_name='product_id__name',lookup_expr='icontains')
    quantity = filters.RangeFilter()
    unit_price = filters.RangeFilter()
    rate= filters.RangeFilter()
    amount = filters.RangeFilter()
    discount = filters.RangeFilter()
    dis_amt = filters.RangeFilter()

    class Meta:
        model = PurchaseReturnItems
        fields = []

class PurchasePriceListFilter(filters.FilterSet):
    purchase_price_list_id = filters.CharFilter(method=filter_uuid)
    customer_category_id = filters.CharFilter(method=filter_uuid)
    customer_category_name = filters.CharFilter(field_name='customer_category_id__name',lookup_expr='icontains')
    brand_id = filters.CharFilter(method=filter_uuid)
    brand_name = filters.CharFilter(field_name='brand_id__name',lookup_expr='icontains')
    effective_from = filters.DateFilter()
    effective_range = filters.DateFromToRangeFilter(field_name='effective_from')

    class Meta:
        model = PurchasePriceList
        fields =[]