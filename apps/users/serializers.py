from django.core.files.storage import default_storage
from djoser.serializers import UserCreateSerializer
from apps.company.serializers import *
from apps.masters.serializers import *
from rest_framework import serializers
from django.conf import settings
from .models import Roles, Permissions, Actions, Modules, Role_Permissions, Module_Sections, User
import os

#=========================MOD_SERIALIZATION=========================
class ModRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['role_id','role_name']

class ModPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['permission_id','permission_name']

class ModRolePermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role_Permissions
        fields = ['role_permission_id','access_level']

class ModModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = ['module_id','module_name']

class ModActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actions
        fields = ['action_id','action_name']

class ModModuleSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module_Sections
        fields = ['section_id','section_name']


#=========================SERIALIZATIONS=========================
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'


class RolePermissionsSerializer(serializers.ModelSerializer):
    role = ModRoleSerializer(source='role_id', read_only = True)
    permission = ModPermissionsSerializer(source='permission_id', read_only = True)

    class Meta:
        model = Role_Permissions
        fields = '__all__'


class ActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actions
        fields = '__all__'


class ModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = '__all__'


class ModuleSectionsSerializer(serializers.ModelSerializer):
    module = ModModulesSerializer(source='module_id', read_only = True)
    class Meta:
        model = Module_Sections
        fields = '__all__'

class GetUserDataSerializer(serializers.ModelSerializer):
    company = ModCompaniesSerializer(source='company_id', read_only = True)
    branch = ModBranchesSerializer(source='branch_id', read_only = True)
    role = ModRoleSerializer(source='role_id', read_only = True)
    status = ModStatusesSerializer(source='status_id', read_only = True)
    class Meta:
        model = User
        fields = ['user_id','username','first_name','last_name','email','mobile','otp_required','profile_picture_url','bio','timezone','language','created_at','updated_at','last_login','date_of_birth','gender','is_active','company_id','status_id','role_id','branch_id', 'branch','status','company','role']  
    
 
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'

    '''CURD Operations For Profile Picture'''
    def create(self, validated_data):
            profile_picture_url = validated_data.pop('profile_picture_url', None)
            instance = super().create(validated_data)
            if profile_picture_url:
                instance.profile_picture_url = profile_picture_url
                instance.save()
            return instance
    
    def update(self, instance, validated_data):
        profile_picture_url = validated_data.pop('profile_picture_url', None)
        if profile_picture_url:
            # Delete the previous picture file and its directory if they exist
            if instance.profile_picture_url:
                picture_path = instance.profile_picture_url.path
                if os.path.exists(picture_path):
                    os.remove(picture_path)
                    picture_dir = os.path.dirname(picture_path)
                    if not os.listdir(picture_dir):
                        os.rmdir(picture_dir)
            instance.profile_picture_url = profile_picture_url
            instance.save()
        return super().update(instance, validated_data)