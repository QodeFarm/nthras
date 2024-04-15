#add your urls 
from django.urls import path, include
from rest_framework import routers
from .views import *

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



urlpatterns = [
    path('', include(router.urls)),
    
]


