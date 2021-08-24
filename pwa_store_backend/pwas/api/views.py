from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
import requests
import json
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions, pagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models import Pwa, Rating, Tag, PwaAnalytics
from .serializers import PwaSerializer, RatingSerializer, TagSerializer, PwaAnalyticsSerializer


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
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                IsAuthenticated,)
        return super(TagViewSet, self).get_permissions()


class RatingViewSet(viewsets.ModelViewSet):
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


class PwaViewSet(viewsets.ModelViewSet):
    serializer_class = PwaSerializer
    queryset = Pwa.objects.all()
    pagination_class = StandardResultsSetPagination

    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, )
    search_fields = ['name', 'url', 'description', 'tags__name', 'organization__name', 'organization__description',]

    def get_queryset(self):
        if self.request.method == 'GET':
            self.queryset = super().get_queryset().filter(published=True)
        qs = super().get_queryset().select_related('pwa_analytics', 'organization')
        return qs

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (IsAuthenticated,)
        return super(PwaViewSet, self).get_permissions()

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
        data = request.data
        pwa_id = data.get('pwa_id')
        rating = data.get('rating')
        comment = data.get('comment')
        created_by = request.user
        updated_by = created_by
        try: 
            obj = Rating(
              pwa_id=pwa_id,
              rating=rating,
              comment=comment,
              created_by=created_by,
              updated_by=updated_by
            )
            obj.save()
            # update analytics
            analytic = get_object_or_404(PwaAnalytics, pwa_id=pwa_id)
            analytic.rating_count += 1
            analytic.rating_avg = (analytic.rating_avg + obj.rating) / analytic.rating_count
            analytic.save()

            serializer = RatingSerializer(obj, context={'context': request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['patch'], detail=True, url_path="patch-rating")
    def patch_rating(self, request, pk):
        data = request.data
        pwa_id = data.get('pwa_id')
        rating = data.get('rating')
        comment = data.get('comment')
        created_by = request.user
        updated_by = created_by

        try: 
            obj = Rating.objects.get(pk=pk, created_by=created_by)
            past_rating = obj.rating
            obj.updated_by = updated_by
            obj.rating = rating
            obj.comment = comment
            obj.save()
            # update analytics
            analytic = get_object_or_404(PwaAnalytics, pwa_id=pwa_id)
            analytic.rating_avg -= past_rating
            analytic.rating_avg = (analytic.rating_avg + obj.rating) / analytic.rating_count
            analytic.save()

            serializer = RatingSerializer(obj, context={'context': request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)