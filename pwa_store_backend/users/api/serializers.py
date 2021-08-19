from rest_framework import serializers
from pwa_store_backend.users.models import User, UserSetting


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = ["mode"]


class UserSerializer(serializers.ModelSerializer):
    setting = UserSettingSerializer()
    class Meta:
        model = User
        fields = ("username", "name", "url", "setting")

        extra_kwargs = {
            "url": { "view_name": "api:user-detail" }
        }