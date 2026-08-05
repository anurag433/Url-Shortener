# shortener/urls.py

from django.urls import path
from .views import CreateShortURLView, RedirectView,URLAnalyticsView,DeleteShortURLView,health 

urlpatterns = [
    path("health/", health),
    path('urls/', CreateShortURLView.as_view()),
    path("analytics/", URLAnalyticsView.as_view()),
    path("analytics/<str:short_code>", DeleteShortURLView.as_view()),
    path('<str:short_code>/',RedirectView.as_view()),
]