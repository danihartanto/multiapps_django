# secret/urls.py
from django.urls import path
from . import views

# secret/urls.py
urlpatterns = [
    path('', views.create_secret, name='create_secret'),
    path('created/<uuid:secret_id>/', views.secret_created, name='secret_created'),
    path('<uuid:secret_id>/', views.view_secret, name='view_secret'),
    path('expired/', views.expired_view, name='expired_view'),

]

