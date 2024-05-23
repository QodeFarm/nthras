# myapp/urls.py
from django.urls import path
from .views import * 

urlpatterns = [
    path('total/', TotalView.as_view(), name='total'),
    path('product-details/', ProductDetailsView.as_view(), name='product-details')
  ]
