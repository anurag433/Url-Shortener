from rest_framework import serializers
from .models import ShortURL
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class ShortURLSerializer(serializers.ModelSerializer):
    
    original_url = serializers.CharField()
    expiry_date = serializers.DateField(
        required=False,
        allow_null=True
    )
    class Meta:
        model = ShortURL
        fields = [ 'original_url', 'expiry_date']

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

    def validate_expiry_date(self, value):

        if value is None:
            return value
        if value <= timezone.localdate():
            raise serializers.ValidationError(
                "Expiry date must be after creation date"
            )
        return value