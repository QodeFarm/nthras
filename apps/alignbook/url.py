from django.urls import path
from .views import VoucherView, FetchOutstandingLCView

urlpatterns = [
    path('track_order/', VoucherView.as_view(), name='voucher'),
    path('account_ledger/', FetchOutstandingLCView.as_view(), name='account_ledger'),

]
