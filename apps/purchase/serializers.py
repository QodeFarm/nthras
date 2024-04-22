from rest_framework import serializers
from .models import *
from .serializers import *
from apps.vendor.serializers import ModVendorSerializer,ModVendorAgentSerializer,VendorAddressSerializer,ModVendorPaymentTermsSerializer
from apps.masters.serializers import PurchaseTypesSerializer,ModStateSerializer
from apps.customer.serializers import ModLedgerAccountsSerializers
from apps.products.serializers import ModproductsSerializer
#from apps.sales.serializers import ModGstTypesSerializer,ShippingModesSerializer,ModShippingCompaniesSerializer


class ModPurchaseOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrders
        fields = ['purchaseorder_id','email','delivery_date','order_date','order_no','ref_no','ref_date']

class PurchaseOrdersSerializer(serializers.ModelSerializer):
    #GST_Type = ModGstTypesSerializer(source='GST_Type_id',read_only=True)
    vendor = ModVendorSerializer(source='vendor_id',read_only=True)
    vendor_agent = ModVendorAgentSerializer(source='vendor_agent_id',read_only=True)
    vendor_address = VendorAddressSerializer(source='vendor_address_id',read_only=True)
    payment_term = ModVendorPaymentTermsSerializer(source='payment_term_id',read_only=True)
    purchase_type = PurchaseTypesSerializer(source='purchase_type_id',read_only=True)
    ledger_account = ModLedgerAccountsSerializers(source='ledger_account_id',read_only=True)

    class Meta:
        model = PurchaseOrders
        fields = '__all__'

class ModPurchaseorderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseorderItems
        fields = ['purchaseorder_item_id','tax_code']

class PurchaseorderItemsSerializer(serializers.ModelSerializer):
    purchaseorder_id = ModPurchaseOrdersSerializer(source='vendor_id',read_only=True)
    product_id = ModproductsSerializer(source='vendor_agent_id',read_only=True)

    class Meta:
        model = PurchaseorderItems
        fields = '__all__'


class ModPurchaseShipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseShipments
        fields = ['purchase_shipment_id','destination','shipping_tracking_no','shipping_date','shipping_charges']

class PurchaseShipmentsSerializer(serializers.ModelSerializer):
    #shipping_mode = ShippingModesSerializer(source='shipping_mode_id',read_only=True)
    #shipping_company = ModShippingCompaniesSerializer(source='shipping_company_id',read_only=True)
    port_state = ModStateSerializer(source='port_state_id',read_only=True)

    class Meta:
        model = PurchaseShipments
        fields = '__all__'
