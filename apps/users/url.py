from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from apps.users.views import RoleViewSet, ModulesViewSet, ActionsViewSet, GetUserDataViewSet, PermissionsViewSet, ModuleSectionsViewSet, RolePermissionsViewSet, SendPasswordResetEmailView, UserChangePasswordView, UserPasswordResetView

router = DefaultRouter()

router.register(r'role', RoleViewSet, basename='role')
router.register(r'modules', ModulesViewSet, basename='modules')
router.register(r'actions', ActionsViewSet, basename='actions')
router.register(r'userdata', GetUserDataViewSet, basename='userdata')
router.register(r'permissions', PermissionsViewSet, basename='permissions')
router.register(r'module_sections', ModuleSectionsViewSet, basename='module_sections')
router.register(r'role_permissions', RolePermissionsViewSet, basename='role_permissions')

urlpatterns = [
    path("djoser/", include("djoser.urls")),
    path("token/", include("djoser.urls.jwt")),
    path('change_password/',UserChangePasswordView.as_view(), name='change_password'),
    path('reset_password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset_password' ),
    path('reset_password_email/', SendPasswordResetEmailView.as_view(), name='reset_password_email'),
]
urlpatterns += router.urls
