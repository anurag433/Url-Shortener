from rest_framework import serializers
from .models import ShortURL
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class ShortURLSerializer(serializers.ModelSerializer):
    
    original_url = serializers.CharField()
    custom_url = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank =True
    )
    expiry_date = serializers.DateField(
        required=False,
        allow_null=True
    )
    class Meta:
        model = ShortURL
        fields = [ 'original_url', 'expiry_date', 'custom_url']

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

    def validate_custom_url(self, value):
        if not value:
            return None

        value = value.strip() 
        if len(value) < 4 or len(value) > 20:
            raise serializers.ValidationError(
                "Custom url must be between 4 and 20 character"
            )

        import re
        if not re.match(r"^[A-Za-z0-9_-]+$", value):
            raise serializers.ValidationError(
                "Custom url can contain only letters, numbers, '-' and '_'."
            )

        if ShortURL.objects.filter(short_code=value).exists():
            raise serializers.ValidationError(
                "This custom url is already taken"
            )

        return value 
class URLAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = [
            "original_url",
            "short_code",
            "created_at",
            "expiry_date",
            "clicks",
            "qr_code_url",
        ]