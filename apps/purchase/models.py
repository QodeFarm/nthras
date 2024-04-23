from django.db import models
from utils_variables import *
from apps.masters.models import PurchaseTypes,State,ProductBrands
from apps.customer.models import LedgerAccounts,CustomerCategories
from apps.vendor.models import Vendor,VendorAgent,VendorAddress,VendorPaymentTerms
from apps.sales.models import GstTypes,ShippingModes,ShippingCompanies
from apps.products.models import products,ProductGroups


# Create your models here.
class PurchaseOrders(models.Model):
    purchaseorder_id = models.AutoField(primary_key=True)
    GST_Type_id = models.ForeignKey(GstTypes, on_delete=models.CASCADE, null=True, default=None, db_column = 'GST_Type_id')
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, default=None, db_column = 'vendor_id')
    email = models.EmailField(max_length=255, null=True, default=None)
    delivery_date = models.DateField(null=True, default=None)
    order_date = models.DateField(null=True, default=None)
    order_no = models.CharField(max_length=255, null=True, default=None)
    ref_no = models.CharField(max_length=255, null=True, default=None)
    ref_date = models.DateField(null=True, default=None)
    vendor_agent_id = models.ForeignKey(VendorAgent, on_delete=models.CASCADE, null=True, default=None, db_column = 'vendor_agent_id')
    TAX_CHOICES = [('inclusive', 'Inclusive'),
                   ('exclusive', 'Exclusive')
                ]
    tax = models.CharField(max_length=20, choices=TAX_CHOICES , default= 'Inclusive')
    vendor_address_id = models.ForeignKey(VendorAddress, on_delete=models.CASCADE, null=True, default=None, db_column = 'vendor_address_id')
    remarks = models.TextField()
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
    purchaseorder_item_id = models.AutoField(primary_key=True)
    purchaseorder_id = models.ForeignKey(PurchaseOrders, on_delete=models.CASCADE, null=True, default=None, db_column = 'purchaseorder_id')
    product_id = models.ForeignKey(products, on_delete=models.CASCADE, null=True, default=None, db_column = 'product_id')
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
    purchase_shipment_id = models.AutoField(primary_key=True)
    destination = models.CharField(max_length=255, null=True, default=None)
    shipping_mode_id = models.ForeignKey(ShippingModes, on_delete=models.CASCADE, null=True, default=None, db_column = 'shipping_mode_id')
    shipping_company_id = models.ForeignKey(ShippingCompanies, on_delete=models.CASCADE, null=True, default=None, db_column = 'shipping_company_id')
    shipping_tracking_no = models.CharField(max_length=255, null=True, default=None)
    shipping_date = models.DateField(null=True, default=None)
    shipping_charges = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    vehicle_vessel_no = models.CharField(max_length=255, null=True, default=None)
    charge_type = models.CharField(max_length=255, null=True, default=None)
    document_through = models.CharField(max_length=255, null=True, default=None)
    port_of_landing = models.CharField(max_length=255, null=True, default=None)
    port_of_discharge = models.CharField(max_length=255, null=True, default=None)
    port_address_for_eway = models.CharField(max_length=255, null=True, default=None)
    port_state_for_eway = models.CharField(max_length=255, null=True, default=None)
    port_state_id = models.ForeignKey(State, on_delete=models.CASCADE, null=True, default=None, db_column = 'port_state_id')
    no_of_packets = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
	
    class Meta:
        db_table = purchaseshipmentstable

    def __str__(self):
        return f"{self.purchase_shipment_id}"

class PurchasePriceList(models.Model):
    purchase_price_list_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, null=True, default=None)
    customer_category_id = models.ForeignKey(CustomerCategories, on_delete=models.CASCADE, null=True, default=None, db_column = 'customer_category_id')
    brand_id = models.ForeignKey(ProductBrands, on_delete=models.CASCADE, null=True, default=None, db_column = 'brand_id')
    effective_from = models.DateField(null=True, default=None)
    effective_date = models.DateField(null=True, default=None)
    group_id = models.ForeignKey(ProductGroups, on_delete=models.CASCADE, null=True, default=None, db_column = 'group_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = purchasepricelisttable

    def __str__(self):
        return f"{self.purchase_price_list_id}"

class PurchaseOrderReturns(models.Model):
    purchase_order_return_id = models.AutoField(primary_key=True)
    purchaseorder_id = models.ForeignKey(PurchaseOrders, on_delete=models.CASCADE, null=True, default=None, db_column = 'purchaseorder_id')
    purchase_return_no = models.CharField(max_length=255, null=True, default=None)
    payment_link = models.CharField(max_length=255, null=True, default=None)
    due_date = models.DateField(null=True, default=None)
    return_reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = purchaseorderreturnstable

    def __str__(self):
        return f"{self.purchase_order_return_id}"