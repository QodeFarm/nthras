import os
import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from utils_methods import *
from utils_variables import *

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)

    def __str__(self):
        return self.country_name
    
    class Meta:
        db_table = countrytable

class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, default=None, db_column = 'country_id')
    state_name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.state_name
    
    class Meta:
        db_table = statetable

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    state_id = models.ForeignKey(State, on_delete=models.CASCADE, null=True, default=None, db_column = 'state_id')
    city_name = models.CharField(max_length=100)
    city_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city_name
    
    class Meta:
        db_table = citytable


class Statuses(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.status_name}"
    
    class Meta:
        db_table = 'statuses'

class ProductTypes(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = producttypestable

    def __str__(self):
        return f"{self.type_id} {self.type_name}"

class ProductUniqueQuantityCodes(models.Model):
    quantity_code_id = models.AutoField(primary_key=True)
    quantity_code_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = productuniquequantitycodestable

    def __str__(self):
        return f"{self.quantity_code_id} {self.quantity_code_name}"

class UnitOptions(models.Model):
    unit_options_id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = unitoptionstable

    def __str__(self):
        return f"{self.unit_options_id} {self.unit_name}"

class ProductDrugTypes(models.Model):
    drug_type_id = models.AutoField(primary_key=True)
    drug_type_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = productdrugtypestable

    def __str__(self):
        return f"{self.drug_type_id} {self.drug_type_name}"

class ProductItemType(models.Model):
    item_type_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = productitemtypetable

    def __str__(self):
        return f"{self.item_type_id} {self.item_name}"

class BrandSalesman(models.Model):
    RATE_ON_CHOICES = [ 
        ('Qty', 'Qty'),
        ('Amount', 'Amount'),
        ('Both','Both'),
    ]
    brand_salesman_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    commission_rate = models.DecimalField(max_digits=18, decimal_places=2)
    rate_on = models.CharField(max_length=10, choices=RATE_ON_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = brandsalesmantable

    def __str__(self):
        return f"{self.brand_salesman_id} {self.name}"


def product_brands_picture(instance, filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[-1]
 
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex[:6]
 
    # Construct the filename
    #branch_name = instance.name.replace(' ', '_')
    original_filename = os.path.splitext(filename)[0]  # Get the filename without extension
    return f"products/product_brands/{original_filename}_{unique_id}{file_extension}"

class ProductBrands(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    picture = models.ImageField(max_length=255, default=None, null=True, upload_to=product_brands_picture)
    brand_salesman_id = models.ForeignKey(BrandSalesman, on_delete=models.CASCADE, null=True, default=None, db_column='brand_salesman_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = productbrandstable

    def __str__(self):
        return f"{self.brand_id} {self.brand_name}"

    @receiver(pre_delete, sender='masters.ProductBrands')
    def delete_branches_picture(sender, instance, **kwargs):
        if instance.picture and instance.picture.name:
            file_path = instance.picture.path
            if os.path.exists(file_path):
                os.remove(file_path)
                picture_dir = os.path.dirname(file_path)
                if not os.listdir(picture_dir):
                    os.rmdir(picture_dir)