from ..models import Pwa, Rating, Tag
from django.db.models import F
from rest_framework import viewsets, permissions, pagination
from rest_framework.permissions import AllowAny
from .serializers import PwaSerializer, RatingSerializer, TagSerializer
from rest_framework.filters import SearchFilter


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 500


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (permissions.AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                permissions.IsAuthenticated,)
        return super(TagViewSet, self).get_permissions()

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (permissions.AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                permissions.IsAuthenticated,)
        return super(RatingViewSet, self).get_permissions()

class PwaViewSet(viewsets.ModelViewSet):
    serializer_class = PwaSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Pwa.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (SearchFilter, )
    search_fields = ['name', 'description', 'tags__name']

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                permissions.IsAuthenticated,)
        return super(PwaViewSet, self).get_permissions()