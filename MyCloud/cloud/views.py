from .serializers import *
from rest_framework.permissions import *
from .permission import IsOwner
from .services import CRUDApiView, OwnerListApiView


class FolderListApiView(OwnerListApiView):

    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(parent=self.kwargs['pk'])


class FolderApiView(CRUDApiView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class FileListApiView(OwnerListApiView):
    permission_classes = [IsAuthenticated, ]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class FileApiView(CRUDApiView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
