from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
   # path('user/', include('apps.authentication.url')),
    path('user/', include('apps.auth1.url'))


]
