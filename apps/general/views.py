from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

class CompaniesViewSet(viewsets.ModelViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer

class BranchesViewSet(viewsets.ModelViewSet):
    queryset = Branches.objects.all()
    serializer_class = BranchesSerializer

class BranchBankDetailsViewSet(viewsets.ModelViewSet):
    queryset = BranchBankDetails.objects.all()
    serializer_class = BranchBankDetailsSerializer