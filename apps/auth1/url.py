from django.urls import path, include
from .views import SignUpViews
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'signup', SignUpViews, basename = 'signup')


urlpatterns = [
   path('', include(router.urls)),  
]
