from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Color, Folder, File
admin.site.register(Folder)
admin.site.register(File)
admin.site.register(Color)
#
#
