from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Gallery
from django.http import HttpResponseRedirect
from .forms import GalleryForm

class GalleryCreateView(generic.CreateView):
    ''' Добавление галереи '''
    template_name = 'gallery/gallery_create.html'
    form_class = GalleryForm

    def post(self, request, *args, **kwargs):
        bindform = GalleryForm(request.POST)
        post = bindform.save(commit=False)
        post.user = request.user
        post.save()
        return HttpResponseRedirect('/gallery/list')

class GalleryListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'gallery'
    template_name = 'gallery/gallery_list.html'
    paginate_by = 1

    def get_queryset(self):
        queryset = Gallery.objects.filter(user=self.request.user)
        return queryset

class GalleryUpdateView(generic.UpdateView):
    template_name = 'gallery/gallery_update.html'
    form_class = GalleryForm
    context_object_name = 'gallery'
    success_url = '/gallery/list'

    def get_queryset(self):
        queryset = Gallery.objects.filter(pk=self.kwargs['pk'])
        return queryset

class GalleryDeleteView(generic.DeleteView):
    model = Gallery
    context_object_name = 'gallery'
    template_name = 'gallery/gallery_delete.html'
    success_url = '/gallery/list'
