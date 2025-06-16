# sentiment_app/forms.py

from django import forms

class SentimentForm(forms.Form):
    input_text = forms.CharField(
        label='Masukkan Teks',
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Tulis teks di sini...',
            'autofocus': 'autofocus'  # Tambahkan ini
        })
    )
