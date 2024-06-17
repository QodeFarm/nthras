from collections import OrderedDict
from requests import Response
from rest_framework import serializers
from apps.customer.serializers import ModCustomerAddressesSerializer, ModCustomersSerializer, ModCustomerPaymentTermsSerializers, ModLedgerAccountsSerializers
from apps.inventory.serializers import ModWarehousesSerializer
from apps.masters.serializers import ModCustomerCategoriesSerializers, ModGstTypesSerializer, ModProductBrandsSerializer, ModSaleTypesSerializer, ModShippingCompaniesSerializer, ShippingModesSerializer, ModOrdersSalesmanSerializer, ModPaymentLinkTypesSerializer, ModOrderStatusesSerializer, ModOrderTypesSerializer
from apps.products.serializers import ModProductGroupsSerializer, ModproductsSerializer, productsSerializer
from config.utils_methods import add_key_value_to_all_ordereddicts
from .models import *
from django.conf import settings
from apps.products.models import Products
from drf_writable_nested import WritableNestedModelSerializer

#----------Modified Serializers--------------------------

class ModSaleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleOrder
        fields = ['sale_order_id','customer_id','order_date','delivery_date']

class ModSaleReturnOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleReturnOrders
        fields = ['sale_return_id','return_date','return_no']

class ModSaleInvoiceOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleInvoiceOrders
        fields = ['sale_invoice_id','invoice_date','invoice_no',]
# -------------------------------------------------------

# class SaleOrderSerializer(serializers.ModelSerializer):
#     gst_type = ModGstTypesSerializer(source='gst_type_id', read_only=True)
#     customer = ModCustomersSerializer(source='customer_id', read_only=True)
#     customer_address = ModCustomerAddressesSerializer(source='customer_address_id', read_only=True)
#     payment_term = ModCustomerPaymentTermsSerializers(source='payment_term_id', read_only=True)
#     sale_type = ModSaleTypesSerializer(source='sale_type_id', read_only=True)
#     order_status = ModOrderStatusesSerializer(source='order_status_id', read_only=True)
#     ledger_account = ModLedgerAccountsSerializers(source='ledger_account_id', read_only=True)
#     saleorderitem = 
    
#     class Meta:
#         model = SaleOrder
#         fields = '__all__'
        
class PaymentTransactionsSerializer(serializers.ModelSerializer):
    invoice = ModSaleInvoiceOrdersSerializer(source='sale_invoice_id', read_only=True)
    
    class Meta:
        model = PaymentTransactions
        fields = '__all__'

class SaleInvoiceItemsSerializer(serializers.ModelSerializer):
    sale_order = ModSaleOrderSerializer(source='sale_order_id', read_only=True)
    product = ModproductsSerializer(source='product_id', read_only=True)

    class Meta:
        model = SaleInvoiceItems
        fields = '__all__'

class SalesPriceListSerializer(serializers.ModelSerializer):
    customer_category = ModCustomerCategoriesSerializers(source='customer_category_id', read_only=True)
    brand = ModProductBrandsSerializer(source='brand_id', read_only=True)
    group = ModProductGroupsSerializer(source='group_id', read_only=True)
    class Meta:
        model = SalesPriceList
        fields = '__all__'

class SaleOrderItemsSerializer(serializers.ModelSerializer):
    # sale_order = ModSaleOrderSerializer(source='sale_order_id', read_only=True)
    # product = ModproductsSerializer(source='product_id', read_only=True)

    class Meta:
        model = SaleOrderItems
        fields = '__all__'

class SaleInvoiceOrdersSerializer(serializers.ModelSerializer):
    gst_type = ModGstTypesSerializer(source='gst_type_id', read_only=True)
    customer = ModCustomersSerializer(source='customer_id', read_only=True)
    customer_address = ModCustomerAddressesSerializer(source='customer_address_id', read_only=True)
    payment_term = ModCustomerPaymentTermsSerializers(source='payment_term_id', read_only=True)
    orders_salesman = ModOrdersSalesmanSerializer(source='order_salesman_id', read_only=True)
    payment_link_type = ModPaymentLinkTypesSerializer(source='payment_link_type_id', read_only=True)
    ledger_account = ModLedgerAccountsSerializers(source='ledger_account_id', read_only=True)
    order_status = ModOrderStatusesSerializer(source='order_status_id', read_only=True)
    

    class Meta:
        model = SaleInvoiceOrders
        fields = '__all__'

class SaleReturnOrdersSerializer(serializers.ModelSerializer):
    gst_type = ModGstTypesSerializer(source='gst_type_id', read_only=True)
    customer = ModCustomersSerializer(source='customer_id', read_only=True)
    customer_address = ModCustomerAddressesSerializer(source='customer_address_id', read_only=True)
    payment_term = ModCustomerPaymentTermsSerializers(source='payment_term_id', read_only=True)
    orders_salesman = ModOrdersSalesmanSerializer(source='order_salesman_id', read_only=True)
    payment_link_type = ModPaymentLinkTypesSerializer(source='payment_link_type_id', read_only=True)
    order_status = ModOrderStatusesSerializer(source='order_status_id', read_only=True)

    class Meta:
        model = SaleReturnOrders
        fields = '__all__'
    
class SaleReturnItemsSerializer(serializers.ModelSerializer):
    sale_return = ModSaleReturnOrdersSerializer(source='sale_return_id', read_only=True)
    product = ModproductsSerializer(source='product_id', read_only=True)
    
    class Meta:
        model = SaleReturnItems
        fields = '__all__'

class OrderAttachmentsSerializer(serializers.ModelSerializer):
    order_type = ModOrderTypesSerializer(source='order_type_id', read_only=True)

    class Meta:
        model = OrderAttachments
        fields = '__all__'

class OrderShipmentsSerializer(serializers.ModelSerializer):
    shipping_mode = ShippingModesSerializer(source='shipping_mode_id', read_only=True)
    shipping_company = ModShippingCompaniesSerializer(source='shipping_company_id', read_only=True)
    order_type = ModOrderTypesSerializer(source='order_type_id', read_only=True)

    class Meta:
        model = OrderShipments
        fields = '__all__'

class SaleOrderSerializer(serializers.ModelSerializer):
    
    sale_order_items = SaleOrderItemsSerializer(many=True)
    # order_shipments = OrderShipmentsSerializer(many=True)
    order_shipments = serializers.DictField(write_only=True)
 
    class Meta:
        model = SaleOrder
        # fields = '__all__'
        fields = ['sale_order_id','email', 'delivery_date', 'order_date','order_no', 'ref_no', 'ref_date', 'tax', 'remarks','advance_amount', 
                  'item_value', 'discount', 'dis_amt','taxable', 'tax_amount', 'cess_amount', 'round_off','doc_amount', 'vehicle_name', 
                  'total_boxes','gst_type_id','customer_id','customer_address_id','payment_term_id','sale_type_id','ledger_account_id','order_status_id',
                  'sale_order_items','order_shipments']


    def create(self, validated_data):
        print('\t***i am working***')
        print(validated_data)
        sale_order_data = validated_data.pop('sale_order')
        sale_order_items_data = validated_data.pop('sale_order_items')
        order_shipments_data = validated_data.pop('order_shipments')

        sale_order = SaleOrder.objects.create(**sale_order_data)

        add_key_value_to_all_ordereddicts(sale_order_items_data,'sale_order',sale_order) #add 'sale_order_id' to the 'Saleorderitems' data

        for item_data in sale_order_items_data:
            SaleOrderItems.objects.create(sale_order_id=str(sale_order), **item_data) # UUID not Valid Error so Converted to str
            # SaleOrderItems.objects.create(**item_data) # this approach also working but no need to convert to str


        data = OrderShipments.objects.create(**order_shipments_data)
        return sale_order



        # serializer = OrderShipmentsSerializer(data=order_shipments_data)
        # if serializer.is_valid():
        #     instance = serializer.save()
        #     return sale_order
        # else:
        #     print(serializer.errors)
        #     print('\t***due to error sale order instance is deleted***')
        #     sale_order.delete()
            




