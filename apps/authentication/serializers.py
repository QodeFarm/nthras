from rest_framework import serializers
from apps.authentication.models import User

class UserSignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only = True)
    class Meta:
        model = User
       # fields = ['email','username','password','password2','user_id','branch_id','company_id','first_name','last_name','mobile','otp_required','role_id','status_id','profile_picture_url','bio','timezone','language','created_at','updated_at','last_login','date_of_birth','gender']
        fields = ['email', 'username','password','password2']
        extra_kwargs={
            'password' : {'write_only':True}
        }
    #validate password and password2 are same or not
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password & Confirm Password Doesn't Match.")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
