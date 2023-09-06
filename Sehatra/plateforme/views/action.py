from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ..models import *


class ActionListView(ListView):
    model = Action
    template_name = "action_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context

    def get_queryset(self):
        return Action.objects.filter(en_ligne=True)


class ActionDetailView(DetailView):
    model = Action
    template_name = "action_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(action=context['object'])
        context["title"] = "Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context
