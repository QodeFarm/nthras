#add your urls 
# from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'ledger-accounts', LedgerAccountsViews)
router.register(r'customers', CustomersViews)
router.register(r'customer-addresses', CustomerAddressesViews)

urlpatterns = [
    path('', include(router.urls)),
    
]
