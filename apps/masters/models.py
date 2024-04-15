from django.db import models
from utils_methods import *
from utils_variables import *

# Create your models here.
class LedgerGroups(models.Model):
    ledger_group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    inactive = models.BooleanField(default=False)
    under_group = models.CharField(max_length=255)
    nature = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):   
        return f"{self.ledger_group_id} {self.name}"
    
    class Meta:
        db_table = ledgergroupstable
        
class FirmStatuses(models.Model):
    firm_status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):   
        return f"{self.firm_status_id} {self.name}"
    
    class Meta:
        db_table = firmstatusestable

class Territory(models.Model):
    territory_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.territory_id} {self.name}"
    
    class Meta:
        db_table = territoriestable

class CustomerCategories(models.Model):
    customer_category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer_category_id} {self.name}"
    
    class Meta:
        db_table = customercategoriestable

class GstCategories(models.Model):
    gst_category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.gst_category_id} {self.name}"
    
    class Meta:
        db_table = gstcategoriestable

class CustomerPaymentTerms(models.Model):
    payment_term_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    fixed_days = models.PositiveIntegerField()
    no_of_fixed_days = models.PositiveIntegerField()
    payment_cycle = models.CharField(max_length=255)
    run_on = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.payment_term_id} {self.name}"
    
    class Meta:
        db_table = customerpaymenttermstable

class PriceCategories(models.Model):
    price_category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.price_category_id} {self.name}"
    
    class Meta:
        db_table = pricecategoriestable

class Transporters(models.Model):
    transporter_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    gst_no = models.CharField(max_length=50)
    website_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.transporter_id} {self.name}"
    
    class Meta:
        db_table = transportertable

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
        db_table = statusestable
