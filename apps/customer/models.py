import os
import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from apps.masters.models import *
from utils import Ledgeraccounts, Customers, Customeraddresses
from django.db import models
import uuid
from utils import EncryptedTextField
from utils import *

# Create your models here.

class LedgerAccounts(models.Model):
    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('Bank', 'Bank'),
        ('Cash', 'Cash'),
    )
    ledger_account_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    is_subledger = models.BooleanField(default=False)
    ledger_group_id = models.ForeignKey(LedgerGroups, on_delete=models.CASCADE, default =None, db_column='ledger_group_id')
    inactive = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    account_no = EncryptedTextField(max_length=255)
    rtgs_ifsc_code = models.CharField(max_length=50)
    classification = models.CharField(max_length=50)
    is_loan_account = models.BooleanField(default=False)
    tds_applicable = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    pan = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):   
        return f"{self.ledger_account_id} {self.name}"
    
    class Meta:
        db_table = Ledgeraccounts 
 
# def get_customer_filename(instance, filename):
#     ext = os.path.splitext(filename)[1]
#     unique_id = uuid.uuid4().hex[:3] 
#     unique_filename = f"{os.path.splitext(filename)[0]}_{unique_id}{ext}"
#     return os.path.join('media/customers/', unique_filename)

def customer_picture(instance, filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[-1]
 
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex[:6]
 
    # Construct the filename
    branch_name = instance.name.replace(' ', '_')
    original_filename = os.path.splitext(filename)[0]  # Get the filename without extension
    return f"customers/{original_filename}_{unique_id}{file_extension}"

class Customer(models.Model):
    TAX_CHOICES = [
        ('Inclusive', 'Inclusive'),
        ('Exclusive', 'Exclusive'),
        ('Both', 'Both'),
    ]
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    print_name = models.CharField(max_length=255)
    identification = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    ledger_account_id = models.ForeignKey(LedgerAccounts, on_delete=models.CASCADE, default=None, db_column='ledger_account_id')
    customer_common_for_sales_purchase = models.BooleanField(default=False)
    is_sub_customer = models.BooleanField(default=False)
    firm_status_id = models.ForeignKey(FirmStatuses, on_delete=models.CASCADE, default=None, db_column='firm_status_id')
    territory_id = models.ForeignKey(Territory, on_delete=models.CASCADE, default=None, db_column='territory_id')
    customer_category_id = models.ForeignKey(CustomerCategories, on_delete=models.CASCADE, default=None, db_column='customer_category_id')
    contact_person = models.CharField(max_length=255)
    picture = models.ImageField(max_length=255, default=None, null=True, upload_to=customer_picture)
    gst = models.CharField(max_length=50)
    registration_date = models.DateField(auto_now_add=True)
    cin = models.CharField(max_length=50)
    pan = models.CharField(max_length=50)
    gst_category_id = models.ForeignKey(GstCategories, on_delete=models.CASCADE, db_column='gst_category_id')
    gst_suspend = models.BooleanField(default=False)
    tax_type = models.CharField(max_length=10, choices=TAX_CHOICES, default='Inclusive')
    distance = models.FloatField(null=True, blank=True)
    tds_on_gst_applicable = models.BooleanField(default=False)
    tds_applicable = models.BooleanField(default=False)
    website = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    skype = models.CharField(max_length=255)
    twitter = models.CharField(max_length=255)
    linked_in = models.CharField(max_length=255)
    payment_term_id = models.ForeignKey(CustomerPaymentTerms, on_delete=models.CASCADE, default=None, db_column='payment_term_id')
    price_category_id = models.ForeignKey(PriceCategories, on_delete=models.CASCADE, default=None, db_column='price_category_id')
    batch_rate_category = models.CharField(max_length=50)
    transporter_id = models.ForeignKey(Transporters, on_delete=models.CASCADE, default=None, db_column='transporter_id')
    credit_limit = models.DecimalField(max_digits=18, decimal_places=2)
    max_credit_days = models.PositiveIntegerField()
    interest_rate_yearly = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):   
        return f"{self.name}"
    
    class Meta:
        db_table = Customers

    @receiver(pre_delete, sender='customer.Customer')
    def delete_branches_picture(sender, instance, **kwargs):
        if instance.picture and instance.picture.name:
            file_path = instance.picture.path
            if os.path.exists(file_path):
                os.remove(file_path)
                picture_dir = os.path.dirname(file_path)
                if not os.listdir(picture_dir):
                    os.rmdir(picture_dir)
        
class CustomerAddresses(models.Model):
    ADDRESS_CHOICE = [
        ('Billing', 'Billing'),
        ('Shipping', 'Shipping')
    ]
    customer_address_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_id')
    address_type = models.CharField(max_length=10, choices=ADDRESS_CHOICE)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email= models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    route_map = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"{self.customer_address_id}"
    
    class Meta:
        db_table = Customeraddresses
    
