"""
from .serializers import *
from rest_framework import generics, mixins
from rest_framework.permissions import *
"""

from rest_framework.views import APIView
from rest_framework import status
from .permission import IsOwner
from .services import *


"""----------------------------------FOLDER-VIEW----------------------------------"""


class FolderApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class FolderNullParentApiView(OwnerListCreateApiView):
    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(parent=None)


class FolderListCreateApiView(OwnerListCreateApiView):
    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(parent=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(parent=Folder.objects.get(id=self.kwargs['pk']))


"""----------------------------------File-VIEW-------------------------------------"""


class FileNullFolderApiView(OwnerListCreateApiView):
    permission_classes = [IsAuthenticated, ]
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(folder=None)


class FileListCreateApiView(OwnerListCreateApiView):
    permission_classes = [IsAuthenticated, ]
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(folder=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(folder=Folder.objects.get(id=self.kwargs['pk']))


class FileApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = File.objects.all()
    serializer_class = FileSerializer


"""----------------------------------USER-VIEW----------------------------------"""


class UserApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = get_user_model().objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.get(user=self.request.user)


class CurrentUserApiView(generics.RetrieveAPIView):
    User = get_user_model()
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])




class Test(OwnerListCreateApiView):
    permission_classes = [IsAuthenticated, ]
    queryset = File.objects.all()
    serializer_class = FileSerializer
    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(folder=self.kwargs['pk'])

    def get_files(self):
        return (file for file in self.request.FILES.values())

    def get_file_name(self):
        return self.request.FILES['name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs['data'], many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def post(self, request, *args, **kwargs):
        files = self.get_files()
        data = []
        for file in files:
            data.append({
                'label': file.name,
                'filesize': file.size
            })
        kwargs['data'] = data
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        folder = Folder.objects.get(id=self.kwargs['pk'])

        serializer.save(folder=folder)




