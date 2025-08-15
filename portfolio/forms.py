# portfolio/forms.py

from django import forms
from .models import Portfolio, Experience, Education, Project

# class PortfolioForm(forms.ModelForm):
#     class Meta:
#         model = Portfolio
#         fields = ['full_name', 'email', 'phone_number', 'linkedin_url', 'github_url', 'summary', 'skills']
#         widgets = {
#             'summary': forms.Textarea(attrs={'rows': 4}),
#             'skills': forms.Textarea(attrs={'rows': 2}),
#         }

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['full_name', 'email', 'phone_number', 'linkedin_url', 'github_url', 'summary', 'skills']
        widgets = {
            # Tambahkan kelas 'form-control' ke setiap field
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap Anda'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Example: your_email@gmail.com'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomor Telepon Aktif / WA'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Example: https://url_linkedin.com'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Example: https://url_github.com'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detailkan secara singkat backround diri anda', 'rows': 4}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Example: Berfikir Kritis, Suka Belajar, Bisa bekerja dengan tim', 'rows': 2}),
        }

# Lakukan hal yang sama untuk Formsets
ExperienceFormSet = forms.inlineformset_factory(
    Portfolio,
    Experience,
    fields=('job_title', 'company', 'location', 'start_date', 'end_date', 'description'),
    extra=1,
    can_delete=True,
    widgets={
        'job_title': forms.TextInput(attrs={'class': 'form-control'}),
        'company': forms.TextInput(attrs={'class': 'form-control'}),
        'location': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        # Untuk input date, kita juga bisa menambahkan kelas
        'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    }
)
# Untuk form edit data experience
ExperienceFormEditSet = forms.inlineformset_factory(
    Portfolio,
    Experience,
    fields=('job_title', 'company', 'location', 'start_date', 'end_date', 'description'),
    extra=1,
    can_delete=True,
    widgets={
        'job_title': forms.TextInput(attrs={'class': 'form-control'}),
        'company': forms.TextInput(attrs={'class': 'form-control'}),
        'location': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        # Untuk input date, kita juga bisa menambahkan kelas
        'start_date': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control', 'type': 'date'}),
        'end_date': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control', 'type': 'date'}),
    }
)

#form create
EducationFormSet = forms.inlineformset_factory(
    Portfolio,
    Education,
    fields=('institution', 'degree', 'field_of_study', 'start_date', 'end_date'),
    extra=1,
    can_delete=True,
    widgets={
        'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Universitas'}),
        'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lulusan Sarjana, Master, Doctor, Dll..'}),
        'field_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jurusan Teknik Informatika, Pendidikan Bahasa, Ilmu Ekonomi, Dll..'}),
        'start_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
        'end_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
    }
)

#form edit
EducationFormEditSet = forms.inlineformset_factory(
    Portfolio,
    Education,
    fields=('institution', 'degree', 'field_of_study', 'start_date', 'end_date'),
    extra=1,
    can_delete=True,
    widgets={
        'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Universitas'}),
        'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lulusan Sarjana, Master, Doctor, Dll..'}),
        'field_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jurusan Teknik Informatika, Pendidikan Bahasa, Ilmu Ekonomi, Dll..'}),
        'start_date': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control','type': 'date'}),
        'end_date': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control','type': 'date'}),
    }
)

ProjectFormSet = forms.inlineformset_factory(
    Portfolio,
    Project,
    fields=('project_name', 'description', 'technologies_used', 'project_url'),
    extra=1,
    can_delete=True,
    widgets={
        # 'description': forms.Textarea(attrs={'rows': 4}),
        'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Project Anda'}),
        'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deskripsikan project anda'}),
        'technologies_used': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: PHP 8, Laravel, Pyhton, Django, Bootstrap 5, Dll'}),
        'project_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: https://domain_project.com'}),
    }
)