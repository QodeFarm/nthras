from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from .views  import *

router = routers.DefaultRouter()
router.register(r'warehouses', WarehousesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]