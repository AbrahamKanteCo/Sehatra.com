from django.http import JsonResponse
from .action import *
from .association import *
from .artiste import *
from .organisateur import *
from django.views.generic import TemplateView, FormView, CreateView
from .video import *
from .billet import billet_create
from .profil import *
from .administration import AdministrationView
from .test import TestView

from django.middleware.csrf import get_token


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(en_ligne=True, is_live=False, is_film=False)
        context['lives'] = Video.objects.filter(en_ligne=True, is_live=True)
        context['films'] = Video.objects.filter(en_ligne=True, is_film=True)
        context["title"] = "Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context
    
    def csrf(request):
        token = get_token(request)
        return JsonResponse({'csrfToken': token})


class PolitiqueDeConfidentialiteView(TemplateView):
    template_name = "politique-de-confidentialite.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context


class CGUView(TemplateView):
    template_name = "cgu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        context = super().get_context_data(**kwargs)
        return context


