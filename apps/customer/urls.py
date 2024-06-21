#add your urls 
# from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'ledger_accounts', LedgerAccountsViews)
router.register(r'customers', CustomerViews)
router.register(r'customers_addresses', CustomerAddressesViews)
router.register(r'customers_attachments', CustomerAttachmentsViews)

urlpatterns = [
    path('', include(router.urls)),
    path('customer/', CustomerCreateViews.as_view(), name='customers-create'),
    path('customer/<str:pk>/', CustomerCreateViews.as_view(), name='customers-details'),    
]
