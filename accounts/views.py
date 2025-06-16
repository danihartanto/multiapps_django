from allauth.account.views import LogoutView as AllauthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLogoutView(LoginRequiredMixin, AllauthLogoutView):
    template_name = "account/logout.html"  # pastikan template ini tersedia

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username  # Tambahan info user jika ingin ditampilkan
        return context
