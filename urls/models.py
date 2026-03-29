
from django.db import models
from django.contrib.auth.models import User
import string
import random


def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))


class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='short_urls')
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=50, unique=True, default=generate_short_code)
    custom_code = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.short_code} → {self.original_url}"
