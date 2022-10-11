from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class FolderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Folder
        fields = ('id', 'label', 'parent', 'color', 'user', )

class FileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = File
        fields = ('id', 'label', 'filesize', 'messages', 'date', 'folder_id', 'user', )
