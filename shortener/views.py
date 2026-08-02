from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.http import Http404
from .models import ShortURL
from .serializers import ShortURLSerializer
from .services import create_short_url
from core.cache import get_from_cache, set_to_cache
from django.http import JsonResponse
from django.utils import timezone


class CreateShortURLView(APIView):

    def post(self, request):
        
        serializer = ShortURLSerializer(data = request.data)
        if serializer.is_valid():
            obj = create_short_url(
                serializer.validated_data['original_url'],
                serializer.validated_data.get("expiry_date")
            )

            short_url = request.build_absolute_uri(f"/{obj.short_code}")
            return Response({
                "short_url": short_url,
                "clicks": obj.clicks,
                "created_at": obj.created_at,
                "expiry_date": obj.expiry_date,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RedirectView(APIView):
    def get(self, request, short_code):
        try:
            obj = ShortURL.objects.get(short_code=short_code)
            if obj.expiry_date and timezone.localdate() > obj.expiry_date:
                return Response(
                    {"error": "This link has expired."},
                    status=410
                )

            obj.clicks += 1
            obj.save(update_fields=["clicks"])

            original_url = get_from_cache(short_code)

            if original_url is None:
                original_url = obj.original_url
                set_to_cache(short_code, original_url)

            return redirect(original_url)

        except ShortURL.DoesNotExist:
            raise Http404("URL not found")

def health(request):
    return JsonResponse({"status": "ok"})