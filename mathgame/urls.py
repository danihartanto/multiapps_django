from django.urls import path
from . import views

urlpatterns = [
    path('', views.math_game, name='mathgame'),
    path('reset/', views.reset_game, name='resetgame'),
    path('history/', views.score_history, name='mathgame_history'),
    path('leaderboard/', views.leaderboard, name='math_leaderboard'),

]
