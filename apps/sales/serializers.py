from rest_framework import serializers
from apps.customer.serializers import ModCustomerAddressesSerializer, ModCustomersSerializer, ModCustomerPaymentTermsSerializers, ModLedgerAccountsSerializers
from apps.masters.serializers import ModCustomerCategoriesSerializers, ModProductBrandsSerializer
from apps.products.serializers import ModProductGroupsSerializer, ModproductsSerializer
from .models import *


#----------Modified Serializers--------------------------
class ModGstTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GstTypes
        fields = ['gst_type_id','name']

class ModSaleTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleTypes
        fields = ['sale_type_id','name']

class ModSaleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleOrder
        fields = ['order_id','customer_id','order_date','delivery_date']

class ModShippingCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCompanies
        fields = ['shipping_company_id','code','name']
# -------------------------------------------------------

class SaleTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleTypes
        fields = '__all__'

class ShippingModesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingModes
        fields = '__all__'

class GstTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GstTypes
        fields = '__all__'

class ShippingCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCompanies
        fields = '__all__'

class SaleOrderSerializer(serializers.ModelSerializer):
    gst_type = ModGstTypesSerializer(source='gst_type_id', read_only=True)
    customer = ModCustomersSerializer(source='customer_id', read_only=True)
    customer_address = ModCustomerAddressesSerializer(source='customer_address_id', read_only=True)
    payment_term = ModCustomerPaymentTermsSerializers(source='payment_term_id', read_only=True)
    sale_type = ModSaleTypesSerializer(source='sale_type_id', read_only=True)
    ledger_account = ModLedgerAccountsSerializers(source='ledger_account_id', read_only=True)
    
    class Meta:
        model = SaleOrder
        fields = '__all__'

class InvoicesSerializer(serializers.ModelSerializer):
    order = ModSaleOrderSerializer(source='order_id', read_only=True)
    # warehouse_id = ModSaleOrderSerializers(source='order_id', read_only=True) #update here later
    sale_type = ModSaleTypesSerializer(source='sale_type_id', read_only=True)

    class Meta:
        model = Invoices
        fields = '__all__'

class PaymentTransactionsSerializer(serializers.ModelSerializer):
    invoice = InvoicesSerializer(source='invoice_id', read_only=True) #change the serializers
    
    class Meta:
        model = PaymentTransactions
        fields = '__all__'

class OrderItemsSerializer(serializers.ModelSerializer):
    order = ModSaleOrderSerializer(source='order_id', read_only=True)
    product = ModproductsSerializer(source='product_id', read_only=True)

    class Meta:
        model = OrderItems
        fields = '__all__'

class ShipmentsSerializer(serializers.ModelSerializer):
    shipping_mode = ShippingModesSerializer(source='shipping_mode_id', read_only=True)
    shipping_company = ModShippingCompaniesSerializer(source='shipping_company_id', read_only=True)
    order = ModSaleOrderSerializer(source='order_id', read_only=True)
    class Meta:
        model = Shipments
        fields = '__all__'

class SalesPriceListSerializer(serializers.ModelSerializer):
    customer_category = ModCustomerCategoriesSerializers(source='customer_category_id', read_only=True)
    brand = ModProductBrandsSerializer(source='brand_id', read_only=True)
    group = ModProductGroupsSerializer(source='group_id', read_only=True)
    class Meta:
        model = SalesPriceList
        fields = '__all__'

class SaleOrderReturnsSerializer(serializers.ModelSerializer):
    sale = ModSaleOrderSerializer(source='sale_id', read_only=True)

    class Meta:
        model = SaleOrderReturns
        fields = '__all__'