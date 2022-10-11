from rest_framework import generics, mixins
from .serializers import *
from rest_framework.permissions import *
from .permission import IsOwner
from rest_framework.response import Response
from .services import ManyModelApiView


class Context(ManyModelApiView):
    queryset_list = [Folder.objects.all(), File.objects.all()]
    serializer_class_list = [FolderSerializer, FileSerializer]
    filter_queryset_list = [
        lambda queryset, pk: queryset.filter(parent=pk),
        lambda queryset, pk: queryset.filter(folder=pk),
    ]

class TestView(generics.ListCreateAPIView):
    """
    Спискок всех подпапок текущей папки.
    list проверяет пренадлежность записи к текущему пользователю.
    """

    permission_classes = [IsAuthenticated, ]
    folder_queryset = Folder.objects.all()
    file_queryset = File.objects.all()

    def is_owner(self):
        if folder := self.queryset.filter(id=self.kwargs['pk']).first():
            if folder.user == self.request.user:
                return True

    def list(self, request, *args, **kwargs):
        if True:
            queryset = self.get_queryset()
            folder_queryset = queryset['folder']
            file_queryset = queryset['file']

            # page = self.paginate_queryset(queryset)
            # if page is not None:
            #     serializer = self.get_serializer(page, many=True)
            #     return self.get_paginated_response(serializer.data)

            folder_serializer = FolderSerializer(folder_queryset, many=True)
            file_serializer = FileSerializer(file_queryset, many=True)

            return Response(folder_serializer.data + file_serializer.data)
        raise Http404

    def get_queryset(self, *args, **kwargs):
        return {
            'folder': self.folder_queryset.filter(parent=self.kwargs['pk']),
            'file': self.file_queryset.filter(folder=self.kwargs['pk']),
        }


class FolderContextView(generics.ListCreateAPIView):
    """
    Спискок всех подпапок текущей папки.
    list проверяет пренадлежность записи к текущему пользователю.
    """

    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

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
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
