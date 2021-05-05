from django.urls import path
from django.http import HttpResponse
from .views import AdvertListView, AdvertDetailView, AdvertCreate, AdvertUpdate, AdvertDelete

def testView(request):
    '''
    Тестовый метод для проверки запуска тестовой
    страницы
    '''
    return HttpResponse('<div align="center"><h1 style="color:blue">Это тестовая страница!</h1></div>')

urlpatterns=[
    path('', AdvertListView.as_view(), name='adv_list'),
    path('detail/<int:pk>', AdvertDetailView.as_view(), name='adv_detail'),
    path('create/', AdvertCreate.as_view(), name='adv_create'),
    path('update/<int:pk>', AdvertUpdate.as_view(), name='adv_update'),
    path('delete/<int:pk>', AdvertDelete.as_view(), name='adv_delete'),


]