from django.db import models
from django.urls import reverse
from django.contrib.auth.admin import User


def get_path_image(uname, iname):
    ''' Тут формирую имя файла картинки.
     К имени спереди - добавляю путь - папку, с именем пользователя, где будет
     храниться картинка. Если этого не делать, то все фотографии будут в одной папке.'''
    path = str(uname).lower() + '/' + str(iname)
    return path


class Gallery(models.Model):
    ''' Модель Gallery, для хранения информации
     с размером в два поля
    '''
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Описание', max_length=70, blank=True, null=True)

    class Meta:
        ordering = ['title']

    def get_detailUrl(self):
        return reverse('gallery_update', kwargs={'pk': self.pk})

    def get_deleteUrl(self):
        return reverse('gallery_delete', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Advert(models.Model):
    '''
    Модель Advert, для хранения информации рекламного
    обьявления
    '''
    title = models.CharField(verbose_name='заглавие', max_length=50)
    text = models.TextField(verbose_name='Текст обьявления', null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=15, null=True, blank=True)
    email = models.EmailField(verbose_name='правильный Email-адрес', max_length=30, null=True)
    date = models.DateTimeField(auto_now_add=True)
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Обьявление'
        verbose_name_plural = 'Обьявления'
        ordering = ['-date']

    def get_detailUrl(self):
        return reverse('adv_detail', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('adv_list')

    def get_UpdateUrl(self):
        return reverse('adv_update', kwargs={'pk': self.pk})

    def get_DeleteUrl(self):
        return reverse('adv_delete', kwargs={'pk': self.pk})


class Photo(models.Model):
    '''
    Модель Photo, для хранения информации о
    фотографиях
    '''
    title = models.CharField(verbose_name='Описание', max_length=30, blank=True, null=True)
    image = models.ImageField(verbose_name='Фотография', upload_to='gallery/')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['user','gallery','title']

    def save(self, *args, **kwargs):
        ''' Переопределяю метод save чтобы изменить значения image.name '''
        self.image.name = get_path_image(self.user, self.image.name)
        super().save(*args, **kwargs)

    def get_PhotodeleteUrl(self):
        return reverse('photo_delete', kwargs={'pk':self.pk})

    def __str__(self):
        return self.title
