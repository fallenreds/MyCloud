from django.urls import path
from .views import *
urlpatterns = [
    path('folder/list/<int:pk>/', FolderContextView.as_view()),
    path('folder/<int:pk>/', FolderUDVIew.as_view()),
    path('test/<int:pk>/', Context.as_view())
]