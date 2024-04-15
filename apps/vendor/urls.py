from django.urls import path, include
from .views import VendorsView, VendorCategoryView, VendorPaymentTermsView, VendorAgentView, VendorAttachmentView, VendorAddressView
from rest_framework import routers

#add your urls 

router = routers.DefaultRouter()
router.register(r'vendor', VendorsView)
router.register(r'vendor_category', VendorCategoryView)
router.register(r'vendor_payment_terms', VendorPaymentTermsView)
router.register(r'vendor_agent', VendorAgentView)
router.register(r'vendor_attachment', VendorAttachmentView)
router.register(r'vendor_address', VendorAddressView)

urlpatterns = [
    path('',include(router.urls))
]
