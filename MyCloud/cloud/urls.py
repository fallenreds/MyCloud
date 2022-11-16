from django.urls import path
from .views import *
urlpatterns = [
    path('folder/list/<int:pk>/', FolderListCreateApiView.as_view()),
    path('folder/<int:pk>/', FolderApiView.as_view()),
    path('folder/', FileNullFolderApiView.as_view()),

    path('file/list/<int:pk>/', FileListCreateApiView.as_view()),
    path('file/<int:pk>/', FileApiView.as_view()),
    path('file/', FileNullFolderApiView.as_view()),

    path('test/<int:pk>/', Test.as_view())

]