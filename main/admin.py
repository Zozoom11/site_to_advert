from django.contrib import admin
from .models import Advert, Photo, Gallery
''' Нужно импортировать модели, чтобы они были тут доступны '''

@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    search_fields = ['title', 'text', 'email']
    list_filter = ('user',)
''' Подключаем нашу модель Advert к админке '''

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ('gallery',)
''' Подключаем нашу модель Photo к админке '''

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ('user',)
''' Подключаем нашу модель Gallery к админке '''
