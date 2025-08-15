# news_app/forms.py
from django import forms
from .models import NewsArticle

class NewsArticleForm(forms.ModelForm):
    """
    Form untuk mengambil input 5W+1H dari user.
    """
    class Meta:
        model = NewsArticle
        # Tambahkan field baru ke daftar fields
        fields = ['kategori','diterbitkan_pada', 'what', 'who', 'when', 'where', 'why', 'how', 'image','generated_content','judul']
        widgets = {
            # 'judul': forms.TextInput(attrs={'class': 'form-control mt-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Judul artikel (opsional)'}),
            # 'hashtag': forms.TextInput(attrs={'class': 'form-control mt-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': '#hashtag (opsional)'}),
            'kategori': forms.Select(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3'}),
            'what': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Peristiwa apa yang terjadi?'}),
            'who': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Siapa saja yang terlibat?'}),
            # 'when': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Kapan peristiwa itu terjadi?'}),
            'when': forms.DateInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'type': 'date'}),
            'where': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Di mana peristiwa itu terjadi?'}),
            'why': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Mengapa peristiwa itu terjadi?'}),
            'how': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Bagaimana proses terjadinya?'}),
            'diterbitkan_pada': forms.DateInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'type': 'date'}),
            'generated_content': forms.Textarea(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'rows': 10}),
            'judul': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Judul berita'}),
        }
        

class NewsArticleCreateForm(forms.ModelForm):
    """
    Form untuk membuat artikel baru (halaman generator).
    Ini tidak termasuk field generated_content, judul, dan hashtag.
    """
    class Meta:
        model = NewsArticle
        fields = ['kategori', 'what', 'who', 'when', 'where', 'why', 'how', 'image']
        widgets = {
            # 'judul': forms.TextInput(attrs={'class': 'form-control mt-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Judul artikel (opsional)'}),
            # 'hashtag': forms.TextInput(attrs={'class': 'form-control mt-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': '#hashtag (opsional)'}),
            'kategori': forms.Select(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3'}),
            'what': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Peristiwa apa yang terjadi?'}),
            'who': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Siapa saja yang terlibat?'}),
            'when': forms.DateInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'type': 'date'}),
            'where': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Di mana peristiwa itu terjadi?'}),
            'why': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Mengapa peristiwa itu terjadi?'}),
            'how': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Bagaimana proses terjadinya?'}),
        }

class NewsArticleEditForm(forms.ModelForm):
    """
    Form untuk mengedit artikel yang sudah ada.
    Ini termasuk field generated_content, judul, dan hashtag.
    """
    class Meta:
        model = NewsArticle
        fields = ['judul', 'hashtag', 'kategori', 'image', 'diterbitkan_pada', 'generated_content']
        widgets = {
            # 'judul': forms.TextInput(attrs={'class': 'form-control mt-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Judul artikel (opsional)'}),
            # 'hashtag': forms.TextInput(attrs={'class': 'form-control mt-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': '#hashtag (opsional)'}),
            'kategori': forms.Select(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3'}),
            # 'what': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Peristiwa apa yang terjadi?'}),
            # 'who': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Siapa saja yang terlibat?'}),
            # 'when': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Kapan peristiwa itu terjadi?'}),
            # 'when': forms.DateInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'type': 'date'}),
            # 'where': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Di mana peristiwa itu terjadi?'}),
            # 'why': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Mengapa peristiwa itu terjadi?'}),
            # 'how': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Bagaimana proses terjadinya?'}),
            'diterbitkan_pada': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'type': 'date'}),
            'generated_content': forms.Textarea(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'rows': 30}),
            'judul': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Judul berita'}),
            'hashtag': forms.TextInput(attrs={'class': 'form-control mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3', 'placeholder': 'Hashtag berita'}),
        }