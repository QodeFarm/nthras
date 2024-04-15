

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
path('',include('djoser.urls')),
#path('auth/',include('djoser.urls.jwt')),

]
