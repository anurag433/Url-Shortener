from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.http import Http404
from .models import ShortURL
from .serializers import ShortURLSerializer
from .services import create_short_url
from core.cache import get_from_cache, set_to_cache

class CreateShortURLView(APIView):

    def post(self, request):
        
        serializer = ShortURLSerializer(data = request.data)
        if serializer.is_valid():
            obj = create_short_url(
                serializer.validated_data['original_url']
            )

            short_url = request.build_absolute_uri(f"/{obj.short_code}")
            return Response({
                "short_url": short_url
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    
class RedirectView(APIView):
    def get(self, request,short_code):
        original_url = get_from_cache(short_code)
        if original_url:
            return redirect(original_url)
        
        try:
            obj = ShortURL.objects.get(short_code=short_code)
            set_to_cache(short_code, obj.original_url)
            obj.clicks +=1 
            obj.save()

            return redirect(obj.original_url)


        except ShortURL.DoesNotExist:
            raise Http404("Url not found !")
