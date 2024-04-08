from rest_framework import serializers
from authentication.models import User

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','user_id','branch_id','company_id','username','first_name','last_name','mobile','otp_required','role_id','status_id','profile_picture_url','bio','timezone','language','created_at','updated_at','last_login','date_of_birth','gender']
