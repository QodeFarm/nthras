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
    path('customer-order/', TestCustomerCreateViews.as_view(), name='customer-order-create'),
    path('customer-order/<str:pk>/', TestCustomerCreateViews.as_view(), name='customer-order-details'),    
]
