from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/users/login'
    template_name = 'templates/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
