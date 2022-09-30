from django.urls import path
from .views import *
urlpatterns = [
    path('folder/list/<int:pk>/', FolderContextView.as_view()),

    path('folder/', MainFolderView.as_view()),
    path('folder/create/', FolderListCreateView.as_view()),
]