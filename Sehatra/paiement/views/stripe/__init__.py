from django.views.decorators.csrf import csrf_exempt # new
import stripe
from django.http.response import JsonResponse, HttpResponse
from django.conf import settings # new
from ...models import Paiement, Billet, ModePaiement


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'https://sehatra.com/paiement/stripe/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            paiement = Paiement()
            paiement.mode = ModePaiement.objects.get(nom="Stripe")
            paiement.billet = Billet.objects.get(slug=request.GET['id'])
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'quantity': 1,
                        'price': '{}'.format(paiement.billet.video.stripe_price_id),
                    }
                ]
            )
            paiement.token = checkout_session['id']
            paiement.save()

            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
