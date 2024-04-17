from django.urls import path
from django.urls.conf import include
from apps.authentication.views import *



urlpatterns = [
    path("djoser/", include("djoser.urls")),
    path("token/", include("djoser.urls.jwt")),
    path('role/', RoleViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='role'),
]