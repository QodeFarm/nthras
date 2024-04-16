from djoser.serializers import UserCreateSerializer
from .models import User
import os
from django.conf import settings
from django.core.files.storage import default_storage


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('user_id', 'username', 'email', 'first_name', 'last_name', 'mobile', 'company_id', 'status_id', 'role_id', 'branch_id', 'password', 'timezone', 'profile_picture_url', 'bio', 'language', 'date_of_birth', 'gender')

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
