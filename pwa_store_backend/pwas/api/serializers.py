from rest_framework import serializers, validators
from pwa_store_backend.users.models import User
from ..models import Pwa, Rating, Tag, PwaScreenshot, PwaAnalytics
from ...organizations.models import Organization
from pwa_store_backend.utils.validators import HasValidJson
import json

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)
        read_only_fields = ('created_at', 'updated_at')

class RatingUserField(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name",)

class RatingSerializer(serializers.ModelSerializer):
    created_by = RatingUserField()
    class Meta:
        model = Rating
        fields = ('id', 'created_by', 'rating', 'comment', 'updated_at',)
        read_only_fields = ('id', 'pwa', 'created_at', 'updated_at')


class PwaScreenshot(serializers.ModelSerializer):
    class Meta:
        model = PwaScreenshot
        fields = ('image_url', 'caption', )


class PwaAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PwaAnalytics
        fields = ('view_count', 'launch_count', 'rating_avg', 'rating_count', )

class PwaOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'description')
        read_only_fields = ('id', 'created_at', 'updated_at')


class PwaSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True, required=False)
    ratings = RatingSerializer(many=True, read_only=True, required=False)
    pwa_analytics = PwaAnalyticsSerializer(read_only=True)
    pwa_screenshots = PwaScreenshot(many=True, read_only=True)
    organization = PwaOrganizationSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = Pwa
        fields = ('id', 'published', 'name', 'url', 'description',
                  'ratings', 'organization', 'manifest_url', 'pwa_analytics', 'pwa_screenshots',
                  'tags', 'image_url', 'updated_at', "manifest_json")
        read_only_fields = ('id', 'created_at', 'updated_at')
        # TODO

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)
        tags = self.context['request'].data.get('tags', None)
        if tags:
            obj.tags.set(list(Tag.objects.filter(name__in=tags)))
            obj.save()
        return obj

    def create(self, validated_data):
        obj = super().create(validated_data)
        tags = self.context['request'].data.get('tags', None)
        if tags:
            obj.tags.set(list(Tag.objects.filter(name__in=tags)))
            obj.save()
        return obj

class PwaDetailSerializer(PwaSerializer):
    manifest_json = serializers.JSONField(required=False, allow_null=True)

    def to_representation(self, instance):
        ret = super(PwaDetailSerializer, self).to_representation(instance)
        ret['manifest_json'] = json.loads(ret['manifest_json'])
        return ret


    class Meta(PwaSerializer.Meta):
        fields = PwaSerializer.Meta.fields + ('manifest_json',)