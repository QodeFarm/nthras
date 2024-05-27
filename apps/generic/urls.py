# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataDownloadViewSet, list_models

router = DefaultRouter()
router.register(r'download', DataDownloadViewSet, basename='download')

urlpatterns = [
    path('', include(router.urls)),
    path('list-models/', list_models, name='list-models'),
]


#http://127.0.0.1:8000/api/v1/generic/download/download/sales/SaleOrder/json/

# http://127.0.0.1:8000/api/v1/generic/list-models/