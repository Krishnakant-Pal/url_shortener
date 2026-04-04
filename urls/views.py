import string
import random
from rest_framework import generics, permissions
from .models import ShortURL
from .serializers import ShortURLSerializer


def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))


class ShortURLListCreateView(generics.ListCreateAPIView):
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.IsAuthenticated]

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