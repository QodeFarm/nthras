from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  #['username', 'password_hash', 'first_name', 'last_name', 'email', 'mobile', 'otp_required', 'role_id', 'status_id', 'profile_picture_url', 'bio', 'timezone', 'language', 'date_of_birth', 'gender']
        # extra_kwargs = {
        #     'password_hash': {'write_only': True},  # Ensures password is write-only
        #     'email': {'required': False},  # Makes email field optional
        #     'mobile': {'required': True}  # Makes mobile field required
        # }

    # def create(self, validated_data):
    #     # Create and return a new user instance, given the validated data
    #     return User.objects.create_user(**validated_data)

