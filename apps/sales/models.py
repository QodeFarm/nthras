from django.db import models
from apps.customer.models import CustomerAddresses, LedgerAccounts, Customer
from apps.masters.models import CustomerPaymentTerms, ProductItemType
from utils_variables import saletypes, saleorders, gsttypes, shippingmodes, shippingcompanies, paymenttransactions, invoices, warehouses, orderitems, shipments
from apps.products.models import products as Products

# Create your models here.

class GstTypes(models.Model):
    gst_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = gsttypes

class SaleTypes(models.Model):
    sale_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = saletypes

class SaleOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    gst_type_id = models.ForeignKey(GstTypes, on_delete=models.CASCADE, null=True, default=None, db_column='gst_type_id')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, default=None, db_column='customer_id')
    email = models.CharField(max_length=255, null=True, default=None)
    delivery_date = models.DateField(null=True, default=None)
    order_date = models.DateField(null=True, default=None)
    order_no = models.CharField(max_length=255, null=True, default=None)
    ref_no = models.CharField(max_length=255, null=True, default=None)
    ref_date = models.DateField(null=True, default=None)
    TAX_CHOICES = [
        ('Inclusive', 'Inclusive'),
        ('Exclusive', 'Exclusive')
        ]
    tax = models.CharField(max_length=10, choices=TAX_CHOICES, null=True, default=None)
    customer_address_id = models.ForeignKey(CustomerAddresses, on_delete=models.CASCADE, null=True, default=None, db_column='customer_address_id')
    remarks = models.TextField(null=True, default=None)
    payment_term_id = models.ForeignKey(CustomerPaymentTerms, on_delete=models.CASCADE, null=True, default=None, db_column='payment_term_id')
    sale_type_id = models.ForeignKey(SaleTypes, on_delete=models.CASCADE, null=True, default=None, db_column='sale_type_id')
    advance_amount = models.DecimalField(max_digits=18, decimal_places=2,null=True, default=None)
    ledger_account_id = models.ForeignKey(LedgerAccounts, on_delete=models.CASCADE, null=True, default=None, db_column='ledger_account_id')
    item_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    discount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    dis_amt = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    taxable = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None, help_text= 'ENTER NUMBER')
    tax_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    cess_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    round_off = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    doc_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    vehicle_name = models.CharField(max_length=255, null=True, default=None)
    total_boxes = models.IntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.order_id}'
    
    class Meta:
        db_table = saleorders

class ShippingModes(models.Model):
    shipping_mode_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = shippingmodes

class ShippingCompanies(models.Model):
    shipping_company_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=255,null=True,default=None)
    name = models.CharField(max_length=255,null=True,default=None)
    gst_no = models.CharField(max_length=255,null=True,default=None)
    website_url = models.CharField(max_length=255,null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = shippingcompanies

class Warehouses(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,default=None)
    code = models.CharField(max_length=255,null=True,default=None)
    item_type_id = models.ForeignKey(ProductItemType, on_delete=models.CASCADE, null=True, default=None, db_column='item_type_id')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, default=None, db_column='customer_id')
    address = models.CharField(max_length=255, null=True, default=None)
    city_id = models.ForeignKey('masters.City', on_delete=models.CASCADE, null=True, default=None, db_column = 'city_id')
    pin_code = models.CharField(max_length=50,null=True,default=None)
    phone = models.CharField(max_length=50,null=True,default=None)
    email = models.CharField(max_length=255,null=True,default=None)
    longitude = models.DecimalField(max_digits=10,decimal_places=6, null=True, default=None)
    latitude = models.DecimalField(max_digits=10,decimal_places=6, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = warehouses

class Invoices(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, null=True, default=None, db_column='order_id')
    warehouse_id = models.ForeignKey(Warehouses, on_delete=models.CASCADE, null=True, default=None, db_column='warehouse_id')
    invoice_date = models.DateField(null=True, default=None)
    due_date = models.DateField(null=True, default=None)
    status = models.CharField(max_length=50,null=True,default=None)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    sale_type_id = models.ForeignKey(SaleTypes, on_delete=models.CASCADE, null=True, default=None, db_column='sale_type_id')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.invoice_id}'
    
    class Meta:
        db_table = invoices

class PaymentTransactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    invoice_id = models.ForeignKey(Invoices, on_delete=models.CASCADE, null=True, default=None, db_column='invoice_id')
    payment_date = models.DateField(null=True, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    payment_method = models.CharField(max_length=100,null=True,default=None)
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ]
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, null=True, default='Pending')
    reference_number = models.CharField(max_length=100,null=True,default=None)
    notes = models.TextField(null=True, default=None)
    currency = models.CharField(max_length=10,null=True,default=None)

    def __str__(self):
        return f'{self.transaction_id}'
    
    class Meta:
        db_table = paymenttransactions

class OrderItems(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, null=True, default=None, db_column='order_id')
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, default=None, db_column='product_id')
    quantity = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    rate = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    discount_percentage = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    discount = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    dis_amt = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    tax_code = models.CharField(max_length=255,null=True,default=None)
    tax_rate = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.order_item_id}'
    
    class Meta:
        db_table = orderitems

class Shipments(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    destination = models.CharField(max_length=255,null=True,default=None)
    shipping_mode_id = models.ForeignKey(ShippingModes,on_delete=models.CASCADE, null=True, default=None, db_column='shipping_mode_id')
    shipping_company_id = models.ForeignKey(ShippingCompanies,on_delete=models.CASCADE, null=True, default=None, db_column='shipping_company_id')
    shipping_tracking_no = models.CharField(max_length=255,null=True,default=None)
    shipping_date = models.DateField(null=True, default=None)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    vehicle_vessel = models.CharField(max_length=255,null=True,default=None, help_text='Enter Text')
    charge_type = models.CharField(max_length=255,null=True,default=None)
    document_through = models.CharField(max_length=255,null=True,default=None)
    port_of_landing = models.CharField(max_length=255,null=True,default=None)
    port_of_discharge = models.CharField(max_length=255,null=True,default=None)
    no_of_packets = models.IntegerField(null=True, default=None)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    order_id = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, null=True, default=None, db_column='order_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.shipment_id}'
    
    class Meta:
        db_table = shipments
