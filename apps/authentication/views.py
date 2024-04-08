from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


# Create your views here.
class UserSignUpView(APIView):
    '''This view is used for user registration purpose'''
    def post(self,requst,format=None):
        return Response({"msg": "working"})