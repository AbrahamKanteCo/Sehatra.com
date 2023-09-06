from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView
from .models import ConcertAccueil, VideoAccueil, Video, Concert, Billet, Paiement
from django.views.generic.detail import DetailView
from django.http import JsonResponse
import json
import requests
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render, HttpResponse
from .forms import FormulaireProCreateForm
from django.urls import reverse_lazy, reverse


# Create your views here.
class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        concert = []
        try:
            con = ConcertAccueil.objects.filter(titre="Accueil")[0]
            if con.concert_1:
                concert.append(con.concert_1)
            if con.concert_2:
                concert.append(con.concert_2)
            if con.concert_3:
                concert.append(con.concert_3)
            context['concert'] = concert
        except:
            context['concert'] = []
        try:
            video = []
            vid = VideoAccueil.objects.filter(titre="Accueil")[0]
            if vid.video_1:
                video.append(vid.video_1)
            if vid.video_2:
                video.append(vid.video_2)
            if vid.video_3:
                video.append(vid.video_3)

            context['video'] = video
        except:
            context['video'] = []

        return context


class TestView(TemplateView):
    template_name = "test-hls.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SupprimerUrl(TemplateView):
    template_name = "confirm_delete_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PolitiqueDeConfidentialiteView(TemplateView):
    template_name = "politique-de-confidentialite.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CGUView(TemplateView):
    template_name = "cgu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AproposView(TemplateView):
    template_name = "a-propos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class VideoDetailView(DetailView):
    model = Video
    template_name = "video_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device'] = self.request.user_agent.os.family
        if self.object.acces_libre:
            context["access"] = True
        else:
            context["access"] = False
            billet = Billet.objects.filter(user=self.request.user, valide=True)
            if len(billet)>0:
                context['access'] = True
        return context


class VenteBilletConcertView (DetailView):
    model = Concert
    template_name = "concert_billet_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            billet = Billet.objects.filter(user=self.request.user, concert=self.object, valide=True)
            if len(billet)>0:
                context['avec_billet'] = True
                context['billet'] = billet[0]
                print (billet[0])
            else:
                context['avec_billet'] = False
        except:
            context['avec_billet'] = False

        return context


class ConcertView(DetailView):
    model = Concert
    template_name = "concert_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.billet = get_object_or_404(Billet, slug=kwargs['billet'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.billet.user == self.request.user and self.billet.valide:
                access = True
            else:
                access = False
            context['access'] = access
        except:
            context['access'] = False

        return context


class ConcertTestView(DetailView):
    model = Concert
    template_name = "concert_test_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.billet = get_object_or_404(Billet, slug=kwargs['billet'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.billet.user == self.request.user and self.billet.valide:
                access = True
            else:
                access = False
            context['access'] = access
        except:
            context['access'] = False

        return context


def paiement(request, slug, mode):

    lien = "https://sehatra.com"
    billet = Billet()
    billet.user = request.user
    billet.concert = Concert.objects.get(slug=slug)
    billet.save()
    access_token = "f3644d524e292a191fb0c8d64df6696cf5481d9daf7b6e7afc802882e187831a"
    url_paiement = "https://api.moobipay.com/v1/payment-init"
    header = {"Authorization": "Bearer " + access_token}
    data= {}


    if mode == "mvola":
        data['service'] = "mv"
        data['currency'] = "MGA"
        data['amount'] = "50000"
    elif mode == "visa-mastercard-ariary":
        data['service'] = "visa"
        data['currency'] = "MGA"
        data['amount'] = "50000"
    elif mode == "orange-money":
        data['service'] = "om"
        data['currency'] = "MGA"
        data['amount'] = "50000"
    elif mode == "visa-mastercard-euro":
        data['service'] = "visa"
        data['currency'] = "EUR"
        data['amount'] = "13"


    data['order_id'] = billet.slug
    data['order_label'] = "Paiement pour "+ billet.concert.titre
    data['return_url'] = lien+"/concert/{}/billet/{}/success".format(billet.concert.slug, billet.slug)
    data['notif_url'] = lien+"/concert/{}/billet/{}/notif".format(billet.concert.slug, billet.slug)
    data['cancel_url'] = lien+"/concert/{}/billet/{}/cancel".format(billet.concert.slug, billet.slug)
    res = requests.post(url_paiement, json=data, headers= header)
    pay_url = res.json()['pay_url']
    paiement = Paiement()
    paiement.billet = billet
    paiement.mode_de_paiement = "Moobi Pay"
    paiement.token = res.json()['pay_token']
    paiement.save()
    try:
        url_notif = "https://rc29esj8k5.execute-api.us-east-1.amazonaws.com/default/send-sms"
        requests.get(url_notif)
    except:
        pass
    return redirect(pay_url)


def paiement_success(request, slug, billet):
    billet = Billet.objects.get(slug=billet)
    billet.valide= True
    billet.save()
    paiement = Paiement.objects.get(billet=billet)
    paiement.valide= True
    paiement.save()
    return redirect("/concert/{}".format(slug))


def suppr_user(request):
    request.user.is_active = False
    request.user.save()
    return redirect("/")


def paiement_notif(request, slug, billet):
    billet = Billet.objects.get(slug=billet)
    return redirect("/concert/{}".format(slug))


def paiement_cancel(request, slug, billet):
    billet = Billet.objects.get(slug=billet)
    billet.delete()
    return redirect("/concert/{}".format(slug))


def check_user(request):
    if request.user.is_authenticated:
        data = {
            'user': True,
        }
    else:
        data = {
            'user': False,
        }

    return JsonResponse(data)


class FormulaireCreateProView(CreateView):
    template_name = 'create_formulaire.html'
    form_class = FormulaireProCreateForm
    success_message = 'Formulaire envoyé avec succès'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        formulaire = form.save(commit=False)
        formulaire.user = self.request.user
        return super(FormulaireCreateProView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
