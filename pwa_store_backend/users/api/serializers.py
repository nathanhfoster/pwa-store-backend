from rest_framework.serializers import ModelSerializer
from pwa_store_backend.users.models import User, UserSetting
from ..models import FavoritePwa
from pwa_store_backend.pwas.api.serializers import PwaSerializer


class UserSettingSerializer(ModelSerializer):

    class Meta:
        model = UserSetting
        fields = ("id", "mode", )


class FavoritePwaSerializer(ModelSerializer):
    pwa = PwaSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = FavoritePwa
        fields = ('id', 'archived', 'archived_date', 'created_at', 'updated_at', 'pwa',)
        read_only_fields = ('id', 'user', 'pwa', 'created_at', 'updated_at')


class UserSerializer(ModelSerializer):
    setting = UserSettingSerializer(required=False)
    user_favorites = FavoritePwaSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = User
        fields = ("id", "name", "setting", "user_favorites", "username", "password",)
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
        }
