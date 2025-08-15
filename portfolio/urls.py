# portfolio/urls.py

from django.urls import path
from .views import PortfolioCreateView, portfolio_detail_view, index_view, PortfolioUpdateView, generate_portfolio_pdf, portfolio_preview_html, PortfolioDeleteView

urlpatterns = [
    path('', index_view, name='portfolio_index'), # <-- Tambahkan URL ini di paling atas
    path('create/', PortfolioCreateView.as_view(), name='portfolio_create'),
    path('my-portfolio/', portfolio_detail_view, name='my_portfolio_detail'),
    path('my-portfolio/pdf/', generate_portfolio_pdf, name='portfolio_pdf'), # 2. Tambahkan URL untuk download PDF
    path('<int:pk>/edit/', PortfolioUpdateView.as_view(), name='portfolio_update'),
    # 2. Tambahkan URL untuk halaman preview HTML
    path('my-portfolio/preview/', portfolio_preview_html, name='portfolio_preview'),
    # 2. Tambahkan URL untuk halaman hapus
    path('<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio_delete'),
]