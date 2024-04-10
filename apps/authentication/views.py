from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.authentication.serializers import UserSignUpSerializer

# Create your views here.
class UserSignUpView(APIView):
    '''This view is used for user registration purpose'''
    def post(self,request,format=None):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg':'registration Successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)