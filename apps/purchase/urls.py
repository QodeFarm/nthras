from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from .views  import *

router = routers.DefaultRouter()
router.register(r'purchase_orders', PurchaseOrdersViewSet)
router.register(r'purchaseorder_items', PurchaseorderItemsViewSet)
router.register(r'purchase_shipments', PurchaseShipmentsViewSet)
router.register(r'purchase_price_list', PurchasePriceListViewSet)
router.register(r'purchase_order_returns', PurchaseOrderReturnsViewSet)


urlpatterns = [
    path('', include(router.urls)),  
]