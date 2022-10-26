from django.urls import path
from .views import *
urlpatterns = [
    path('folder/list/<int:pk>/', FolderListCreateApiView.as_view()),
    path('folder/<int:pk>/', FolderApiView.as_view()),
    path('file/list/<int:pk>/', FolderListCreateApiView.as_view()),
    path('file/<int:pk>/', FolderApiView.as_view()),
    path('file/', FolderNullParentApiView.as_view()),
    path('folder/', FileNullFolderApiView.as_view()),

]