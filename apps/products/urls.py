from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from .views  import *

router = routers.DefaultRouter()
router.register(r'product-groups', ProductGroupsViewSet)
router.register(r'product-categories', ProductCategoriesViewSet)
router.register(r'product-stock-units', ProductStockUnitsViewSet)
router.register(r'product-gst-classifications', ProductGstClassificationsViewSet)
router.register(r'product-sales-gl', ProductSalesGlViewSet)
router.register(r'product-purchase-gl', ProductPurchaseGlViewSet)
router.register(r'products', productsViewSet)

urlpatterns = [
    path('', include(router.urls)),  
]