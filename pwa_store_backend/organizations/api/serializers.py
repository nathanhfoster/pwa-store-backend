from rest_framework import serializers
from ..models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
