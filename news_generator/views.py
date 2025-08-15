# news_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewsArticleCreateForm, NewsArticleEditForm
import json
import requests
from .models import NewsArticle
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

#jangan hapus ini
#api_key = "AIzaSyAKWaOTdVuBUXbxeSqYJKHxDis5Oewmyy4"  
#api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
                
                

@login_required
def news_generator_view(request):
    """
    View berbasis fungsi untuk menangani form input dan menghasilkan berita.
    """
    generated_text = None
    news_article = None

    if request.method == 'POST':
        form = NewsArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            news_article = form.save(commit=False)
            
            prompt = f"""
                Bertindaklah sebagai jurnalis profesional. Susunlah sebuah artikel berita yang kohesif dan menarik berdasarkan fakta-fakta berikut dalam bahasa Indonesia. Minimal generate 100 kata, tapi lebih banyak lebih baik.
                Sertakan judul yang menarik, paragraf pembuka, dan deskripsi detail peristiwa. Untuk hasil query hanya tampilkan hasil berita saja, hapus prompt awal anda, jadi langsung dari judul. Ganti tanda ** (double bintang) menjadi spasi kosong atau dihilangkan saja dari kalimat. Ganti tanda ** (double bintang) menjadi  (whitespace) pada awal kalimat dan  (whitespace) pada akhir kalimat.
                
                Apa (Peristiwa): {news_article.what}
                Siapa (Pelaku): {news_article.who}
                Kapan (Waktu): {news_article.when}
                Di mana (Lokasi): {news_article.where}
                Mengapa (Alasan): {news_article.why}
                Bagaimana (Proses): {news_article.how}
            """

            try:
                # Placeholder untuk API call ke Gemini.
                # Di lingkungan Canvas, apiKey akan disediakan secara otomatis.
                api_key = "AIzaSyAKWaOTdVuBUXbxeSqYJKHxDis5Oewmyy4"  
                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                }

                response = requests.post(
                    api_url,
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(payload)
                )
                response.raise_for_status()
                result = response.json()

                generated_content = result['candidates'][0]['content']['parts'][0]['text']
                news_article.generated_content = generated_content
                
                # Mengisi kolom judul dan hashtag secara otomatis dari generated_content
                if not news_article.judul:
                    lines = generated_content.split('\n')
                    news_article.judul = lines[0] if lines else "Judul Berita Tanpa Nama"
                
                if not news_article.hashtag:
                    words = generated_content.split()
                    hashtags = ['#' + word.strip(',.!?').lower() for word in words if len(word) > 3 and word.isalpha()]
                    news_article.hashtag = ' '.join(hashtags[:5]) # Ambil 5 hashtag pertama

            except Exception as e:
                generated_content = f"Error saat menghasilkan berita: {e}"
                news_article.generated_content = generated_content
            
            # Tambahkan creator sebelum menyimpan
            if request.user.is_authenticated:
                news_article.creator = request.user
            
            news_article.save()
            return redirect('news_app:list')
            # form = NewsArticleForm()
    else:
        form = NewsArticleCreateForm()

    return render(request, 'news_generator/index.html', {
        'form': form,
        'generated_text': generated_text,
        'news_article': news_article
    })

def news_list_view(request):
    """
    View untuk menampilkan daftar semua artikel berita yang telah dihasilkan.
    """
    # Ambil semua artikel berita yang ada
    all_articles = NewsArticle.objects.order_by('-created_at')
    
    # Tambahkan pagination untuk menangani banyak artikel
    paginator = Paginator(all_articles, 10)  # Tampilkan 10 artikel per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news_generator/news_lists.html', {'page_obj': page_obj})

def news_detail_view(request, article_id):
    """
    View untuk menampilkan detail satu artikel berita.
    """
    article = get_object_or_404(NewsArticle, pk=article_id)
    return render(request, 'news_generator/news_detail.html', {'article': article})

@login_required
def news_edit_view(request, article_id):
    """
    View untuk mengedit artikel berita yang sudah ada.
    """
    article = get_object_or_404(NewsArticle, pk=article_id)
    if request.method == 'POST':
        form = NewsArticleEditForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            # Update editor field
            if request.user.is_authenticated:
                article.editor = request.user
            form.save()
            return redirect('news_app:detail', article_id=article.id)
    else:
        form = NewsArticleEditForm(instance=article)
    # return render(request, 'news_app/news_edit.html', {'form': form, 'article': article})
    return render(request, 'news_generator/news_edit.html', {'form': form, 'article': article})


def news_delete_view(request, article_id):
    """
    View untuk menghapus artikel berita.
    """
    article = get_object_or_404(NewsArticle, pk=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('news_app:list')
    return render(request, 'news_generator/news_confirm_delete.html', {'article': article})
