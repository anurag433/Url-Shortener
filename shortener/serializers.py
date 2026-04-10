from rest_framework import serializers
from .models import ShortURL
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class ShortURLSerializer(serializers.ModelSerializer):
    
    original_url = serializers.CharField()
    class Meta:
        model = ShortURL
        fields = ['original_url']

    def validate_original_url(self, value):
        value = value.strip()

        if not value.startswith(('http://', 'https://')):
            value = 'https://' + value

        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid URL")

        return value