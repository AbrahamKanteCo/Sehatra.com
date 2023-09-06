from django.shortcuts import get_object_or_404, render, HttpResponse
from django.views.generic import TemplateView
from ..models import Billet, Paiement, ModePaiement
from .orange_money import get_pay_token, get_transaction_status
from django.shortcuts import redirect, HttpResponseRedirect
from .mvola import get_pay_token_mvola, get_mvola_result
from django import forms
from django.urls import reverse


class PhoneForm(forms.Form):
    telephone = forms.CharField(label='Votre numéro Mvola', max_length=100)


class PaiementView(TemplateView):
    template_name = "paiement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['billet'] = self.billet
        context['video'] = self.billet.video
        return context

    def dispatch(self, request, *args, **kwargs):
        self.billet = get_object_or_404(Billet, slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)


class PaiementMvolaView(TemplateView):
    template_name = "mvola.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['billet'] = self.billet
        context['video'] = self.billet.video
        context['form'] = PhoneForm()
        return context

    def dispatch(self, request, *args, **kwargs):
        self.billet = get_object_or_404(Billet, slug=kwargs['billet'])
        return super().dispatch(request, *args, **kwargs)


class PaiementMvolaVerificationView(TemplateView):
    template_name = "mvola-verification.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['billet'] = self.billet
        context['video'] = self.billet.video
        paiement_mvola(self.billet.slug, self.request.GET.get('telephone', None))
        return context

    def dispatch(self, request, *args, **kwargs):
        self.billet = get_object_or_404(Billet, slug=kwargs['billet'])
        return super().dispatch(request, *args, **kwargs)


def paiement_orange_money(request, billet):
    billet = Billet.objects.get(slug=billet)
    api = get_pay_token(billet).json()
    paiement = Paiement()
    paiement.mode = ModePaiement.objects.get(nom="Orange Money")
    paiement.billet = billet
    paiement.token = api['pay_token']
    paiement.notif_token = api['notif_token']
    paiement.save()
    return redirect(api['payment_url'])


def return_orange_money(request, billet):
    try:
        paiement = Paiement.objects.get(billet__slug=billet)
        result = get_transaction_status(paiement).json()
        if paiement.valide:
            pass
        elif result['status'] == "SUCCESS":
            paiement.valide = True
            paiement.save()
            paiement.billet.valide = True
            paiement.billet.save()
        return HttpResponseRedirect("/video/{}".format(paiement.billet.video.slug))
    except:
        return HttpResponseRedirect("/video/")


def cancel_orange_money(request, billet):
    try:
        paiement = Paiement.objects.get(billet__slug=billet)
        return HttpResponseRedirect("/video/{}".format(paiement.billet.video.slug))
    except:
        return HttpResponseRedirect("/video/")


def notif_orange_money(request):
    paiement = Paiement.objects.get(notif_token=request.POST['notif_token'])
    if request.POST['status'] == "SUCCESS":
        paiement.valide = True
        paiement.billet.valide = True
        paiement.billet.save()
        paiement.save()
    return HttpResponse("Success!")


def success_stripe(request):
    paiement = Paiement.objects.get(token=request.GET['session_id'])
    paiement.valide = True
    paiement.billet.valide = True
    paiement.billet.save()
    paiement.save()
    return HttpResponseRedirect("/video/{}".format(paiement.billet.video.slug))


def cancel_stripe(request):
    return HttpResponseRedirect("/")


def paiement_mvola (billet, numero):
    billet = Billet.objects.get(slug=billet)
    token = get_pay_token_mvola(numero, billet.video.tarif_ariary)
    paiement = Paiement()
    paiement.mode = ModePaiement.objects.get(nom="Mvola")
    paiement.telephone = numero
    paiement.billet = billet
    paiement.token = token
    paiement.save()
    return token


def paiement_mvola_verify (request, billet):
    billet = Billet.objects.get(slug=billet)
    paiements = Paiement.objects.filter(billet__slug= billet)

    for paiement in paiements:
        status = get_mvola_result(paiement.token)
        if status == "completed":
            paiement.valide= True
            billet.valide = True
            paiement.save()
            billet.save()
            return HttpResponseRedirect("/video/{}".format(billet.video.slug))

    return HttpResponseRedirect("/video/{}".format(billet.video.slug))




def paiement_stripe(request, billet):
    return


def paiement_paypal(request, billet):
    return
