from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ..models import *


class ActualiteListView(ListView):
    model = Actualite
    template_name = "actualite_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Vidéo Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context


class ActualiteDetailView(DetailView):
    model = Actualite
    template_name = "actualite_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Vidéo Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context
