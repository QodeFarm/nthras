from django.urls import path
from django.urls.conf import include
from apps.users.views import *



urlpatterns = [
    path("djoser/", include("djoser.urls")),
    path("token/", include("djoser.urls.jwt")),
    path('login/',UserLoginView.as_view(),name='login'),
    path('role/', RoleViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='role'),
    path('modules/', ModulesViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='modules'),
    path('actions/', ActionsViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='actions'),
    path('userdata/', GetUserDataViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='userdata'),
    path('permissions/', PermissionsViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='permissions'),
    path('modulesections/', ModuleSectionsViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='modulesections'),
    path('role_permissions/', RolePermissionsViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='role_permissions'),
    

]

