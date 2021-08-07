from .models import Pwa, Tag
from django.db.models import F
from rest_framework import viewsets, permissions, pagination
from rest_framework.permissions import AllowAny
from .api.serializers import PwaSerializer, TagSerializer


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 500


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

class TagView(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Tag.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (permissions.AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                permissions.IsAuthenticated,)
        return super(PwaView, self).get_permissions()

class PwaView(viewsets.ModelViewSet):
    serializer_class = PwaSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Pwa.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                permissions.IsAuthenticated,)
        return super(PwaView, self).get_permissions()