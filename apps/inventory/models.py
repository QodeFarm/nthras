import os
import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from utils_methods import *
from utils_variables import *

# Create your models here.
class Warehouses(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    item_type_id = models.ForeignKey('masters.ProductItemType', on_delete=models.CASCADE, null=True, default=None, db_column = 'item_type_id')
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, null=True, default=None, db_column = 'customer_id')
    address = models.CharField(max_length=255)
    city_id = models.ForeignKey('masters.City', on_delete=models.CASCADE, null=True, default=None, db_column = 'city_id')
    pin_code = models.CharField(max_length=50, null=True, default=None)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, default=None)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = warehousestable

    def __str__(self):
        return f"{self.warehouse_id} {self.name}"
		
