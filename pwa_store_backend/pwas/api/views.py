from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Pwa, Rating, Tag, PwaAnalytics
from rest_framework import viewsets, status, permissions, pagination
from .serializers import PwaSerializer, RatingSerializer, TagSerializer, PwaAnalyticsSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
import requests
import json

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

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = TagSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class PwaViewSet(viewsets.ModelViewSet):
    serializer_class = PwaSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Pwa.objects.filter(published=True)

    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (SearchFilter, )
    search_fields = ['name', 'url', 'short_description', 'description', 'tags__name', 'organization__name', 'organization__description',]

    def get_queryset(self):
        qs = super().get_queryset().select_related('pwa_analytics', 'organization')
        return qs

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (AllowAny,)
            # self.permission_classes = (
            #     permissions.IsAuthenticated,)
        return super(PwaViewSet, self).get_permissions()

    @action(methods=['get'], detail=False, url_path="get-manifest", url_name="get_manifest")
    def get_manifest(self, request):
        try:
            url = request.query_params.get('url')
            r = requests.get(f"{url}/manifest.json")
            return Response(r.json(), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid URL"}, status=status.HTTP_406_NOT_ACCEPTABLE)



    @action(methods=['patch'], detail=False, url_path="analytics-counter")
    def increase_counts(self, request):
        data = json.loads(request.body)
        try:
            analytics_obj = PwaAnalytics.objects.get(pwa__id=data.get('pwa_id'))
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
        serializer = PwaSerializer(qs.get(id=data.get('pwa_id')), context={ 'request': request })
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=['post'], detail=False, url_path="post-rating")
    def post_rating(self, request):
        try: 
            data = request.data
            obj = Rating(
              pwa_id=data.get('pwa_id'),
              rating=data.get('rating'),
              comment=data.get('comment'),
              created_by=request.user,
            )
            obj.save()
            serializer = RatingSerializer(obj, context={'context': request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)