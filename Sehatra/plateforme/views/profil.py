from django.views.generic import TemplateView, CreateView, UpdateView
from ..models import Profil
from paiement.models import Billet


class ProfilCreateView(CreateView):
    model = Profil
    fields = ["nom", "age", "pays", 'devise']
    template_name = "profil_create.html"
    success_url = "/"

    def form_valid(self, form):
        res = form.save(commit=False)
        res.user = self.request.user
        res.save()
        ret = super(ProfilCreateView, self).form_valid(form)
        return ret


class ProfilUpdateView(UpdateView):
    model = Profil
    fields = ["nom", "age", "pays", 'devise']
    template_name = "profil_create.html"
    success_url = "/profil"


class ProfilView(TemplateView):
    template_name = "profil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['object'] = Profil.objects.get(user=self.request.user)
            context['videos'] = [billet.video for billet in Billet.objects.filter(user=self.request.user, valide=True, video__en_ligne=True)]
        except Profil.DoesNotExist:
            context['object'] = None
        return context


class MesVideosView(TemplateView):
    template_name = "mes_videos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = [billet.video for billet in Billet.objects.filter(user=self.request.user, valide=True, video__en_ligne=True)]
        return context

