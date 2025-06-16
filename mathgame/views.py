# Create your views here.
import random
from django.shortcuts import render, redirect
from .models import MathGameScore
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.db import models

def make_math_question(request):
    score = request.session.get('score', 0)

    # Tentukan level berdasarkan score
    if score < 20:
        level = 'easy'
        min_val, max_val = 1, 9  # 1 digit
    elif score <= 50:
        level = 'medium'
        min_val, max_val = 10, 99  # 2 digit
    else:
        level = 'hard'
        min_val, max_val = 100, 999  # 3 digit

    operations = ['+', '-', '*', '/']
    op = random.choice(operations)
    num1 = random.randint(min_val, max_val)
    num2 = random.randint(min_val, max_val)

    if op == '/':
        num1 = num1 * num2
        answer = num1 / num2
    else:
        answer = eval(f"{num1} {op} {num2}")

    request.session['level'] = level

    return f"{num1} {op} {num2}", round(answer, 2)


# @login_required
# def math_game(request):
#     if 'score' not in request.session:
#         request.session['score'] = 0
#         request.session['total'] = 0
#         request.session['game_over'] = False  # initialize game_over

#     message = ''
#     game_over = request.session.get('game_over', False)

#     if request.method == 'POST' and not game_over:
#         user_answer = request.POST.get('answer')
#         correct_answer = float(request.session.get('answer', 0))
#         try:
#             if abs(float(user_answer) - correct_answer) < 0.01:
#                 request.session['score'] += 1
#                 message = '✅ Correct!'
#             else:
#                 message = f"❌ Wrong! The correct answer was {correct_answer}. Game over!"
                
#                 # Simpan skor ke database saat jawaban salah
#                 MathGameScore.objects.create(
#                     user=request.user,
#                     score=request.session.get('score', 0),
#                     total_questions=request.session.get('total', 0) + 1  # +1 karena ini jawaban terakhir
#                 )
                
#                 request.session['game_over'] = True
#         except:
#             message = "⚠️ Invalid input."

#         request.session['total'] += 1

#     if not request.session.get('game_over', False):
#         question, answer = make_math_question()
#         request.session['answer'] = answer
#     else:
#         question = None

#     context = {
#         'question': question,
#         'score': request.session.get('score', 0),
#         'total': request.session.get('total', 0),
#         'message': message,
#         'game_over': request.session.get('game_over', False),
#     }
#     return render(request, 'mathgame/index.html', context)
@login_required
def math_game(request):
    if 'score' not in request.session:
        request.session['score'] = 0
        request.session['total'] = 0
        request.session['game_over'] = False

    score = request.session['score']
    total = request.session['total']
    game_over = request.session.get('game_over', False)
    message = ''

    if request.method == 'POST' and not game_over:
        user_answer = request.POST.get('answer')
        correct_answer = float(request.session.get('answer', 0))
        try:
            if abs(float(user_answer) - correct_answer) < 0.01:
                request.session['score'] += 1
                message = '✅ Correct!'
            else:
                message = f"❌ Wrong! The correct answer was {correct_answer}"
                request.session['game_over'] = True
                


                # Simpan skor saat game over
                MathGameScore.objects.create(
                    user=request.user,
                    score=score,
                    total_questions=request.session.get('total', 0) + 1,  # +1 karena ini jawaban terakhir
                    level = request.session.get('level', 0) 
                )

        except ValueError:
            message = "⚠️ Invalid input."

        request.session['total'] += 1

    # Ambil pertanyaan baru hanya jika game belum berakhir
    if not request.session.get('game_over', False):
        question, answer = make_math_question(request)
        request.session['answer'] = answer
    else:
        question = None

    last = MathGameScore.objects.filter(user=request.user).order_by('-created_at').first()

    context = {
        'question': question,
        'message': message,
        'game_over': request.session.get('game_over', False),
        'last_score': last.score if last else None,
        'last_total': last.total_questions if last else None,
        'level': request.session.get('level', 'easy'),
        'score': request.session.get('score', 0),
        'total': request.session.get('total', 0),
        'message': message,
    }
    return render(request, 'mathgame/index.html', context)

@login_required
def reset_game(request):
    
    # score = request.session.get('score', 0)
    # total = request.session.get('total', 0)

    # if total > 0:
    #     MathGameScore.objects.create(
    #         user=request.user,
    #         score=score,
    #         total_questions=total
    #     )

        # Simpan skor terakhir ke session
        # request.session['last_score'] = score
        # request.session['last_total'] = total

    # Hapus data skor aktif, bukan semua session
    request.session.pop('score', None)
    request.session.pop('total', None)
    request.session.pop('answer', None)

    return redirect('mathgame')



@login_required
def score_history(request):
    scores = MathGameScore.objects.filter(user=request.user).order_by('-created_at')

    # Filter
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    min_percent = request.GET.get('min_percent')

    if start_date:
        scores = scores.filter(created_at__date__gte=parse_date(start_date))
    if end_date:
        scores = scores.filter(created_at__date__lte=parse_date(end_date))
    if min_percent:
        try:
            min_percent = float(min_percent)
            scores = [s for s in scores if (s.score / s.total_questions * 100 if s.total_questions else 0) >= min_percent]
        except:
            pass

    for s in scores:
        s.percentage = round((s.score / s.total_questions) * 100, 2) if s.total_questions else 0

    context = {
        'scores': scores,
        'filters': {
            'start_date': start_date or '',
            'end_date': end_date or '',
            'min_percent': min_percent or ''
        }
    }
    return render(request, 'mathgame/history.html', context)

def leaderboard(request):
    top_scores = MathGameScore.objects.values('user__username').annotate(
        total_score=models.Sum('score')
    ).order_by('-total_score')[:5]

    return render(request, 'mathgame/leaderboard.html', {'top_scores': top_scores})
# @login_required
# def leaderboard(request):
#     top_scores = (
#         MathGameScore.objects.values('user__username')
#         .annotate(max_score=max('score'))
#         .order_by('-max_score')[:10]
#     )
#     print(top_scores)
#     return render(request, 'mathgame/leaderboard.html', {'top_scores': top_scores})