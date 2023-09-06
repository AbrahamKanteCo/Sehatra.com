from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ..models import *


class OrganisateurListView(ListView):
    model = Organisateur
    template_name = "organisateur_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Organisateurs Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context

    def get_queryset(self):
        return Organisateur.objects.filter(en_ligne=True)


class OrganisateurDetailView(DetailView):
    model = Organisateur
    template_name = "organisateur_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(organisateur=context['object'])
        context["title"] = "{} - Organisateurs sur Sehatra.com".format(context['object'].nom)
        context["image"] = context['object'].photo_de_couverture.url
        return context
