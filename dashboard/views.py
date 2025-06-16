from django.shortcuts import render, redirect
# from .models import MathGameScore
from mathgame.models import MathGameScore
from hangman_game.models import PlayerScore
from django.contrib.auth.decorators import login_required
from django.db import models

@login_required
def dashboard(request):
    top_scores = MathGameScore.objects.values('user__username').annotate(
        total_score=models.Sum('score')
    ).order_by('-total_score')[:5]
    
    scores = PlayerScore.objects.select_related('user').order_by('-score', 'created_at')[:10]

    #return render(request, 'mathgame/leaderboard.html', {'top_scores': top_scores})
    return render(request, 'dashboard/index.html', {'top_scores': top_scores, 'scores': scores})