from rest_framework import serializers
from ..models import Pwa, Rating, Tag, PwaAnalytics

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)
        read_only_fields = ('created_at', 'updated_at')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'pwa', 'created_by', 'value')
        read_only_fields = ('id', 'created_at', 'updated_at')

class RatingsField(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('created_by', 'value')
        read_only_fields = ('id', 'pwa','created_at', 'updated_at')

class PwaAnalytics(serializers.ModelSerializer):
    class Meta:
        model = PwaAnalytics
        fields = ('view_count', 'launch_count')

class PwaSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True, required=False)
    ratings = RatingsField(many=True, read_only=True, required=False)
    pwa_analytics = PwaAnalytics(read_only=True)

    class Meta:
        model = Pwa
        fields = ('id', 'name', 'url', 'short_description', 'description',
          'ratings', 'organization', 'pwa_analytics',
                'tags', 'icon_url','updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        