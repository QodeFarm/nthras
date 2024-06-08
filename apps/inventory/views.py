from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from config.utils_methods import *
from config.utils_variables import *

# Create your views here.
class WarehousesViewSet(viewsets.ModelViewSet):
    queryset = Warehouses.objects.all()
    serializer_class = WarehousesSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)