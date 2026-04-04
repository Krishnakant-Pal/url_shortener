from django.urls import path
from .views import ShortURLListCreateView, ShortURLDetailView

urlpatterns = [
    path('', ShortURLListCreateView.as_view(), name='shorturl-list-create'),
    path('<int:pk>/', ShortURLDetailView.as_view(), name='shorturl-detail'),
]