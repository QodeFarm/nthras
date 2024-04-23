from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

#add your urls

router = DefaultRouter()

router.register(r'sale_order', SaleOrderView)
router.register(r'payment_transactions', PaymentTransactionsView)
router.register(r'shipments', ShipmentsView)
router.register(r'order_items', OrderItemsView)
router.register(r'invoices', InvoicesView)
router.register(r'sales_price_list', SalesPriceListView)
router.register(r'sale_order_returns', SaleOrderReturnsView)

urlpatterns = [
    path('',include(router.urls))
]
