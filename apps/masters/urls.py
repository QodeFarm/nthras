from django.contrib import admin
#add your urls 
from django.urls import path, include
from rest_framework import routers, permissions
from .views  import *

router = routers.DefaultRouter()
router.register(r'country', CountryViewSet),
router.register(r'state', StateViewSet),
router.register(r'city', CityViewSet),
router.register(r'statuses', StatusesViewset)
router.register(r'ledger-groups', LedgerGroupsViews)
router.register(r'firm-statuses', FirmStatusesViews)
router.register(r'territory', TerritoryViews)
router.register(r'customer-categories', CustomerCategoriesViews)
router.register(r'gst-categories', GstCategoriesViews)
router.register(r'customer-payment-terms', CustomerPaymentTermsViews)
router.register(r'price-categories', PriceCategoriesViews)
router.register(r'transporters', TransportersViews)
router.register(r'product-types', ProductTypesViewSet)
router.register(r'product-unique-quantity-codes', ProductUniqueQuantityCodesViewSet)
router.register(r'unit-options', UnitOptionsViewSet)
router.register(r'product-drug-types', ProductDrugTypesViewSet)
router.register(r'product-item-type', ProductItemTypeViewSet)
router.register(r'brand-salesman', BrandSalesmanViewSet)
router.register(r'product-brands', ProductBrandsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]


