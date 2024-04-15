from django.db import models
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
