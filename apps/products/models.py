import os
import uuid
from django.db import models
from apps.masters.models import *
# from apps.customers.models import LedgerGroups
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from utils_methods import EncryptedTextField
from utils_variables import *


def product_groups_picture(instance, filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[-1]
 
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex[:6]
 
    # Construct the filename
    #branch_name = instance.name.replace(' ', '_')
    original_filename = os.path.splitext(filename)[0]  # Get the filename without extension
    return f"products/product_groups/{original_filename}_{unique_id}{file_extension}"

# Create your models here.
class ProductGroups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(max_length=255, default=None, null=True, upload_to=product_groups_picture)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = productgroupstable

    def __str__(self):
        return f"{self.group_id} {self.group_name}"

    @receiver(pre_delete, sender='products.ProductGroups')
    def delete_branches_picture(sender, instance, **kwargs):
        if instance.picture and instance.picture.name:
            file_path = instance.picture.path
            if os.path.exists(file_path):
                os.remove(file_path)
                picture_dir = os.path.dirname(file_path)
                if not os.listdir(picture_dir):
                    os.rmdir(picture_dir)



def product_categories_picture(instance, filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[-1]
 
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex[:6]
 
    # Construct the filename
    #branch_name = instance.name.replace(' ', '_')
    original_filename = os.path.splitext(filename)[0]  # Get the filename without extension
    return f"products/product_categories/{original_filename}_{unique_id}{file_extension}"

class ProductCategories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    picture = models.ImageField(max_length=255, default=None, null=True, upload_to=product_categories_picture)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = productcategoriestable

    def __str__(self):
        return f"{self.category_id} {self.category_name}"

    @receiver(pre_delete, sender='products.ProductCategories')
    def delete_branches_picture(sender, instance, **kwargs):
        if instance.picture and instance.picture.name:
            file_path = instance.picture.path
            if os.path.exists(file_path):
                os.remove(file_path)
                picture_dir = os.path.dirname(file_path)
                if not os.listdir(picture_dir):
                    os.rmdir(picture_dir)



class ProductStockUnits(models.Model):
    stock_unit_id = models.AutoField(primary_key=True)
    stock_unit_name = models.CharField(max_length=255)
    description = models.TextField()
    quantity_code_id = models.ForeignKey(ProductUniqueQuantityCodes, on_delete=models.CASCADE, null=True, default=None, db_column = 'quantity_code_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = productstockunitstable

    def __str__(self):
        return f"{self.stock_unit_id} {self.stock_unit_name}"


class ProductGstClassifications(models.Model):
    TYPE_CHOICES = [ 
        ('HSN', 'HSN'),
        ('SAC', 'SAC'),
        ('Both','Both'),
    ]
    gst_classification_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=True, null=True)
    code = models.CharField(max_length=50)
    hsn_or_sac_code = models.CharField(max_length=50)
    hsn_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = productgstclassificationstable

    def __str__(self):
        return f"{self.gst_classification_id} {self.code}"


class ProductSalesGl(models.Model):
    sales_gl_id = models.AutoField(primary_key=True)
    #ledger_group_id = models.ForeignKey(LedgerGroups, on_delete=models.CASCADE, null=True, default=None, db_column = 'ledger_group_id')
    name = models.CharField(max_length=255)
    sales_accounts = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    is_subledger = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    type = models.CharField(max_length=255)
    account_no = EncryptedTextField(max_length=255)
    rtgs_ifsc_code = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    is_loan_account = models.BooleanField(default=False)
    tds_applicable = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    pan = models.CharField(max_length=50)
    employee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_sales_gl'

    def __str__(self):
        return f"{self.sales_gl_id} {self.name}"

class ProductPurchaseGl(models.Model):
    purchase_gl_id = models.AutoField(primary_key=True)
    #ledger_group_id = models.ForeignKey(LedgerGroups, on_delete=models.CASCADE, null=True, default=None, db_column = 'ledger_group_id')
    name = models.CharField(max_length=255)
    purchase_accounts = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    is_subledger = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    type = models.CharField(max_length=255)
    account_no = EncryptedTextField(max_length=255)
    rtgs_ifsc_code = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    is_loan_account = models.BooleanField(default=False)
    tds_applicable = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    pan = models.CharField(max_length=50)
    employee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_purchase_gl'

    def __str__(self):
        return f"{self.purchase_gl_id} {self.name}"


def products_picture(instance, filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[-1]
 
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex[:6]
 
    # Construct the filename
    #branch_name = instance.name.replace(' ', '_')
    original_filename = os.path.splitext(filename)[0]  # Get the filename without extension
    return f"products/products/{original_filename}_{unique_id}{file_extension}"

class products(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Pending','Pending'),
    ]
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    #ledger_group_id = models.ForeignKey(LedgerGroups, on_delete=models.CASCADE, null=True, default=None, db_column = 'ledger_group_id')
    category_id = models.ForeignKey(ProductCategories, on_delete=models.CASCADE, null=True, default=None, db_column = 'category_id')
    type_id = models.ForeignKey(ProductTypes, on_delete=models.CASCADE, null=True, default=None, db_column = 'type_id')
    code = models.CharField(max_length=50)
    barcode = models.CharField(max_length=50)
    unit_options_id = models.ForeignKey(UnitOptions, on_delete=models.CASCADE, null=True, default=None, db_column = 'unit_options_id')
    gst_input = models.CharField(max_length=255)
    stock_unit_id = models.ForeignKey(ProductStockUnits, on_delete=models.CASCADE, null=True, default=None, db_column = 'stock_unit_id')
    print_barcode = models.BooleanField(default=False)
    gst_classification_id = models.ForeignKey(ProductGstClassifications, on_delete=models.CASCADE, null=True, default=None, db_column = 'gst_classification_id')
    picture = models.ImageField(max_length=255, default=None, null=True, upload_to=products_picture)
    sales_description = models.TextField()
    sales_gl_id = models.ForeignKey(ProductSalesGl, on_delete=models.CASCADE, null=True, default=None, db_column = 'sales_gl_id')
    mrp = models.DecimalField(max_digits=18, decimal_places=2)
    minimum_price = models.DecimalField(max_digits=18, decimal_places=2)
    sales_rate = models.DecimalField(max_digits=18, decimal_places=2)
    wholesale_rate = models.DecimalField(max_digits=18, decimal_places=2)
    dealer_rate = models.DecimalField(max_digits=18, decimal_places=2)
    rate_factor = models.DecimalField(max_digits=18, decimal_places=2)
    discount = models.DecimalField(max_digits=18, decimal_places=2)
    dis_amount = models.DecimalField(max_digits=18, decimal_places=2)
    purchase_description = models.TextField()
    purchase_gl_id = models.ForeignKey(ProductPurchaseGl, on_delete=models.CASCADE, null=True, default=None, db_column = 'purchase_gl_id')
    purchase_rate = models.DecimalField(max_digits=18, decimal_places=2)
    purchase_rate_factor = models.DecimalField(max_digits=18, decimal_places=2)
    purchase_discount = models.DecimalField(max_digits=18, decimal_places=2)
    item_type_id = models.ForeignKey(ProductItemType, on_delete=models.CASCADE, null=True, default=None, db_column = 'item_type_id')
    minimum_level = models.IntegerField()
    maximum_level = models.IntegerField()
    salt_composition = models.TextField()
    drug_type_id = models.ForeignKey(ProductDrugTypes, on_delete=models.CASCADE, null=True, default=None, db_column = 'drug_type_id')
    weighscale_mapping_code = models.CharField(max_length=50)
    brand_id = models.ForeignKey(ProductBrands, on_delete=models.CASCADE, null=True, default=None, db_column = 'brand_id')
    purchase_warranty_months = models.IntegerField()
    sales_warranty_months = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Inclusive')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = productstable

    def __str__(self):
        return f"{self.product_id} {self.name}"

    @receiver(pre_delete, sender='products.products')
    def delete_branches_picture(sender, instance, **kwargs):
        if instance.picture and instance.picture.name:
            file_path = instance.picture.path
            if os.path.exists(file_path):
                os.remove(file_path)
                picture_dir = os.path.dirname(file_path)
                if not os.listdir(picture_dir):
                    os.rmdir(picture_dir)