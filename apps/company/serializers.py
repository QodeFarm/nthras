from rest_framework import serializers
from .models import *
from apps.masters.serializers import *
import os
from django.conf import settings
from django.core.files.storage import default_storage

class ModCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = ['company_id','name']

class ModBranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = ['branch_id','name']

class CompaniesSerializer(serializers.ModelSerializer):
    city = ModCitySerializer(source='city_id', read_only = True)
    class Meta:
        model = Companies
        fields = '__all__'

    def create(self, validated_data):
            logo = validated_data.pop('logo', None)
            instance = super().create(validated_data)
            if logo:
                instance.logo = logo
                instance.save()
            return instance
    
    def update(self, instance, validated_data):
        logo = validated_data.pop('logo', None)
        if logo:
            # Delete the previous logo file and its directory if they exist
            if instance.logo:
                logo_path = instance.logo.path
                if os.path.exists(logo_path):
                    os.remove(logo_path)
                    logo_dir = os.path.dirname(logo_path)
                    if not os.listdir(logo_dir):
                        os.rmdir(logo_dir)
            instance.logo = logo
            instance.save()
        return super().update(instance, validated_data)

class BranchesSerializer(serializers.ModelSerializer):
    company = ModCompaniesSerializer(source='company_id', read_only = True)
    status = ModStatusesSerializer(source='status_id', read_only = True)
    city = ModCitySerializer(source='city_id', read_only = True)
    state = ModStateSerializer(source='state_id', read_only = True)
    country = ModCountrySerializer(source='country_id', read_only = True)

    class Meta:
        model = Branches
        fields='__all__'

    def create(self, validated_data):
            picture = validated_data.pop('picture', None)
            instance = super().create(validated_data)
            if picture:
                instance.picture = picture
                instance.save()
            return instance
    
    def update(self, instance, validated_data):
        picture = validated_data.pop('picture', None)
        if picture:
            # Delete the previous picture file and its directory if they exist
            if instance.picture:
                picture_path = instance.picture.path
                if os.path.exists(picture_path):
                    os.remove(picture_path)
                    picture_dir = os.path.dirname(picture_path)
                    if not os.listdir(picture_dir):
                        os.rmdir(picture_dir)
            instance.picture = picture
            instance.save()
        return super().update(instance, validated_data)

class BranchBankDetailsSerializer(serializers.ModelSerializer):
    branch = ModBranchesSerializer(source='branch_id', read_only = True)
    class Meta:
        model = BranchBankDetails
        fields = '__all__'