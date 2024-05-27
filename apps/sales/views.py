import json
from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from rest_framework import viewsets, status
from .serializers import *
from utils_methods import list_all_objects,create_instance,update_instance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import SaleOrderFilter,InvoicesFilter,PaymentTransactionsFilter,OrderItemsFilter,ShipmentsFilter,SalesPriceListFilter,SaleOrderReturnsFilter
# Create your views here.

from rest_framework.decorators import action, api_view
    

class SaleOrderView(viewsets.ModelViewSet):
    queryset = SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SaleOrderFilter
    ordering_fields = ['num_employees', 'created_at', 'updated_at', 'name']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     print(queryset.query)
    #     return queryset
    
    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    

    # @action(detail=False, methods=['get'], url_path=r'download/(?P<file_format>[^/.]+)')
    # def download_data(self, request, app_label=None, model_name=None, file_format=None):
    #     try:
    #         queryset = self.queryset
    #         serializer = self.serializer_class(queryset, many=True)
    #         data = serializer.data


    #         if file_format == 'json':
    #             serializer = self.serializer_class(queryset, many=True)
    #             data = serializer.data
                
    #             # Serialize the data to JSON
    #             formatted_data = json.dumps(serializer.data, indent=4)

    #             # Set the Content-Disposition header to force download
    #             response = HttpResponse(formatted_data, content_type='application/json')
    #             response['Content-Disposition'] = f'attachment; filename="{model_name}.json"'
    #             return response
            
    #     except ValueError as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class PaymentTransactionsView(viewsets.ModelViewSet):
    queryset = PaymentTransactions.objects.all()
    serializer_class = PaymentTransactionsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = PaymentTransactionsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class InvoicesView(viewsets.ModelViewSet):
    queryset = Invoices.objects.all()
    serializer_class = InvoicesSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = InvoicesFilter
    ordering_fields = []


    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class OrderItemsView(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = OrderItemsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class ShipmentsView(viewsets.ModelViewSet):
    queryset = Shipments.objects.all()
    serializer_class = ShipmentsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = ShipmentsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SalesPriceListView(viewsets.ModelViewSet):
    queryset = SalesPriceList.objects.all()
    serializer_class = SalesPriceListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SalesPriceListFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)

class SaleOrderReturnsView(viewsets.ModelViewSet):
    queryset = SaleOrderReturns.objects.all()
    serializer_class = SaleOrderReturnsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = SaleOrderReturnsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    