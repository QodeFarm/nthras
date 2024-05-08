from django_filters import rest_framework as filters
from .models import PurchaseOrders,PurchaseorderItems,PurchaseShipments,PurchasePriceList,PurchaseOrderReturns

class PurchaseOrdersFilter(filters.FilterSet):
    purchaseorder_id = filters.NumberFilter()
    vendor_id = filters.NumberFilter()
    vendor_name = filters.CharFilter(field_name='vendor_id__name', lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='exact')
    delivery_date = filters.DateFromToRangeFilter()
    order_date = filters.DateFromToRangeFilter()
    order_no = filters.CharFilter(lookup_expr='icontains')
    remarks = filters.CharFilter(lookup_expr='icontains')
    purchase_type_id = filters.NumberFilter()
    name = filters.CharFilter(field_name='purchase_type_id__name', lookup_expr='icontains')
    advance_amount = filters.RangeFilter()
    item_value = filters.RangeFilter()
    discount = filters.RangeFilter()
    doc_amount = filters.RangeFilter()
    created_at = filters.DateFromToRangeFilter()
	
    class Meta:
        model = PurchaseOrders
        fields =[]

class PurchaseorderItemsFilter(filters.FilterSet):
    purchaseorder_id = filters.NumberFilter()
    product_id = filters.NumberFilter()
    name = filters.CharFilter(field_name='product_id__name',lookup_expr='icontains')
    rate= filters.RangeFilter()
    amount = filters.RangeFilter()
    discount = filters.RangeFilter()

    class Meta:
        model = PurchaseorderItems
        fields = ['purchaseorder_id', 'product_id', 'rate','amount','discount']

class PurchaseShipmentsFilter(filters.FilterSet):
    purchaseorder_id = filters.NumberFilter()
    shipping_date = filters.DateFilter()
    shipping_tracking_no = filters.CharFilter(field_name='shipping_tracking_no', lookup_expr='icontains')
    shipping_charges= filters.RangeFilter()
    
    class Meta:
        model = PurchaseShipments
        fields = ['purchaseorder_id','shipping_date','shipping_tracking_no','shipping_charges']

class PurchasePriceListFilter(filters.FilterSet):
    customer_category_id = filters.NumberFilter()
    name = filters.CharFilter(field_name='customer_category_id__name',lookup_expr='icontains')
    brand_id = filters.NumberFilter()
    brand_name = filters.CharFilter(field_name='brand_id__brand_name',lookup_expr='icontains')
    effective_from = filters.DateFilter()
    effective_range = filters.DateFromToRangeFilter(field_name='effective_from')

    class Meta:
        model = PurchasePriceList
        fields = ['customer_category_id','brand_id','effective_from']

class PurchaseOrderReturnsFilter(filters.FilterSet):
    purchaseorder_id = filters.NumberFilter()
    purchase_return_no = filters.CharFilter(lookup_expr='icontains')
    due_date = filters.DateFilter()
    return_reason = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = PurchaseOrderReturns
        fields = ['purchaseorder_id','purchase_return_no','due_date','return_reason']