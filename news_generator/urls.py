# news_app/urls.py
from django.urls import path
from .views import news_generator_view, news_list_view, news_detail_view, news_edit_view, news_delete_view

app_name = 'news_app'

urlpatterns = [
    path('', news_generator_view, name='generator'),
    # URL baru untuk halaman daftar berita
    path('list/', news_list_view, name='list'),
    # URL baru untuk halaman detail berita.
    # <int:article_id> menangkap ID artikel sebagai integer dan meneruskannya ke view.
    path('detail/<int:article_id>/', news_detail_view, name='detail'),
    # URL baru untuk mengedit artikel
    path('edit/<int:article_id>/', news_edit_view, name='edit'),
    # URL baru untuk menghapus artikel
    path('delete/<int:article_id>/', news_delete_view, name='delete'),
]