from django.urls import path
from django.urls.conf import include
from apps.authentication.views import *



urlpatterns = [
    path("djoser/", include("djoser.urls")),
    path("token/", include("djoser.urls.jwt")),
    path('role/', RoleViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='role'),
    path('permissions/', PermissionsViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='permissions'),
    path('role_permissions/', RolePermissionsViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='role_permissions'),
    path('actions/', ActionsViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='actions'),
    path('modules/', ModulesViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='modules'),
]

