from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from django.db.models import Q

from ..models import Pwa, Tag
from .serializers import TagSerializer, PwaSerializer

class TagViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    lookup_field = "name"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = TagSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class PwaViewSet(viewsets.ModelViewSet):
    serializer_class = PwaSerializer
    queryset = Pwa.objects.all()
    # lookup_field = "name"

    # def get_queryset(self, *args, **kwargs):
    #     return self.queryset.filter(id=self.request.user.id)

    # @action(detail=False, methods=["GET"])
    # def me(self, request):
    #     serializer = PwaSerializer(request.user, context={"request": request})
    #     return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    @action(methods=['GET'], detail=False, url_path='search', url_name='pwa_search')
    def search(self, request, *args, **kwargs):
        key = self.request.GET.get('key', '')
        qs = self.queryset.filter(
          Q(name__contains=key) | Q(description__startswith=key)
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
