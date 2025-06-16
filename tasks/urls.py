from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='tasks'),
    path('add/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
]
