from rest_framework import serializers
from ..models import Pwa, Rating, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', 'created_at', 'updated_at')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'pwa_id', 'owner', 'value')
        read_only_fields = ('id', 'created_at', 'updated_at')

class RatingsField(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('owner', 'value')
        read_only_fields = ('id', 'pwa_id','created_at', 'updated_at')

class PwaSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True, required=False)
    ratings = RatingsField(many=True, read_only=True, required=False)
    
    class Meta:
        model = Pwa
        fields = ('id', 'name', 'url', 'short_description', 'description',
                'views', 'launches', 'ratings', 'organization',
                'tags', 'icon_url','updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        