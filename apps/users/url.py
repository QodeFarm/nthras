from djoser import views
from django.urls import path
from django.urls.conf import include
from django.contrib.auth import get_user_model
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
router.register(r"create_user", views.UserViewSet)

from djoser.views import UserViewSet

urlpatterns = [
    #path("create/", include("djoser.urls")),
    path('activation/<uid>/<token>/', UserViewSet.as_view({'post': 'activation'}), name='activation'),
    path("token/", include("djoser.urls.jwt")),
    path('change_password/',UserChangePasswordView.as_view(), name='change_password'),
    path('reset_password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset_password' ),
    path('reset_password_email/', SendPasswordResetEmailView.as_view(), name='reset_password_email'),
]
urlpatterns += router.urls

User = get_user_model()