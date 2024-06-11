from djoser import views
from django.urls import path
from django.urls.conf import include
from djoser.views import UserViewSet
from rest_framework_simplejwt import views as jwtview
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
from apps.users.views import RoleViewSet, ModulesViewSet, ActionsViewSet, GetUserDataViewSet, ModuleSectionsViewSet, RolePermissionsViewSet, SendPasswordResetEmailView, UserChangePasswordView, UserPasswordResetView, UserTimeRestrictionsViewSet, UserAllowedWeekdaysViewSet, UserLoginView, UserRoleViewSet
router = DefaultRouter()

router.register(r"create_user", views.UserViewSet)
router.register(r'role', RoleViewSet, basename='role')
router.register(r'modules', ModulesViewSet, basename='modules')
router.register(r'actions', ActionsViewSet, basename='actions')
router.register(r'userdata', GetUserDataViewSet, basename='userdata')
router.register(r'module_sections', ModuleSectionsViewSet, basename='module_sections')

router.register(r'user_time_restrictions', UserTimeRestrictionsViewSet, basename='user_time_restrictions')
router.register(r'user_allowed_weekday', UserAllowedWeekdaysViewSet, basename='user_allowed_weekday')

router.register(r'user_roles', UserRoleViewSet, basename='user_role')  
router.register(r'role_permissions', RolePermissionsViewSet, basename='role_permissions')

urlpatterns = [
    path('activation/<uid>/<token>/', UserViewSet.as_view({'post': 'activation'}), name='activation'),
    path("login/", UserLoginView.as_view(), name="User_Login_View"),
    path("jwt/refresh/", jwtview.TokenRefreshView.as_view(), name="get_access_token"),
    path("jwt/verify/", jwtview.TokenVerifyView.as_view(), name="jwt_verify"),
    path('change_password/',UserChangePasswordView.as_view(), name='change_password'),
    path('reset_password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset_password' ),
    path('reset_password_email/', SendPasswordResetEmailView.as_view(), name='reset_password_email'),
]
urlpatterns  += router.urls

User = get_user_model()