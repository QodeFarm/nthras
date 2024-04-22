from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from .views  import *

router = routers.DefaultRouter()
router.register(r'purchase-orders', PurchaseOrdersViewSet)
router.register(r'purchaseorder-items', PurchaseorderItemsViewSet)
router.register(r'purchase-shipments', PurchaseShipmentsViewSet)

urlpatterns = [
    path('', include(router.urls)),  
]