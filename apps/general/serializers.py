from rest_framework import serializers
from .models import *
from apps.masters.serializers import Mod_StatusesSerializer
import os

class Mod_CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = ['company_id','name']

class Mod_BranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = ['branch_id','name']

class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = '__all__'

class BranchesSerializer(serializers.ModelSerializer):
    company = Mod_CompaniesSerializer(source='company_id', read_only = True)
    statuses = Mod_StatusesSerializer(source='status_id', read_only = True)
    class Meta:
        model = Branches
        fields='__all__'
    
    def update(self, instance, validated_data):
        #Here it is Checking if 'picture' is present in the validated data and if it's None
        if 'picture' in validated_data:
            if validated_data['picture'] is None:
                #Here it is Retrieving the current value of 'picture' from the instance
                validated_data['picture'] = instance.picture
            else:
                #Here it is Deleting the previous picture file and its directory if they exist
                if instance.picture:
                    #Here it is Assuming 'instance.picture.path' contains the file path
                    picture_path = instance.picture.path
                    if os.path.exists(picture_path):
                        os.remove(picture_path)
                        # Remove the directory containing the picture
                        picture_dir = os.path.dirname(picture_path)
                        os.rmdir(picture_dir)
        
        # Call the parent class's update method to perform the update
        return super().update(instance, validated_data)

class BranchBankDetailsSerializer(serializers.ModelSerializer):
    branch = Mod_BranchesSerializer(source='branch_id', read_only = True)
    class Meta:
        model = BranchBankDetails
        fields = '__all__'