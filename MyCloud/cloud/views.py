from rest_framework import generics, mixins
from .serializers import *
from rest_framework.permissions import *


class FolderContextView(generics.ListCreateAPIView):
    """
    Спискок всех подпапок текущей папки.
    list проверяет пренадлежность записи к текущему пользователю.
    """

    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = ForlderSerializer

    def is_owner(self):
        if folder := self.queryset.filter(id=self.kwargs['pk']).first():
            if folder.user == self.request.user:
                return True

    def list(self, request, *args, **kwargs):
        if self.is_owner():
            return super().list(request, *args, **kwargs)
        raise Http404

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(parent=self.kwargs['pk'])


class FolderUDVIew(mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):

    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = ForlderSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class MainFolderView(generics.ListCreateAPIView):
    """
    Cписок папок которые не имеют родителей
    """

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user, parent_id=None)

    queryset = Folder.objects.all()
    serializer_class = ForlderSerializer


class FolderListCreateView(generics.ListCreateAPIView):
    pass
