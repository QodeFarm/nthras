from django.urls import path
from .views import VoucherView, FetchOutstandingLCView

urlpatterns = [
    path('track_order/', VoucherView.as_view(), name='voucher'),
    path('fetch-outstanding-lc/', FetchOutstandingLCView.as_view(), name='fetch-outstanding-lc'),

]
