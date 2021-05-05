from django.http import HttpResponseRedirect
from django.views import generic
from gallery.forms import PhotoCreateForm
from .forms import AdvertForm
from .models import Advert, Photo
from django.contrib.auth.mixins import LoginRequiredMixin
from main.permissions import UserIsOwnerOrAdminMixin
from django.db.models import Q


class AdvertListView(generic.ListView):
    ''' Список обьявлений '''
    # queryset = Advert.objects.all()
    template_name = 'main/advertlist.html'
    context_object_name = 'adv'
    paginate_by = 4

    def get_queryset(self):
        if self.request.GET.get('val'):
            value = self.request.GET.get('val')
            queryset = Advert.objects.filter(Q(text__contains=value) | Q(title__contains=value))
        else:
            queryset = Advert.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        val = self.request.GET.get('val')
        context['search'] = val
        return context


class AdvertDetailView(LoginRequiredMixin, generic.DetailView):
    ''' Детализированная форма обьявления '''
    model = Advert
    template_name = 'main/advertdetail.html'
    context_object_name = 'adv'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        qsetAdvert = Advert.objects.values('gallery_id').filter(pk=pk)
        gallery = qsetAdvert.get().get('gallery_id')
        context = super().get_context_data(**kwargs)
        context['photo'] = Photo.objects.filter(gallery=gallery)
        context['permit'] = UserIsOwnerOrAdminMixin.has_permission(self)
        return context


class AdvertCreate(LoginRequiredMixin, generic.CreateView):
    ''' Создание нового обьявления '''
    # form_class = AdvertForm
    template_name = 'main/advertcreate.html'

    def get_form(self, form_class=AdvertForm):
        form = AdvertForm(user=self.request.user)
        return form

    def post(self, request, *args, **kwargs):
        bindform = AdvertForm(request.user, request.POST)
        post = bindform.save(commit=False)
        post.user = request.user
        post.save()
        return HttpResponseRedirect('/')


class AdvertUpdate(UserIsOwnerOrAdminMixin, generic.UpdateView):
    ''' Редактирование обьявления '''
    permission_required = 'firstproject.nge_advert'
    template_name = 'main/advertupdate.html'
    form_class = AdvertForm

    def get_queryset(self):
        queryset = Advert.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.user = self.request.user
        return form


class AdvertDelete(UserIsOwnerOrAdminMixin, generic.DeleteView):
    ''' Удаление обьявления '''
    model = Advert
    context_object_name = 'adv'
    template_name = 'main/advert_confirm_delete.html'
    success_url = '/'

class PhotoGalleryCreate(generic.CreateView):
    ''' Добавление фото в галерею '''
    template_name = 'gallery/photo_create.html'

    def get_form(self, form_class=PhotoCreateForm):
        form = PhotoCreateForm(user=self.request.user)
        return form

    def post(self, request, *args, **kwargs):
        bindform = PhotoCreateForm(request.user, request.POST, files=request.FILES)
        print('bindform.data =========>', bindform.data)
        gallery = bindform.data['gallery']
        if bindform.is_valid():
            post = bindform.save(commit=False)
            post.user = request.user
            post.save()
        else:
            print('errors ==========>', bindform.errors)
        return HttpResponseRedirect('/gallery/photolist/{}'.format(gallery))

class PhotoGalleryList(generic.ListView):
    ''' Список фотографий в галерее '''
    template_name = 'gallery/photo_list.html'
    context_object_name = 'photolist'
    paginate_by = 5

    def get_queryset(self):
        queryset = Photo.objects.filter(gallery=self.kwargs['pk'])
        return queryset

class PhotoDelete(generic.DeleteView):
    ''' Удаление фотографий из галереи '''
    model = Photo
    template_name = 'gallery/photo_delete.html'
    success_url = '/gallery/list/'


