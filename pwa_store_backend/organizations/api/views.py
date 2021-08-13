from ..models import Organization
from django.db.models import F
from rest_framework import viewsets, permissions, pagination
from rest_framework.permissions import AllowAny
from .serializers import OrganizationSerializer

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 500


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Organization.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                permissions.IsAuthenticated,)
        return super(OrganizationViewSet, self).get_permissions()