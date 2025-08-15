# news_app/models.py
from django.db import models
from django.contrib.auth.models import User

# Daftar kategori yang akan digunakan untuk dropdown
CATEGORY_CHOICES = [
    ('POLITIK', 'Politik'),
    ('EKONOMI', 'Ekonomi'),
    ('TEKNOLOGI', 'Teknologi'),
    ('OLAHRAGA', 'Olahraga'),
    ('LAINNYA', 'Lainnya'),
]

class NewsArticle(models.Model):
    """
    Model untuk menyimpan artikel berita yang dihasilkan.
    """
    judul = models.CharField(max_length=255, blank=True, null=True)
    hashtag = models.CharField(max_length=255, blank=True, null=True)
    kategori = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='LAINNYA')
    
    what = models.TextField()
    who = models.CharField(max_length=255)
    when = models.DateField(blank=True, null=True)
    where = models.CharField(max_length=255)
    why = models.TextField()
    how = models.TextField()
    
    generated_content = models.TextField(blank=True, null=True)
    
    # Kolom untuk melacak user yang membuat dan mengedit
    creator = models.ForeignKey(User, related_name='created_articles', on_delete=models.SET_NULL, null=True, blank=True)
    editor = models.ForeignKey(User, related_name='edited_articles', on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    diterbitkan_pada = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.judul or f"Berita dari {self.who} pada {self.when}"

