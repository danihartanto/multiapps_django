from django.urls import path
from .views import count_characters

urlpatterns = [
    path('', count_characters, name='charcount'),
]
