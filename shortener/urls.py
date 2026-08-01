# shortener/urls.py

from django.urls import path
from .views import CreateShortURLView, RedirectView, health

urlpatterns = [
    path("health/", health),
    path('urls/', CreateShortURLView.as_view()),
    path('<str:short_code>/',RedirectView.as_view()),
]