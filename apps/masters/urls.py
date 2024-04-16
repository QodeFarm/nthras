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


