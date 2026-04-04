from rest_framework import serializers
from django.utils import timezone
from .models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    short_code = serializers.CharField(required=False)

    class Meta:
        model = ShortURL
        fields = ('id', 'original_url', 'short_code', 'expires_at', 'click_count', 'created_at')
        read_only_fields = ('id', 'click_count', 'created_at')

    def validate_expires_at(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Expiry date must be in the future.")
        return value