from django.db import models

# Create your models here.
# portfolio/models.py
from django.urls import reverse
from django.conf import settings # <-- 1. Tambahkan impor ini

class Portfolio(models.Model):
    # 2. Tambahkan field ini. Letakkan di paling atas untuk kerapian.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    summary = models.TextField(help_text="Tulis ringkasan profesional tentang diri Anda.")
    skills = models.TextField(help_text="Sebutkan skill Anda, pisahkan dengan koma (contoh: Python, Django, Data Analysis)")

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        # Nanti kita akan sesuaikan URL ini agar tidak pakai 'pk'
        return reverse('my_portfolio_detail')

class Experience(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='experiences', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Kosongkan jika masih bekerja di sini")
    description = models.TextField(help_text="Jelaskan tanggung jawab dan pencapaian Anda dalam bentuk poin-poin.")

    def __str__(self):
        return f"{self.job_title} at {self.company}"

class Education(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='educations', on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} in {self.field_of_study}"

class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='projects', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.CharField(max_length=200, help_text="Contoh: Django, React, PostgreSQL")
    project_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.project_name