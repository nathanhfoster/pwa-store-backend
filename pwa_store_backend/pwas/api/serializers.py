from rest_framework import serializers
from models import Pwa, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('id', 'date_created', 'last_modified')

class PwaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pwa
        fields = '__all__'
        read_only_fields = ('id', 'date_created', 'last_modified')
        