from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from .views  import *

router = routers.DefaultRouter()
router.register(r'product_types', ProductTypesViewSet)
router.register(r'product_unique_quantity_codes', ProductUniqueQuantityCodesViewSet)
router.register(r'unit_options', UnitOptionsViewSet)
router.register(r'product_drug_types', ProductDrugTypesViewSet)
router.register(r'product_item_type', ProductItemTypeViewSet)
router.register(r'brand_salesman', BrandSalesmanViewSet)
router.register(r'product_brands', ProductBrandsViewSet)

urlpatterns = [
    path('', include(router.urls)),  
]