from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList
from .serializers import *
from rest_framework.permissions import *


class ManyModelApiView(generics.GenericAPIView):
    """
    Класс для получения кверисетов разных моделей.
    Внимание: порядок кверисетов и сериалайзеров должен совпадать
    """

    queryset_list = []
    serializer_class_list = []
    filter_list = []
    filter_queryset_list = []

    def filter_queryset(self, queryset):
        return [
            filter_func(queryset, self.kwargs["pk"])
            for queryset, filter_func in zip(self.queryset_list, self.filter_queryset_list)
        ]

    def get_lookup_field(self):
        return self.kwargs[self.lookup_field]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return self.filter_queryset(self.queryset_list)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class_list

    def list(self, request, *args, **kwargs):
        queryset_list = self.get_queryset()
        serializer_class_list = self.get_serializer()
        response_data = ReturnList(serializer=serializers.Serializer())
        for queryset, Serializer in zip(queryset_list, serializer_class_list):
            response_data += Serializer(queryset, many=True).data
        return Response(response_data)


class OwnerListCreateApiView(generics.ListCreateAPIView):
    """
    List of all model objects by 'pk'
    It is obligatory to override the get_queryset method.
    For example: self.queryset.filter(parent=self.kwargs['pk'])
    """

    def is_owner(self):
        """
        Checks if the user is the owner.

        Gets the first object of the queryset list and checks if it belongs to a user.
        WARNING: you need to override the get_queryset() method, for example:
            def get_queryset(self, *args, **kwargs):
                return self.queryset.filter(field=self.kwargs['pk'])
        """
        if queryset := self.get_queryset().first():
            if queryset.user == self.request.user:
                return True

    def list(self, request, *args, **kwargs):
        if self.is_owner():
            return super().list(request, *args, **kwargs)
        raise Http404


