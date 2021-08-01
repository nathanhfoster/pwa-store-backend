from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import F
from .models import User
from rest_framework import viewsets
from .serializers import UserSerializer, Serializer, AdminSerializer
from user.permissions import IsAuthorOrSuperUser, IsStaffOrTargetUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.utils.timezone import now


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, )
    search_fields = ('email', 'id', 'username', 'first_name', 'last_name', )

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                IsAuthenticated, IsAuthorOrSuperUser,)
        return super(UserView, self).get_permissions()

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def refresh(self, request, pk):
        qs = User.objects.get(pk=pk)

        if request.user and request.user.is_authenticated:
            user = request.user
            user.last_login = now()
            user.save(update_fields=['last_login'])

        return Response(Serializer(qs).data)

    @action(methods=['get'], detail=False, permission_classes=[permission_classes])
    def all(self, request):
        qs = User.objects.all()
        serializer = AdminSerializer(qs, many=True)
        return Response(serializer.data)