from django.db import models
from utils_variables import *
from apps.masters.models import PurchaseTypes,State,ProductBrands, GstTypes,ShippingModes,ShippingCompanies
from apps.customer.models import LedgerAccounts,CustomerCategories
from apps.vendor.models import Vendor,VendorAgent,VendorAddress,VendorPaymentTerms
from apps.products.models import products
import uuid

# Create your models here.
class PurchaseOrders(models.Model):
    purchaseorder_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gst_type_id = models.ForeignKey(GstTypes, on_delete=models.CASCADE, null=True, default=None, db_column = 'GST_Type_id')
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_column = 'vendor_id')
    email = models.EmailField(max_length=255, null=True, default=None)
    delivery_date = models.DateField()
    order_date = models.DateField()
    order_no = models.CharField(max_length=255)
    ref_no = models.CharField(max_length=255, null=True, default=None)
    ref_date = models.DateField()
    vendor_agent_id = models.ForeignKey(VendorAgent, on_delete=models.CASCADE, null=True, default=None, db_column = 'vendor_agent_id')
    TAX_CHOICES = [('inclusive', 'Inclusive'),
                   ('exclusive', 'Exclusive')
                ]
    tax = models.CharField(max_length=20, choices=TAX_CHOICES , default= 'Inclusive')
    vendor_address_id = models.ForeignKey(VendorAddress, on_delete=models.CASCADE, null=True, default=None, db_column = 'vendor_address_id')
    remarks = models.TextField(null=True, default=None)
    approval_status = models.CharField(max_length=255, null=True, default=None)
    payment_term_id = models.ForeignKey(VendorPaymentTerms, on_delete=models.CASCADE, null=True, default=None, db_column = 'payment_term_id')
    purchase_type_id = models.ForeignKey(PurchaseTypes, on_delete=models.CASCADE, null=True, default=None, db_column = 'purchase_type_id')
    advance_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    ledger_account_id = models.ForeignKey(LedgerAccounts, on_delete=models.CASCADE, null=True, default=None, db_column = 'ledger_account_id')
    item_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    discount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    dis_amt = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    taxable = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    tax_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    cess_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    round_off = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    doc_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
	
    class Meta:
        db_table = purchaseorderstable

    def __str__(self):
        return f"{self.purchaseorder_id}"

class PurchaseorderItems(models.Model):
    purchaseorder_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchaseorder_id = models.ForeignKey(PurchaseOrders, on_delete=models.CASCADE, db_column = 'purchaseorder_id')
    product_id = models.ForeignKey(products, on_delete=models.CASCADE, db_column = 'product_id')
    quantity = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    rate = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    discount_percentage = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    discount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    dis_amt = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    tax_code = models.CharField(max_length=255, null=True, default=None)
    tax_rate = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
	
    class Meta:
        db_table = purchaseorderitemstable
		
    def __str__(self):
        return f"{self.purchaseorder_item_id}"

class PurchaseShipments(models.Model):
    purchase_shipment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchaseorder_id = models.ForeignKey(PurchaseOrders, on_delete=models.CASCADE, db_column = 'purchaseorder_id')
    destination = models.CharField(max_length=255, null=True, default=None)
    shipping_mode_id = models.ForeignKey(ShippingModes, on_delete=models.CASCADE, null=True, default=None, db_column = 'shipping_mode_id')
    shipping_company_id = models.ForeignKey(ShippingCompanies, on_delete=models.CASCADE, null=True, default=None, db_column = 'shipping_company_id')
    shipping_tracking_no = models.CharField(max_length=255, null=True, default=None)
    shipping_date = models.DateField()
    shipping_charges = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    vehicle_vessel_no = models.CharField(max_length=255, null=True, default=None)
    charge_type = models.CharField(max_length=255, null=True, default=None)
    document_through = models.CharField(max_length=255, null=True, default=None)
    port_of_landing = models.CharField(max_length=255, null=True, default=None)
    port_of_discharge = models.CharField(max_length=255, null=True, default=None)
    port_address_for_eway = models.CharField(max_length=255, null=True, default=None)
    port_state_for_eway = models.CharField(max_length=255)
    port_state_id = models.ForeignKey(State, on_delete=models.CASCADE,db_column = 'port_state_id')
    no_of_packets = models.IntegerField()
    weight = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
	
    class Meta:
        db_table = purchaseshipmentstable

    def __str__(self):
        return f"{self.purchase_shipment_id}"

class PurchasePriceList(models.Model):
    purchase_price_list_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=255)
    customer_category_id = models.ForeignKey(CustomerCategories, on_delete=models.CASCADE, db_column = 'customer_category_id')
    brand_id = models.ForeignKey(ProductBrands, on_delete=models.CASCADE, null=True, default=None, db_column = 'brand_id')
    effective_from = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = purchasepricelisttable

    def __str__(self):
        return f"{self.purchase_price_list_id}"

class PurchaseOrderReturns(models.Model):
    purchase_order_return_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchaseorder_id = models.ForeignKey(PurchaseOrders, on_delete=models.CASCADE, db_column = 'purchaseorder_id')
    purchase_return_no = models.CharField(max_length=255, null=True, default=None)
    payment_link = models.CharField(max_length=255, null=True, default=None)
    due_date = models.DateField(null=True, default=None)
    return_reason = models.TextField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = purchaseorderreturnstable

    def __str__(self):
        return f"{self.purchase_order_return_id}"