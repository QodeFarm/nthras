from django.core.files.storage import default_storage
from djoser.serializers import UserCreateSerializer
from apps.company.serializers import *
from apps.masters.serializers import *
from rest_framework import serializers
from django.conf import settings
from .models import Roles, Permissions, Actions, User
import os

class ModRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['role_id','role_name']

class ModPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['permission_id','permission_name']

class ModActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actions
        fields = ['action_id','action_name']



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'


class ActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actions
        fields = '__all__'


class UserCreateSerializer(UserCreateSerializer):
    company = ModCompaniesSerializer(source='company_id', read_only = True)
    branch = ModBranchesSerializer(source='branch_id', read_only = True)
    role = ModRoleSerializer(source='role_id', read_only = True)
    status = ModStatusesSerializer(source='status_id', read_only = True)    
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__' #['user_id', 'username', 'email', 'first_name', 'last_name', 'mobile', 'company_id', 'status_id', 'role_id', 'branch_id', 'password', 'timezone', 'profile_picture_url', 'bio', 'language', 'date_of_birth', 'gender']

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