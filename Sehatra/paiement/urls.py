from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from .views import *


urlpatterns = [
    path('<slug:slug>/', login_required(PaiementView.as_view()), name="paiement"),
    path('<slug:billet>/orange-money/', login_required(paiement_orange_money), name="paiement-orange-money"),
    path('<slug:billet>/mvola/', login_required(PaiementMvolaView.as_view()), name="paiement-mvola-initiation"),
    path('orange-money/return/<slug:billet>/', return_orange_money, name="return-orange-money"),
    path('orange-money/cancel/<slug:billet>/', cancel_orange_money, name="cancel-orange-money"),
    path('orange-money/notif/<slug:billet>/', notif_orange_money, name="notif-orange-money"),
    path('stripe/config/', stripe_config, name="stripe-config"),
    path('stripe/create-checkout-session/', create_checkout_session, name="stripe-checkout"),
    path('stripe/success/', success_stripe, name="stripe-success"),
    path('stripe/cancel/', cancel_stripe, name="stripe-cancel"),
    path('<slug:billet>/mvola/verification/', login_required(PaiementMvolaVerificationView.as_view()), name="paiement-mvola-verification"),
    path('mvola/verification/<slug:billet>/', paiement_mvola_verify, name="paiement-mvola-verification"),
    path('<slug:billet>/stripe/', login_required(paiement_stripe), name="paiement-stripe"),
    path('<slug:billet>/paypal/', login_required(paiement_paypal), name="paiement-paypal"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
