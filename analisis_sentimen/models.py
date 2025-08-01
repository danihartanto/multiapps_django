from django.db import models

# sentiment_app/models.py

class SentimentResult(models.Model):
    input_text = models.TextField(help_text="Teks yang dianalisis")
    tokenized_words = models.TextField(help_text="Token hasil tokenisasi, dipisah koma", blank=True)
    matched_words = models.TextField(help_text="Kata yang cocok dengan leksikon beserta bobotnya", blank=True)
    total_score = models.FloatField(help_text="Skor total dari hasil analisis")
    sentiment_label = models.CharField(max_length=10, choices=[
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sentiment_label} ({self.total_score}) - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

