from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class ForlderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Folder
        fields = ('id', 'label', 'parent', 'color', 'user')
