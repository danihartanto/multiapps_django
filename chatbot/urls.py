from django.urls import path
from .views import chat_view, chat_page

urlpatterns = [
    path('chat/', chat_view, name='chat'),
    path('chatbot/', chat_page, name='chat_ui'),

]
