from django.db import models

# Create your models here.

class LedgerGroups(models.Model):
    ledger_group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    inactive = models.BooleanField(default=False)
    under_group = models.CharField(max_length=255)
    nature = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):   
        return f"{self.ledger_group_id} {self.name}"
    
    class Meta:
        db_table = 'ledger_groups'
        
class FirmStatuses(models.Model):
    firm_status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):   
        return f"{self.firm_status_id} {self.name}"
    
    class Meta:
        db_table = 'firm_statuses'

class Territory(models.Model):
    territory_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.territory_id} {self.name}"
    
    class Meta:
        db_table = 'territory'

class CustomerCategories(models.Model):
    customer_category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer_category_id} {self.name}"
    
    class Meta:
        db_table = 'customer_categories'

class GstCategories(models.Model):
    gst_category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.gst_category_id} {self.name}"
    
    class Meta:
        db_table = 'gst_categories'

class CustomerPaymentTerms(models.Model):
    payment_term_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    fixed_days = models.PositiveIntegerField()
    no_of_fixed_days = models.PositiveIntegerField()
    payment_cycle = models.CharField(max_length=255)
    run_on = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.payment_term_id} {self.name}"
    
    class Meta:
        db_table = 'customer_payment_terms'

class PriceCategories(models.Model):
    price_category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.price_category_id} {self.name}"
    
    class Meta:
        db_table = 'price_categories'

class Transporters(models.Model):
    transporter_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    gst_no = models.CharField(max_length=50)
    website_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transporter_id} {self.name}"
    
    class Meta:
        db_table = 'transporters'