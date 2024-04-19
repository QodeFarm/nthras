from .serializers import RoleSerializer, PermissionsSerializer, ActionsSerializer, ModulesSerializer, RolePermissionsSerializer, ModuleSectionsSerializer, GetUserDataSerializer
from .models import Roles, Permissions, Actions, Modules, Role_Permissions, Module_Sections, User
from rest_framework import viewsets
from django.shortcuts import render
from utils_methods import *
# from rest_framework.decorators import permission_classes 
# from rest_framework.permissions import IsAuthenticated
# @permission_classes([IsAuthenticated])
# Create your views here.
class GetUserDataViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserDataSerializer
    

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)
        

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    

class PermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    

class RolePermissionsViewSet(viewsets.ModelViewSet):
    queryset = Role_Permissions.objects.all()
    serializer_class = RolePermissionsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)


class ActionsViewSet(viewsets.ModelViewSet):
    queryset = Actions.objects.all()
    serializer_class = ActionsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    

class ModulesViewSet(viewsets.ModelViewSet):
    queryset = Modules.objects.all()
    serializer_class = ModulesSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    

class ModuleSectionsViewSet(viewsets.ModelViewSet):
    queryset = Module_Sections.objects.all()
    serializer_class = ModuleSectionsSerializer

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    
#=================================================================
from rest_framework_simplejwt.tokens import RefreshToken

# Creating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'username': user.username,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

from rest_framework.views import APIView
from .serializers import UserLoginSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({"status": True, "message": 'Login Success', "token": token}, status=status.HTTP_200_OK)
        else:
            return Response({"errors": {'non_field_errors': ['Username or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)

