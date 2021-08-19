from django.contrib.auth import get_user_model
from rest_framework import serializers
from pwa_store_backend.users.models import User, UserSetting

# User = get_user_model()

class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = ["mode"]


class UserSerializer(serializers.ModelSerializer):
    settings = UserSettingSerializer()
    class Meta:
        model = User
        fields = ("username", "name", "url", "settings")

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": ("id", "username")}
        }