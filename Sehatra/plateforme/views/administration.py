from ..models import *
from django.views.generic import TemplateView
from paiement.models import *



class AdministrationView(TemplateView):
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organisateur = Organisateur.objects.get(user= self.request.user)
        context['videos'] = Video.objects.filter(organisateur= organisateur)
        paiements = Paiement.objects.filter(billet__video__organisateur= organisateur, valide=True,
                                            billet__gratuit=False).order_by("-date")
        somme = 0
        cours_euro = 4700

        for paiement in paiements:
            if paiement.mode == 3:
                somme += paiement.billet.video.tarif_euro * cours_euro
            else:
                somme += paiement.billet.video.tarif_ariary
        context['somme'] = somme *75 / 100

        context['organisateur'] = organisateur
        context["paiements"] = paiements
        context['nb_billet'] = len(paiements)
        context["title"] = "Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context
