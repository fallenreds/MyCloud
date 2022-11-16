from django.db import models
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
user = get_user_model()


class Color(models.Model):
    """Модель цветов папок"""
    color = models.TextField('Цвет папки', max_length=100)

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class Folder(MPTTModel):
    """Модель папок"""
    label = models.TextField('Название', max_length=100)
    user = models.ForeignKey(
        user,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    parent = TreeForeignKey(
        'self',
        verbose_name="Родительская папка",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    color = models.ForeignKey(
        Color,
        verbose_name="Цвет папки",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'


class File(models.Model):
    """Модель файлов"""
    label = models.TextField('Название', max_length=100)
    filesize = models.PositiveIntegerField('Размер файла', default=1)
    messages = models.TextField('Ccылки на чанки в ТГ', max_length=500, null=True, blank=True)
    date = models.DateTimeField('Дата создания', default=timezone.now)
    user = models.ForeignKey(
        user,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    folder = models.ForeignKey(
        Folder,
        verbose_name='Папка',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'