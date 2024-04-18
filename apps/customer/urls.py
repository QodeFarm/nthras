#add your urls 
# from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'ledger-accounts', LedgerAccountsViews)
router.register(r'customers', CustomerViews)
router.register(r'customer-addresses', CustomerAddressesViews)
router.register(r'customer-attachments', CustomerAttachmentsViews)

urlpatterns = [
    path('', include(router.urls)),
    
]
