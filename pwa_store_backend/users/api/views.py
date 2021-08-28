from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import update_last_login
from rest_framework import generics
from pwa_store_backend.users.models import UserSetting
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserSettingSerializer
from pwa_store_backend.pwas.models import Pwa
from pwa_store_backend.pwas.api.serializers import PwaSerializer

User = get_user_model()


def get_user_response(token, user, user_setting):
    return {
        'token': token.key,
        'id': user.pk,
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'setting': user_setting,
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'last_login': user.last_login,
        'date_joined': user.date_joined,
    }


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def pwas(self, request, pk):
        queryset = Pwa.objects.all().filter(created_by=pk)
        serializer = PwaSerializer(queryset, many=True)

        return Response(serializer.data)


class RegisterView(ObtainAuthToken):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        update_last_login(None, user)
        token, created = Token.objects.get_or_create(user=user)
        setting_serializer = UserSettingSerializer(user.setting)
        return Response(get_user_response(token, user, setting_serializer.data))


class LoginView(ObtainAuthToken):
    permission_classses = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        update_last_login(None, user)
        token = get_object_or_404(Token, user=user)
        setting_serializer = UserSettingSerializer(user.setting)
        return Response(get_user_response(token, user, setting_serializer.data))


class UpdateSettingsView(generics.UpdateAPIView):
    queryset = UserSetting.objects.all()
    serializer_class = UserSettingSerializer
