from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_name', 'last_name'
    )
''' Подключаем нашу модель Profile к админке '''
