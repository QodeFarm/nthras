# myapp/urls.py
from django.urls import path
from .views import * 

urlpatterns = [
    path('get-total/', TotalView.as_view(), name='total'),
    path('process-order-items/', ProcessOrderView.as_view(), name='process-order'),
  ]
