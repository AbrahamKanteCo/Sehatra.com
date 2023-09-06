from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ..models import *


class ArtisteListView(ListView):
    model = Artiste
    template_name = "artiste_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Vidéo Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context

    def get_queryset(self):
        return Artiste.objects.filter(en_ligne=True)


class ArtisteDetailView(DetailView):
    model = Artiste
    template_name = "artiste_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(artiste=context['object'])
        context["title"] = "Vidéo Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context
