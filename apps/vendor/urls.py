from django.urls import path, include
from .views import VendorsView, VendorCategoryView, VendorPaymentTermsView, VendorAgentView, VendorAttachmentView, VendorAddressView
from rest_framework.routers import DefaultRouter

#add your urls 

router = DefaultRouter()
router.register(r'vendor', VendorsView)
router.register(r'vendor-category', VendorCategoryView)
router.register(r'vendor-payment-terms', VendorPaymentTermsView)
router.register(r'vendor-agent', VendorAgentView)
router.register(r'vendor-attachment', VendorAttachmentView)
router.register(r'vendor-address', VendorAddressView)

urlpatterns = [
    path('',include(router.urls))
]
