import os
import csv
import string
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from django.conf import settings
from django.shortcuts import render
from .forms import SentimentForm
from .models import SentimentResult
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

#cek apakah dia staff atau bukan
# berikan @is_staff_user pada tiap fungsi yg hanya staff bisa akses
def is_staff_user(user):
    return user.is_authenticated and user.is_staff

# === Konfigurasi dasar path ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# link dataset https://github.com/MohFahmi27/Sentiment-Analysis-for-Bahasa-using-Lexicon-Based-Approach/blob/main/data/datasetAnalysis/lexicon-word-dataset.csv
LEXICON_FILE = os.path.join(BASE_DIR, 'data', 'lexicon', 'lexicon_dataset.tsv')

# === Setup Stemmer Bahasa Indonesia ===
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# === Fungsi Preprocessing (cleaning + stemming) ===
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # hilangkan tanda baca
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_text(text):
    cleaned = clean_text(text)
    return stemmer.stem(cleaned)

# === Fungsi baca lexicon dari file lokal ===
def load_lexicons():
    lexicon_list = []
    try:
        with open(LEXICON_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                word = row.get('word', '').strip().lower()
                weight = row.get('weight', '0').strip()
                num_words = row.get('number_of_words', str(len(word.split()))).strip()

                if not word:
                    continue

                try:
                    weight = float(weight)
                    num_words = int(float(num_words))  # kalau 1.0 → 1
                    lexicon_list.append({
                        'word': word,
                        'weight': weight,
                        'number_of_words': num_words
                    })
                except ValueError:
                    continue
    except FileNotFoundError:
        print("File lexicon_dataset.tsv tidak ditemukan di path:", LEXICON_FILE)

    # Urutkan dari frasa terpanjang agar tidak terjadi overlap match
    return sorted(lexicon_list, key=lambda x: -x['number_of_words'])

# === Fungsi analisis sentimen ===
def sentiment_analysis(text):
    lexicons = load_lexicons()
    matched = []
    total_score = 0

    tokens = text.split()
    used_indices = set()

    for lex in lexicons:
        n = lex['number_of_words']
        if n > len(tokens):
            continue

        for i in range(len(tokens) - n + 1):
            if any(j in used_indices for j in range(i, i + n)):
                continue

            window = ' '.join(tokens[i:i + n])
            if window == lex['word']:
                matched.append((lex['word'], lex['weight']))
                total_score += lex['weight']
                used_indices.update(range(i, i + n))
                break

    label = 'neutral'
    if total_score > 0:
        label = 'positive'
    elif total_score < 0:
        label = 'negative'

    return tokens, matched, total_score, label

# === View utama ===
def analyze_text(request):
    result = None
    if request.method == 'POST':
        if 'reset' in request.POST:
            form = SentimentForm()
        else:
            form = SentimentForm(request.POST)
            if form.is_valid():
                raw_text = form.cleaned_data['input_text']
                processed_text = preprocess_text(raw_text)
                tokens, matched, score, label = sentiment_analysis(processed_text)

                # Simpan ke DB
                SentimentResult.objects.create(
                    # input_text=raw_text,
                    input_text=processed_text, #teks yg disimpan adalah teks yg sudah bersih
                    tokenized_words=",".join(tokens),
                    matched_words=",".join([f"{w}:{s}" for w, s in matched]),
                    total_score=score,
                    sentiment_label=label
                )

                result = {
                    'original': raw_text,
                    'processed': processed_text,
                    'tokens': tokens,
                    'matched': matched,
                    'score': score,
                    'label': label
                }
    else:
        form = SentimentForm()

    return render(request, 'analisis_sentimen/index.html', {
        'form': form,
        'result': result
    })

# menampilkan data hasil sentimen dari DB
def sentiment_history(request):
    search = request.GET.get('q', '')
    label_filter = request.GET.get('label', '')
    results = SentimentResult.objects.all().order_by('-created_at')

    if search:
        results = results.filter(input_text__icontains=search)
    if label_filter:
        results = results.filter(sentiment_label=label_filter)

    return render(request, 'analisis_sentimen/history.html', {
        'results': results  # kirim semua data
    })

@csrf_exempt
def delete_sentiment(request, id):
    if request.method == 'POST':
        try:
            obj = SentimentResult.objects.get(id=id)
            obj.delete()
            return JsonResponse({'message': 'Data berhasil dihapus'})
        except SentimentResult.DoesNotExist:
            return JsonResponse({'error': 'Data tidak ditemukan'}, status=404)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def update_sentiment(request, id):
    if request.method == 'POST':
        try:
            obj = SentimentResult.objects.get(id=id)
            obj.tokenized_words = request.POST.get('tokenized_words', obj.tokenized_words)
            obj.matched_words = request.POST.get('matched_words', obj.matched_words)
            obj.sentiment_label = request.POST.get('sentiment_label', obj.sentiment_label)
            obj.total_score = float(request.POST.get('total_score', obj.total_score))
            obj.save()
            return JsonResponse({'message': 'Data berhasil diperbarui'})
        except SentimentResult.DoesNotExist:
            return JsonResponse({'error': 'Data tidak ditemukan'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return HttpResponseNotAllowed(['POST'])

@user_passes_test(is_staff_user)
@login_required
def list_data_lexicon(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("Anda tidak memiliki akses ke halaman ini.")
    tsv_path = os.path.join(settings.BASE_DIR, 'data', 'lexicon', 'lexicon_dataset.tsv')
    data = []

    try:
        with open(tsv_path, newline='', encoding='utf-8') as tsvfile:
            reader = csv.reader(tsvfile, delimiter=',')  # Sesuaikan: pakai koma
            headers = next(reader, [])
            for row in reader:
                if len(row) == len(headers):  # ✅ Validasi jumlah kolom
                    data.append(row)
    except FileNotFoundError:
        headers = []
        data = []

    return render(request, 'analisis_sentimen/list_data_lexicon.html', {
        'headers': headers,
        'data': data,
    })

@user_passes_test(is_staff_user)
@login_required
@csrf_exempt
def add_lexicon_entry(request):
    if request.method == 'POST':
        word = request.POST.get('word', '').strip().lower()
        weight = request.POST.get('weight', '').strip()
        number_of_words = request.POST.get('number_of_words', '').strip()

        if not word or not weight or not number_of_words:
            return JsonResponse({'error': 'Semua field harus diisi.'}, status=400)

        try:
            float(weight)
            int(number_of_words)
        except ValueError:
            return JsonResponse({'error': 'Skor harus angka, jumlah kata harus bilangan bulat'}, status=400)

        tsv_path = os.path.join(settings.BASE_DIR, 'data', 'lexicon', 'lexicon_dataset.tsv')

        with open(tsv_path, newline='', encoding='utf-8') as file:
            reader = list(csv.reader(file, delimiter=','))
            headers = reader[0]
            data = reader[1:]

        # Cek duplikat berdasarkan word
        for row in data:
            if row[1].strip().lower() == word:
                return JsonResponse({'error': f'Kata "{word}" sudah ada.'}, status=400)

        last_index = max([int(row[0]) for row in data]) if data else 0
        new_index = last_index + 1

        with open(tsv_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow([new_index, word, weight, number_of_words])

        return JsonResponse({'message': 'Berhasil ditambahkan'})

@user_passes_test(is_staff_user)
@login_required
@csrf_exempt
def update_lexicon_entry(request):
    if request.method == 'POST':
        try:
            index = int(request.POST.get('index'))
            word = request.POST.get('word').strip()
            weight = request.POST.get('weight').strip()
            number_of_words = request.POST.get('number_of_words').strip()

            tsv_path = os.path.join(settings.BASE_DIR, 'data', 'lexicon', 'lexicon_dataset.tsv')

            with open(tsv_path, newline='', encoding='utf-8') as file:
                rows = list(csv.reader(file, delimiter=','))

            headers = rows[0]
            updated = False

            for i, row in enumerate(rows[1:], start=1):
                if int(row[0]) == index:
                    rows[i] = [index, word, weight, number_of_words]
                    updated = True
                    break

            if not updated:
                return JsonResponse({'error': 'Index tidak ditemukan'}, status=404)

            with open(tsv_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerows(rows)

            return JsonResponse({'message': 'Update berhasil'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@user_passes_test(is_staff_user)
@login_required
@csrf_exempt
def delete_lexicon_entry(request):
    if request.method == 'POST':
        try:
            target_index = int(request.POST.get('index'))

            tsv_path = os.path.join(settings.BASE_DIR, 'data', 'lexicon', 'lexicon_dataset.tsv')
            with open(tsv_path, newline='', encoding='utf-8') as file:
                rows = list(csv.reader(file, delimiter=','))

            header = rows[0]
            data_rows = rows[1:]

            new_data = [row for row in data_rows if int(row[0]) != target_index]

            if len(new_data) == len(data_rows):
                return JsonResponse({'error': 'Index tidak ditemukan'}, status=404)

            # Tulis ulang (dengan header)
            with open(tsv_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(header)
                writer.writerows(new_data)

            return JsonResponse({'message': 'Baris berhasil dihapus'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
