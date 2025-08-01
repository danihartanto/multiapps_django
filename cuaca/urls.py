from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cuaca_index'),
    path('get-child/', views.get_child_wilayah, name='get_child_wilayah'),
    path('get-prakiraan/', views.get_prakiraan, name='get_prakiraan'),
]
