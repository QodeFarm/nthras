# myapp/urls.py
from django.urls import path
from .views import * 

urlpatterns = [
    path('get_total/', TotalView.as_view(), name='total'),
    path('process_order_items/', ProcessOrderView.as_view(), name='process_order'),
  ]
