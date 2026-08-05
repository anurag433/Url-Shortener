from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.http import Http404
from .models import ShortURL
from .serializers import ShortURLSerializer
from .services import create_short_url, generate_qr
from core.cache import get_from_cache, set_to_cache, delete_from_cache
from django.http import JsonResponse
from django.utils import timezone
from .storage import delete_file

class CreateShortURLView(APIView):

    def post(self, request):
        
        serializer = ShortURLSerializer(data = request.data)
        if serializer.is_valid():
            obj = create_short_url(
                serializer.validated_data['original_url'],
                serializer.validated_data.get("expiry_date")
            )

            short_url = request.build_absolute_uri(f"/{obj.short_code}")
            generate_qr(obj, short_url)
            return Response({
                "short_url": short_url,
                "clicks": obj.clicks,
                "created_at": obj.created_at,
                "expiry_date": obj.expiry_date,
                "qr_code": obj.qr_code_url
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

class URLAnalyticsView(APIView):

    def post(self, request):
        try:
            url = request.data.get("url", "").strip()
            if not url:
                return Response(
                    {
                        "message": "Please enter a Short URL or Short Code."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if url.startswith(("http://", "https://")):
                short_code = url.rstrip("/").split("/")[-1]
            else:
                short_code = url

            obj = ShortURL.objects.get(short_code=short_code)
            if obj.expiry_date:
                if timezone.localdate() > obj.expiry_date:
                    link_status = "Expired"
                else:
                    link_status = "Active"
            else:
                link_status = "Never Expires"
            return Response(
                {
                    
                    "original_url": obj.original_url,
                    "short_url": request.build_absolute_uri(f"/{obj.short_code}"),
                    "short_code": obj.short_code,
                    "created_at": obj.created_at.strftime("%d %b %Y"),
                    "expiry_date": (
                        obj.expiry_date.strftime("%d %b %Y")
                        if obj.expiry_date else "Never"
                    ),
                    "clicks": obj.clicks,
                    "status": link_status,
                    "qr_code": obj.qr_code_url
                    
                },
                status=status.HTTP_200_OK
            )
        except ShortURL.DoesNotExist:
            return Response(
                {
                    "message": "Short URL not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteShortURLView(APIView):
    def delete(self, request, short_code):
        try:

            obj = ShortURL.objects.get(short_code=short_code)
            delete_file(f"{obj.short_code}.png")
            delete_from_cache(short_code)
            obj.delete()
            return Response(
                {
                    "message": "Short URL deleted successfully."
                },
                status=status.HTTP_200_OK
            )
        except ShortURL.DoesNotExist:
            return Response(
                {
                    "message": "Short URL not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )