from rest_framework.serializers import ModelSerializer, JSONField, Field
from pwa_store_backend.users.models import User
from rest_framework import serializers
from ..models import Pwa, Rating, Tag, PwaScreenshot, PwaAnalytics
from pwa_store_backend.users.models import User
from ...organizations.models import Organization
import json


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)
        read_only_fields = ('created_at', 'updated_at')


class RatingUserField(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name",)


class RatingSerializer(ModelSerializer):
    created_by = RatingUserField()

    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    # def __init__(self, *args, **kwargs):
    #     super(RatingSerializer, self).__init__(*args, **kwargs)
    #     if kwargs.get('context', None) and kwargs.get('context').get('request').method == 'GET':
    #         self.fields['created_by'] = RatingUserField()


class PwaScreenshot(ModelSerializer):
    class Meta:
        model = PwaScreenshot
        fields = ('image_url', 'caption', )


class PwaAnalyticsSerializer(ModelSerializer):
    class Meta:
        model = PwaAnalytics
        fields = ('view_count', 'launch_count', 'rating_avg', 'rating_count', )


class PwaOrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'description')
        read_only_fields = ('id', 'created_at', 'updated_at')


class PwaMinimalSerializer(ModelSerializer):

    class Meta:
        model = Pwa
        fields = ('id', 'slug', 'name', 'url', 'image_url',)
        read_only_fields = ('id', 'created_at', 'updated_at', 'tags')


class PwaSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True, required=False)
    ratings = RatingSerializer(many=True, read_only=True, required=False)
    pwa_analytics = PwaAnalyticsSerializer(read_only=True)
    pwa_screenshots = PwaScreenshot(many=True, read_only=True)
    organization = PwaOrganizationSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = Pwa
        fields = ('id', 'slug', 'published', 'name', 'url', 'description',
                  'ratings', 'organization', 'manifest_url', 'pwa_analytics', 'pwa_screenshots',
                  'tags', 'image_url', 'updated_at',)
        lookup_field = 'slug'
        read_only_fields = ('id', 'created_at', 'updated_at')

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

    class Meta(PwaSerializer.Meta):
        fields = PwaSerializer.Meta.fields + ('created_by', 'updated_by', 'manifest_json',)
