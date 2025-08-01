from django.urls import path
from .views import login_view, register_view  # pastikan ini sesuai views kamu

urlpatterns = [
    path('login/', login_view, name='login'),       # 👈 ini yang penting
    path('register/', register_view, name='register'),
]
