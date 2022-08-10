from django.db import models
from django.utils import timezone

class Folder(models.Model):
    "Папки"
    label = models.TextField('Название',max_length=100)