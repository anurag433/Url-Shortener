from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ShortURLSerializer
from .services import create_short_url

class CreateShortURLView(APIView):

    def post(self, request):
        
        serializer = ShortURLSerializer(data = request.data)
        if serializer.is_valid():
            obj = create_short_url(
                serializer.validated_data['original_url']
            )
            return Response({
                "short_code": obj.short_code
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)