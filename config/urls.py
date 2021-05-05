from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('gallery/', include('gallery.urls')),
    path('', include('main.urls')), #подключаем файл urls.py из приложения main

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)