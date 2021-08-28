from rest_framework import serializers
from pwa_store_backend.users.models import User, UserSetting


class UserSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSetting
        fields = ["id", "mode"]


class UserSerializer(serializers.ModelSerializer):
    setting = UserSettingSerializer(required=False)

    class Meta:
        model = User
        fields = ("id", "name", "setting", "username", "password")
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
        }
