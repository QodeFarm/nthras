from django.db import models
import os
from uuid import uuid4  # Import the UUID module
# from masters import Ledger_accounts, Firm_statuses, Territory, Gst_categories, , Price_categories, Vendor_agent, Transporters

# Create your models here.
    
class VendorCategory(models.Model):
    vendor_category_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, null=True, default=None)
    name = models.CharField(max_length=255, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.vendor_category_id}_{self.name} ({self.code})'

    class Meta:
        db_table = 'vendor_category'


class VendorPaymentTerms(models.Model):
    payment_term_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, default=None)
    code = models.CharField(max_length=50, null=True, default=None)
    fixed_days = models.IntegerField(null=True, default=None)
    no_of_fixed_days = models.IntegerField(null=True, default=None)
    payment_cycle = models.CharField(max_length=255, null=True, default=None)
    run_on = models.CharField(max_length=255, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.payment_term_id}_{self.name} ({self.code})'
    
    class Meta:
        db_table = 'vendor_payment_terms'


class VendorAgent(models.Model):
    vendor_agent_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, null=True, default=None)
    name = models.CharField(max_length=255, null=True, default=None)
    commission_rate = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    
    RATE_ON_CHOICES = [
        ('Qty', 'Quantity'),
        ('Amount', 'Amount'),
    ]
    rate_on = models.CharField(max_length=20, choices=RATE_ON_CHOICES, null=True, default=None)
    
    AMOUNT_TYPE_CHOICES = [
        ('Taxable', 'Taxable'),
        ('BillAmount', 'Bill Amount'),
    ]
    amount_type = models.CharField(max_length=20, choices=AMOUNT_TYPE_CHOICES, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.vendor_agent_id}_{self.name} ({self.code})'
    
    class Meta:
        db_table = 'vendor_agent'


def custom_upload_to(instance, filename):
    file_extension = filename.split('.')[-1]
    unique_id = uuid4().hex[:7]  # Generate a unique ID (e.g., using UUID)
    new_filename = f"{unique_id}_{filename}"
    new_filename = new_filename.replace(' ', '_')
    return os.path.join('vendor', str(instance.name), new_filename)

class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    gst_no = models.CharField(max_length=255, null=True, default=None)
    name = models.CharField(max_length=255, null=True, default=None)
    print_name = models.CharField(max_length=255, null=True, default=None)
    identification = models.CharField(max_length=255, null=True, default=None)
    code = models.CharField(max_length=255, null=True, default=None)
    # ledger_account_id = models.ForeignKey(LedgerAccounts, null=True, default=None)
    vendor_common_for_sales_purchase = models.BooleanField(null=True, default=None)
    is_sub_vendor = models.BooleanField(null=True, default=None)
    # firm_status_id = models.ForeignKey(FirmStatuses, null=True, default=None)
    # territory_id = models.ForeignKey(Territory, null=True, default=None)
    vendor_category_id = models.ForeignKey(VendorCategory, on_delete=models.CASCADE, null=True, default=None, db_column='vendor_category_id')
    contact_person = models.CharField(max_length=255, null=True, default=None)
    # picture = models.ImageField(max_length=255, null=True, default=None)
    picture = models.ImageField(upload_to=custom_upload_to, max_length=255, null=True, default=None)
    gst = models.CharField(max_length=255, null=True, default=None)
    registration_date = models.DateField(null=True, default=None)
    cin = models.CharField(max_length=255, null=True, default=None)
    pan = models.CharField(max_length=255, null=True, default=None)
    # gst_category_id = models.ForeignKey(GstCategories,null=True, default=None)
    gst_suspend = models.BooleanField(null=True, default=None)
    TAX_TYPE_CHOICES = [('inclusive', 'Inclusive'),
                        ('exclusive', 'Exclusive')
                        ]
    tax_type = models.CharField(max_length=20, choices=TAX_TYPE_CHOICES , default= 'Inclusive')
    distance = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    tds_on_gst_applicable = models.BooleanField(null=True, default=None)
    tds_applicable = models.BooleanField(null=True, default=None)
    website = models.URLField(max_length=255, null=True, default=None)
    facebook = models.URLField(max_length=255, null=True, default=None)
    skype = models.URLField(max_length=255, null=True, default=None)
    twitter = models.URLField(max_length=255, null=True, default=None)
    linked_in = models.URLField(max_length=255, null=True, default=None)
    payment_term_id = models.ForeignKey(VendorPaymentTerms,on_delete=models.CASCADE, null=True, default=None, db_column='payment_term_id')
    # price_category_id = models.ForeignKey(PriceCategories, null=True, default=None)
    vendor_agent_id = models.ForeignKey(VendorAgent, on_delete=models.CASCADE, null=True, default=None, db_column='vendor_agent_id')
    # transporter_id = models.ForeignKey(Transporters, null=True, default=None)
    credit_limit = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    max_credit_days = models.IntegerField(null=True, default=None)
    interest_rate_yearly = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=None)
    rtgs_ifsc_code = models.CharField(max_length=255, null=True, default=None)
    accounts_number = models.CharField(max_length=255, null=True, default=None)
    bank_name = models.CharField(max_length=255, null=True, default=None)
    branch = models.CharField(max_length=255, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.vendor_id}_{self.name} ({self.code})'

    class Meta:
        db_table = 'vendor'


class VendorAttachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, default=None, db_column='vendor_id')
    attachment_name = models.CharField(max_length=255, null=True, default=None)
    attachment_path = models.CharField(max_length=255, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vendor_attachments'  # Set custom table name

    def __str__(self):
        return f'{self.attachment_id}_{self.attachment_name}'
    
class VendorAddress(models.Model):
    vendor_address_id = models.AutoField(primary_key=True)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, default=None,db_column='vendor_id')
    ADDRESS_TYPE_CHOICES = [
        ('billing', 'Billing'),
        ('shipping', 'Shipping')
        ]
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, null=True, default=None)
    address = models.CharField(max_length=255, null=True, default=None)
    country = models.CharField(max_length=255, null=True, default=None)
    state = models.CharField(max_length=255, null=True, default=None)
    city = models.CharField(max_length=255, null=True, default=None)
    pin_code = models.CharField(max_length=50, null=True, default=None)
    phone = models.CharField(max_length=50, null=True, default=None)
    email = models.EmailField(max_length=255, null=True, default=None)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, default=None)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, default=None)
    route_map = models.CharField(max_length=255, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vendor_addresses'

    def __str__(self):
        return f'{self.vendor_address_id}_{self.attachment_name}'