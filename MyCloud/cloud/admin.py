from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Folder, File, Color

admin.site.register(Folder)
admin.site.register(File)
admin.site.register(Color)


