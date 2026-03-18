# shortener/urls.py

from django.urls import path
from .views import CreateShortURLView, RedirectView

urlpatterns = [
    path('shorten/', CreateShortURLView.as_view()),
    path('<str:short_code>/',RedirectView.as_view()),
]