from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'country', CountryViewSet),
router.register(r'state', StateViewSet),
router.register(r'city', CityViewSet),
router.register(r'statuses', StatusesViewset)

urlpatterns = [
    path('', include(router.urls)),
]

