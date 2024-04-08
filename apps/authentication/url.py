from django.contrib import admin
from django.urls import path, include
from apps.authentication.views import *

urlpatterns = [
    path('sign-in/', UserSignUpView.as_view(), name='register'),
 
]
