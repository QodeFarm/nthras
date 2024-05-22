"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from config import settings
from config.views import api_links


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('apps.users.url')),
    path('api/v1/company/', include('apps.company.urls')),
    path('api/v1/customers/', include('apps.customer.urls')),
    path('api/v1/vendor/', include('apps.vendor.urls')),
    path('api/v1/company/', include('apps.company.urls')),
    path('api/v1/masters/', include('apps.masters.urls')),
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/sales/', include('apps.sales.urls')),
    path('api/v1/customer/', include('apps.customer.urls')),
    path('api/v1/inventory/', include('apps.inventory.urls')),
    path('api/v1/purchase/', include('apps.purchase.urls')),
    path('api/v1/per_val/', include('apps.per_val.url')),
    path('', api_links, name='api_links'),
]

#below will handle media files uploaded when instance is created.

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

