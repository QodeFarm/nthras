from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

#add your urls

router = DefaultRouter()
router.register(r'sale-types', SaleTypesView)
router.register(r'sale-order', SaleOrderView)
router.register(r'shipping-modes', ShippingModesView)
router.register(r'gst-types', GstTypesView)
router.register(r'shipping-companies', ShippingCompaniesView)
router.register(r'payment-transactions', PaymentTransactionsView)
router.register(r'shipments', ShipmentsView)
router.register(r'order-items', OrderItemsView)
router.register(r'invoices', InvoicesView)
router.register(r'sales-price-list', SalesPriceListView)
router.register(r'sale-order-returns', SaleOrderReturnsView)

urlpatterns = [
    path('',include(router.urls))
]
