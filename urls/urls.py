from django.urls import path
from .views import ShortURLListCreateView, ShortURLDetailView, RedirectView

urlpatterns = [
    path('', ShortURLListCreateView.as_view(), name='shorturl-list-create'),
    path('<int:pk>/', ShortURLDetailView.as_view(), name='shorturl-detail'),
    path('r/<str:short_code>/', RedirectView.as_view(), name='redirect'),
]