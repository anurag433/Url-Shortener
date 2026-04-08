from rest_framework import serializers
from .models import ShortURL

class ShortURLSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShortURL
        fields = ['original_url']

    def validate_original_url(self, value):
        value = value.strip()
        if not value.startswith(('http://', 'https://')):
            value = 'http://' + value
        return value