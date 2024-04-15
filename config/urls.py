from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/company/', include('apps.company.urls')),
    path('api/v1/masters/', include('apps.masters.urls'))

]
#below will handle media files uploaded when instance is created.

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 