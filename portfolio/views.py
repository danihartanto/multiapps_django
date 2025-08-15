# portfolio/views.py
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin # <-- 1. Impor untuk Class-based View
from django.contrib.auth.decorators import login_required # <-- 2. Impor untuk Function-based View
from .models import Portfolio
from .forms import PortfolioForm, ExperienceFormSet, ExperienceFormEditSet, EducationFormSet, EducationFormEditSet, ProjectFormSet
from .utils import render_to_pdf # 1. Impor fungsi helper kita
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy

# 3. Tambahkan LoginRequiredMixin
class PortfolioCreateView(LoginRequiredMixin, View):
    template_name = 'portfolio/portfolio_form.html'

    def get(self, request, *args, **kwargs):
        # Logika GET tetap sama
        form = PortfolioForm()
        experience_formset = ExperienceFormSet()
        education_formset = EducationFormSet()
        project_formset = ProjectFormSet()
        return render(request, self.template_name, {
            'form': form,
            'experience_formset': experience_formset,
            'education_formset': education_formset,
            'project_formset': project_formset,
        })

    def post(self, request, *args, **kwargs):
        form = PortfolioForm(request.POST)
        
        if form.is_valid():
            # 4. Jangan simpan dulu, kaitkan dengan user yang login
            portfolio = form.save(commit=False)
            portfolio.user = request.user # <-- Mengaitkan dengan user aktif
            portfolio.save() # <-- Baru simpan ke database
            
            experience_formset = ExperienceFormSet(request.POST, instance=portfolio)
            education_formset = EducationFormSet(request.POST, instance=portfolio)
            project_formset = ProjectFormSet(request.POST, instance=portfolio)

            if experience_formset.is_valid() and education_formset.is_valid() and project_formset.is_valid():
                experience_formset.save()
                education_formset.save()
                project_formset.save()
                return redirect(portfolio.get_absolute_url())

        # Logika jika tidak valid tetap sama
        experience_formset = ExperienceFormSet(request.POST)
        education_formset = EducationFormSet(request.POST)
        project_formset = ProjectFormSet(request.POST)
        
        return render(request, self.template_name, {
            'form': form,
            'experience_formset': experience_formset,
            'education_formset': education_formset,
            'project_formset': project_formset,
        })
# --- TAMBAHKAN CLASS BARU DI BAWAH INI ---
class PortfolioUpdateView(LoginRequiredMixin, View):
    template_name = 'portfolio/portfolio_form.html'

    def get(self, request, pk, *args, **kwargs):
        # 1. Ambil portfolio yang mau diedit. Pastikan hanya pemilik yang bisa edit.
        portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)

        # 2. Isi form & formset dengan data yang sudah ada (menggunakan 'instance')
        form = PortfolioForm(instance=portfolio)
        experience_formset = ExperienceFormEditSet(instance=portfolio)
        education_formset = EducationFormEditSet(instance=portfolio)
        project_formset = ProjectFormSet(instance=portfolio)
        
        return render(request, self.template_name, {
            'form': form,
            'experience_formset': experience_formset,
            'education_formset': education_formset,
            'project_formset': project_formset,
            'is_update': True # Flag untuk template
        })

    def post(self, request, pk, *args, **kwargs):
        # 3. Ambil lagi portfolio yang mau diedit
        portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
        
        # 4. Proses data POST dengan instance yang sudah ada
        form = PortfolioForm(request.POST, instance=portfolio)
        experience_formset = ExperienceFormSet(request.POST, instance=portfolio)
        education_formset = EducationFormSet(request.POST, instance=portfolio)
        project_formset = ProjectFormSet(request.POST, instance=portfolio)

        if form.is_valid() and experience_formset.is_valid() and education_formset.is_valid() and project_formset.is_valid():
            form.save()
            experience_formset.save()
            education_formset.save()
            project_formset.save()
            # 5. Arahkan kembali ke halaman detail setelah berhasil
            return redirect(portfolio.get_absolute_url())

        # Jika tidak valid, tampilkan kembali form dengan error
        return render(request, self.template_name, {
            'form': form,
            'experience_formset': experience_formset,
            'education_formset': education_formset,
            'project_formset': project_formset,
            'is_update': True
        })
# --- TAMBAHKAN CLASS DELETE BARU DI BAWAH INI ---
class PortfolioDeleteView(LoginRequiredMixin, View):
    template_name = 'portfolio/portfolio_confirm_delete.html'
    success_url = reverse_lazy('portfolio_index') # Halaman tujuan setelah berhasil hapus

    def get(self, request, pk, *args, **kwargs):
        # Ambil portfolio untuk ditampilkan di halaman konfirmasi
        # Pastikan hanya pemilik yang bisa mengakses halaman ini
        portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
        return render(request, self.template_name, {'portfolio': portfolio})

    def post(self, request, pk, *args, **kwargs):
        # Ambil portfolio yang akan dihapus
        portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
        
        # Hapus objek dari database
        portfolio.delete()

        # Opsional: Tambahkan pesan sukses
        messages.success(request, 'Portofolio Anda telah berhasil dihapus.')
        
        # Arahkan ke halaman sukses
        return redirect(self.success_url)
# TAMBAHKAN VIEW BARU DI BAWAH INI
@login_required
def index_view(request):
    """
    Menampilkan portofolio jika ada, atau pesan untuk membuat portofolio jika tidak ada.
    """
    portfolio = None
    skills_list = []
    
    # Coba temukan portofolio milik user yang sedang login
    try:
        portfolio = Portfolio.objects.get(user=request.user)
        skills_list = [skill.strip() for skill in portfolio.skills.split(',')]
    except Portfolio.DoesNotExist:
        # Jika tidak ditemukan, 'portfolio' akan tetap None
        pass

    context = {
        'portfolio': portfolio,
        'skills_list': skills_list
    }
    return render(request, 'portfolio/index.html', context)


@login_required
def portfolio_detail_view(request): # <-- Hapus 'pk'
    # 6. Ambil portfolio berdasarkan user yang sedang login, bukan berdasarkan pk
    portfolio = get_object_or_404(Portfolio, user=request.user)
    
    skills_list = [skill.strip() for skill in portfolio.skills.split(',')]
    context = {
        'portfolio': portfolio,
        'skills_list': skills_list,
    }
    return render(request, 'portfolio/portfolio_detail_ats.html', context)

@login_required
def generate_portfolio_pdf(request):
    """
    View untuk membuat PDF menggunakan xhtml2pdf melalui fungsi utilitas.
    """
    # Ambil data portfolio (logika ini tidak berubah)
    portfolio = get_object_or_404(Portfolio, user=request.user)
    skills_list = [skill.strip() for skill in portfolio.skills.split(',')]
    context = {
        'portfolio': portfolio,
        'skills_list': skills_list,
    }

    # 2. Panggil fungsi render_to_pdf dari utils.py
    pdf = render_to_pdf('portfolio/portfolio_preview.html', context)

    # 3. Tentukan preview atau download (logika ini tidak berubah)
    action = request.GET.get('action', 'download')
    if action == 'preview':
        disposition = 'inline'
    else:
        disposition = 'attachment'
    
    pdf['Content-Disposition'] = f'{disposition}; filename="portfolio_{portfolio.full_name}.pdf"'
    
    return pdf
@login_required
def portfolio_preview_html(request):
    """
    Menampilkan halaman preview HTML yang gayanya disamakan dengan PDF.
    """
    portfolio = get_object_or_404(Portfolio, user=request.user)
    skills_list = [skill.strip() for skill in portfolio.skills.split(',')]
    context = {
        'portfolio': portfolio,
        'skills_list': skills_list,
    }
    
    # Render template preview yang baru
    return render(request, 'portfolio/portfolio_preview.html', context)

