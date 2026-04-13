import string
import random
from rest_framework import generics, permissions, status
from .models import ShortURL
from .serializers import ShortURLSerializer,URLAnalyticsSerializer
from django.utils import timezone
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import track_click
from django.db.models import Sum
from rest_framework.throttling import UserRateThrottle

class CreateURLThrottle(UserRateThrottle):
    # Stricter limit specifically for creating short URLs
    scope = 'create_url'

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))


class ShortURLListCreateView(generics.ListCreateAPIView):
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [CreateURLThrottle] 

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        short_code = serializer.validated_data.get('short_code')
        custom = False 

        if short_code:
            custom = True
        else:
            while True:
                short_code = generate_short_code()
                if not ShortURL.objects.filter(short_code=short_code).exists():
                    break
        serializer.save(user=self.request.user, short_code=short_code,custom_code=custom)


class ShortURLDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)


class RedirectView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, short_code):
        cache_key = f"url_{short_code}"
        original_url = cache.get(cache_key)

        if not original_url:
          
            try:
                url_obj = ShortURL.objects.get(short_code=short_code)
            except ShortURL.DoesNotExist:
                return Response({'error': 'URL not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Check if link has expired
            if url_obj.expires_at and url_obj.expires_at < timezone.now():
                return Response({'error': 'This link has expired.'}, status=status.HTTP_404_NOT_FOUND)

            original_url = url_obj.original_url

            # Store in Redis for 1 hour 
            cache.set(cache_key, original_url, timeout=3600)
            
          
        # track click in background
        track_click.delay(short_code)

        return Response({'url': original_url}, status=status.HTTP_200_OK)

class URLAnalyticsView(generics.RetrieveAPIView):
    # Returns stats for a single short URL by short_code
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = URLAnalyticsSerializer

    def get_object(self):
        return generics.get_object_or_404(
            ShortURL,
            short_code=self.kwargs['short_code'],
            user=self.request.user  
        )


class SummaryView(APIView):
    # Returns total URLs and total clicks for the logged in user
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = ShortURL.objects.filter(user=request.user)
        total_urls = qs.count()
        total_clicks = qs.aggregate(total=Sum('click_count'))['total'] or 0

        return Response({
            'total_urls': total_urls,
            'total_clicks': total_clicks,
        })