import json
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from rest_framework import status, pagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from ...models import Pwa, Rating, Tag, PwaAnalytics
from ..serializers import PwaSerializer, PwaDetailSerializer, RatingSerializer, TagSerializer, PwaAnalyticsSerializer
from pwa_store_backend.utils.pagination import StandardResultsSetPagination


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                IsAuthenticated,)
        return super(TagViewSet, self).get_permissions()


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                IsAuthenticated,)
        return super(RatingViewSet, self).get_permissions()

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = TagSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class PwaViewSet(ModelViewSet):
    serializer_class = PwaSerializer
    queryset = Pwa.objects.all()
    pagination_class = StandardResultsSetPagination
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, )
    search_fields = ['name', 'url', 'description', 'tags__name', 'organization__name', 'organization__description', ]

    def get_queryset(self):
        if self.request.parser_context['kwargs'].get('slug', None):
            qs = super().get_queryset().select_related('pwa_analytics', 'organization')
        else:
            qs = super().get_queryset().filter(published=True).select_related('pwa_analytics', 'organization')
        return qs

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super(PwaViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        self.serializer_class = PwaDetailSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = PwaDetailSerializer
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PwaDetailSerializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(methods=['patch'], detail=False, url_path="analytics-counter", permission_classes=[AllowAny, ])
    def increase_counts(self, request):
        data = json.loads(request.body)
        try:
            analytics_obj = PwaAnalytics.objects.get(pwa__slug=data.get('slug'))
            if data.get('incr_view', False):
                analytics_obj.view_count += 1
            elif data.get('incr_launch', False):
                analytics_obj.launch_count += 1
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            analytics_obj.save()
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        qs = self.get_queryset()
        serializer = PwaSerializer(qs.get(slug=data.get('slug')), context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
