# sentiment_app/urls.py

from django.urls import path
from .views import analyze_text

urlpatterns = [
    path('', analyze_text, name='analisis_sentimen'),
]
