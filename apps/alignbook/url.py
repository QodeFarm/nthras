from django.urls import path
from .views import VoucherView

urlpatterns = [
    path('track_order/', VoucherView.as_view(), name='voucher'),
]
