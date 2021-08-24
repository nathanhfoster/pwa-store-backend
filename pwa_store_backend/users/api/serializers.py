from rest_framework import serializers
from pwa_store_backend.users.models import User, UserSetting


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = ["id", "mode"]

class UserSerializer(serializers.ModelSerializer):
    setting = UserSettingSerializer()
    class Meta:
        model = User
        fields = ("id", "name", "setting")

        # extra_kwargs = {
        #     "url": { "view_name": "api:user-detail" }
        # }