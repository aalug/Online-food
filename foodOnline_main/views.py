from django.shortcuts import render
from django.views.generic import TemplateView

from vendor.models import Vendor


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
        context['vendors'] = vendors
        return context
