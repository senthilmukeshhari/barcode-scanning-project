from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'College Lab Entry/Exit System'
admin.site.site_title = 'College Lab Entry/Exit System'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('entry_exit_app.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)