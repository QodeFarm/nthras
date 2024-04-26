from django.shortcuts import render
from rest_framework import viewsets
from .models import Companies, Branches, BranchBankDetails
from .serializers import CompaniesSerializer, BranchesSerializer, BranchBankDetailsSerializer
from utils_methods import list_all_objects, create_instance, update_instance
from utils_variables import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import CompanyFilter
from django.db.models import  Max, Min, Sum
from rest_framework.response import Response

class CompaniesViewSet(viewsets.ModelViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = CompanyFilter
    ordering_fields = ['num_employees', 'created_at', 'updated_at', 'name']

    def list(self, request, *args, **kwargs):
        max_employees = request.query_params.get('max_num_employees', None)
        min_employees = request.query_params.get('min_num_employees', None)
        companies_per_city = request.query_params.get('companies_per_city', None)
        sum_employees_country = request.query_params.get('sum_employees_per_country', None)
        name = request.query_params.get('name', None)  # Retrieve the name parameter
        
        # Initialize response_data
        response_data = {}
        
        # Filter queryset by name if provided
        filtered_queryset = self.queryset
        if name:
            filtered_queryset = filtered_queryset.filter(name__icontains=name)

        # Here it handles the max_num_employees filter
        if max_employees == 'true':
            max_num_employees = filtered_queryset.aggregate(Max('num_employees'))
            response_data['max_num_employees'] = {
                'value': max_num_employees.get('num_employees__max'),
                'filter': name
            }

        # Here it handles the min_num_employees filter
        if min_employees == 'true':
            min_num_employees = filtered_queryset.aggregate(Min('num_employees'))
            response_data['min_num_employees'] = {
                'value': min_num_employees.get('num_employees__min'),
                'filter': name
            }

        # Here it handles the companies_per_city filter
        if companies_per_city:
            total_companies = filtered_queryset.filter(city_id__city_name=companies_per_city).count()
            response_data['total_companies_in_city'] = {
                'value': total_companies,
                'filter': name
            }

        # Here it handles the sum_employees_per_country filter
        if sum_employees_country:
            total_employees = filtered_queryset.filter(
                city_id__state_id__country_id__country_name=sum_employees_country
            ).aggregate(total_employees=Sum('num_employees'))
            response_data['total_employees_in_country'] = {
                'value': total_employees.get('total_employees'),
                'filter': name
            }
            
        # If any aggregations were added or if no specific aggregation query was provided, return them
        if response_data:
            return Response(response_data)

        # If no specific aggregation query was provided and no name filter, list all objects using your custom method
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class BranchesViewSet(viewsets.ModelViewSet):
    queryset = Branches.objects.all()
    serializer_class = BranchesSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
class BranchBankDetailsViewSet(viewsets.ModelViewSet):
    queryset = BranchBankDetails.objects.all()
    serializer_class = BranchBankDetailsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)