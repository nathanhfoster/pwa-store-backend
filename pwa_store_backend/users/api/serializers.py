from rest_framework.serializers import ModelSerializer
from pwa_store_backend.users.models import User, UserSetting, FavoritePwa
from pwa_store_backend.pwas.api.serializers import PwaMinimalSerializer


class UserSettingSerializer(ModelSerializer):

    class Meta:
        model = UserSetting
        fields = ("id", "mode", )


class FavoritePwaSerializer(ModelSerializer):
    pwa = PwaMinimalSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = FavoritePwa
        fields = ('id', 'archived', 'archived_date', 'created_at', 'updated_at', 'pwa',)
        read_only_fields = ('id', 'user', 'pwa', 'created_at', 'updated_at')


class UserSerializer(ModelSerializer):
    setting = UserSettingSerializer(required=False)
    user_favorites = FavoritePwaSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = User
        fields = ("id", "name", 'email', "setting", "user_favorites", "username", "password",)
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User()
        user.set_password(validated_data['password'])
        validated_data['password'] = user.password
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
