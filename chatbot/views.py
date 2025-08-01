from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

# Aturan tanya-jawab
from .models import ChatRule

def rule_based_response(message):
    message = message.lower().strip()
    rules = ChatRule.objects.all()
    for rule in rules:
        if rule.keyword.lower() in message:
            return rule.response
    return "Maaf, saya belum mengerti pertanyaan itu."

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_message = body.get('message', '')
        bot_reply = rule_based_response(user_message)
        return JsonResponse({'reply': bot_reply})
    return JsonResponse({'error': 'Hanya menerima POST'})
def chat_page(request):
    return render(request, 'chatbot/index.html')