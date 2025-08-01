from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PlayerScore
import random

# Daftar kata (bisa diimprove nanti)
WORDS = ['python', 'django', 'frontend', 'framework', 'backend', 'function', 'variable']

def init_game(session):
    word = random.choice(WORDS)
    session['word'] = word
    # Otomatis tambahkan huruf pertama & terakhir
    guesses = list(set([word[0], word[-1]]))
    session['guesses'] = guesses
    session['tries_left'] = 6
    session['score_saved'] = False

@login_required
def hangman_game(request):
    if 'word' not in request.session:
        init_game(request.session)

    word = request.session['word']
    guesses = request.session.get('guesses', [])
    tries_left = request.session.get('tries_left', 6)

    # displayed = ' '.join([c if c in guesses else '_' for c in word])
    displayed = ' '.join([
        c if (i == 0 or i == len(word)-1 or c in guesses) else '_'
        for i, c in enumerate(word)
    ])
    is_won = all(c in guesses for c in word)
    is_lost = tries_left <= 0

    # Simpan skor ke DB jika menang dan belum disimpan
    if is_won and not request.session.get('score_saved', False):
        PlayerScore.objects.create(
            user=request.user,
            score=tries_left
        )
        request.session['score_saved'] = True

    # context = {
    #     'displayed': displayed,
    #     'tries_left': tries_left,
    #     'guesses': guesses,
    #     'is_won': is_won,
    #     'is_lost': is_lost,
    #     'word': word if is_won or is_lost else None,
    # }
    context = {
        'word': request.session.get('word', ''),
        'guesses': request.session.get('guesses', []),
        'tries_left': request.session.get('tries_left', 6),
        'is_won': is_won,
        'is_lost': is_lost,
    }
    return render(request, 'hangman_game/index.html', context)

@login_required
def guess_letter(request):
    if request.method == 'POST':
        letter = request.POST.get('letter', '').lower()
        if letter and letter.isalpha() and len(letter) == 1:
            guesses = request.session.get('guesses', [])
            if letter not in guesses:
                guesses.append(letter)
                request.session['guesses'] = guesses
                if letter not in request.session['word']:
                    request.session['tries_left'] -= 1
    return redirect('hangman')

@login_required
def leaderboard(request):
    scores = PlayerScore.objects.select_related('user').order_by('-score', 'created_at')[:10]
    return render(request, 'hangman_game/leaderboard.html', {'scores': scores})

@login_required
def restart_game(request):
    init_game(request.session)
    return redirect('hangman')