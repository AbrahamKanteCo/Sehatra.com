from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ..models import *


class AssociationListView(ListView):
    model = Association
    template_name = "association_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Vidéo Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context

    def get_queryset(self):
        return Association.objects.filter(en_ligne=True)


class AssociationDetailView(DetailView):
    model = Association
    template_name = "association_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actions'] = Action.objects.filter(association=context['object'])
        context["title"] = "Vidéo Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context
