import os
import csv
import string
import re

from django.shortcuts import render
from .forms import SentimentForm
from .models import SentimentResult
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

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
                    num_words = int(num_words)
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
    print(lexicon_list)
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
                    input_text=raw_text,
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
