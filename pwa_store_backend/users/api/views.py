from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import update_last_login
from rest_framework import generics
from pwa_store_backend.users.models import UserSetting, User, FavoritePwa
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserSettingSerializer, FavoritePwaSerializer, FavoritePwaSerializer
from pwa_store_backend.pwas.models import Pwa
from pwa_store_backend.pwas.api.serializers import PwaSerializer


def get_user_response(token, user):
    update_last_login(None, user)
    user_setting = UserSettingSerializer(user.setting).data
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


class RegisterViewSet(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response(get_user_response(token, user))


class LoginViewSet(ObtainAuthToken):
    permission_classses = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = get_object_or_404(Token, user=user)
        return Response(get_user_response(token, user))


class UpdateSettingsViewSet(generics.UpdateAPIView):
    queryset = UserSetting.objects.all()
    serializer_class = UserSettingSerializer


class FavoritePwaViewSet(ModelViewSet):
    serializer_class = FavoritePwaSerializer
    queryset = FavoritePwa.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == 'PATCH':
            self.permission_classes = (
                IsAuthenticated,)
        return super(FavoritePwaViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            pwa = get_object_or_404(Pwa, slug=data.get('pwa_slug'))
            fav = FavoritePwa(
              pwa=pwa,
              user=request.user
            )
            fav.save()
            serializer = self.get_serializer(fav)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
