"""
from .serializers import *
from rest_framework import generics, mixins
from rest_framework.permissions import *
"""
from .permission import IsOwner
from .services import *


class UserApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = get_user_model().objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.get(user=self.request.user)


class FolderNullParentApiView(OwnerListCreateApiView):
    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(parent=None)


class FileNullFolderApiView(OwnerListCreateApiView):
    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(folder=None)


class FolderListCreateApiView(OwnerListCreateApiView):
    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(parent=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(parent=self.kwargs['pk'])


class FileListCreateApiView(OwnerListCreateApiView):
    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(folder=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(folder=self.kwargs['pk'])


class FolderApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class FileApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class CurrentUserApiView(generics.RetrieveAPIView):
    User = get_user_model()
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):

        return self.queryset.filter(id=self.kwargs['pk'])
#TODO сделать сегодня авторизацию, заробратся с моделю юзера