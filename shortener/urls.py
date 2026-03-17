# shortener/urls.py

from django.urls import path
from .views import CreateShortURLView

urlpatterns = [
    path('shorten/', CreateShortURLView.as_view()),
]