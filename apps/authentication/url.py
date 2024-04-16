from django.urls import path
from django.urls.conf import include


urlpatterns = [
    path("djoser/", include("djoser.urls")),
    path("token/", include("djoser.urls.jwt"))
]