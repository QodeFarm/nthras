from django.urls import path, include
from rest_framework import routers
from .views import CompaniesViewSet, BranchesViewSet, BranchBankDetailsViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompaniesViewSet),
router.register(r'branches', BranchesViewSet),
router.register(r'branchbankdetails', BranchBankDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]