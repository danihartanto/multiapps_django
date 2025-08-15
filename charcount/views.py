from django.shortcuts import render

from django.shortcuts import render

def count_characters(request):
    result_char = None
    result_word = None
    text = ''
    if request.method == 'POST':
        text = request.POST.get('text', '')
        result_char = len(text)
        result_word = len(text.split())

    return render(request, 'charcount/index.html', {
        'text': text,
        'result_char': result_char,
        'result_word': result_word,
    })

