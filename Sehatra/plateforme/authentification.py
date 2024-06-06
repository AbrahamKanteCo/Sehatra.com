import traceback
from django.contrib.auth.backends import ModelBackend
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

import random
import string

from plateforme.models import ConfirmationCode, CustomUserCreationForm
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from allauth.socialaccount.models import SocialAccount



class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get('token')
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request())

            user, created = User.objects.get_or_create(email=idinfo['email'], defaults={
                'username': idinfo.get('name'),
                'first_name': idinfo.get('given_name'),
                'last_name': idinfo.get('family_name'),
            })

            if not created:
                user.first_name = idinfo.get('given_name', user.first_name)
                user.last_name = idinfo.get('family_name', user.last_name)
                user.save()

            social_account, social_created = SocialAccount.objects.get_or_create(
                user=user,
                provider='google',
                defaults={
                    'uid': idinfo['sub'],
                    'extra_data': idinfo,
                }
            )

            if not social_created:
                social_account.extra_data = idinfo
                social_account.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_identifiant':str(user.id)
            }, status=200)
        except ValueError:
            return Response({'error': 'Token Google invalide'}, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email").rstrip()
        password = request.data.get("password")
        email_backend = AuthenticationUser()
        user = email_backend.authenticate(username=email, password=password)
        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_identifiant':str(user.id)
            },status=200)
        elif user is not None and user.is_active==False: 
            confirmation_code=AuthenticationUser.generate_confirmation_code()

            #stocker le code 
            user_code=ConfirmationCode(
                    user=user,
                    code=confirmation_code
                )
            user_code.save()

            AuthenticationUser.activateEmail(request, user, email,confirmation_code)
            return Response({"message": "Votre compte est désactivé","status":422}, status=422)
        else:
            return Response({"error": "L'adresse e-mail ou le mot de passe sont incorrects"}, status=401)
        
class AuthenticationUser(ModelBackend):
    """
    Authenticate against the email field.
    """

    def authenticate(self, username, password, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        


    def register(request):
        if request.method == 'POST':
            print(request.POST)
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False  # Désactive l'utilisateur jusqu'à confirmation
                user.save()
                #generate code confirmation
                confirmation_code=AuthenticationUser.generate_confirmation_code()

                #stocker le code 
                user_code=ConfirmationCode(
                    user=user,
                    code=confirmation_code
                )
                user_code.save()
                try:
                    AuthenticationUser.activateEmail(request, user, form.cleaned_data.get('email'),confirmation_code)
                    return JsonResponse({"message": "Code de confirmation envoyé"}, status=200)
                except Exception:
                    traceback.print_exc()
                    return JsonResponse({"error": "Problème de connexion"}, status=500)
            else:
                traceback.print_exc()
                return JsonResponse({"error": "Formulaire non valide"}, status=500)
        else :
            return JsonResponse({"error": "Méthode non autorisée"}, status=400)


    def activateEmail(request, user, to_email,code):
        
        mail_subject = '[sehatra.com] Confirmez votre adresse e-mail'
        message = render_to_string('acc_confirm_email.html', {
            'user': user,
            'uid': code,
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

    def activateAccount(request):
        if request.method == 'POST':
            email=request.POST.get('email').rstrip()
            code=request.POST.get('code')
            user__account=User.objects.get(email=email)
            try:
                activation= ConfirmationCode.objects.get(user=user__account,code=code)
                if activation.is_valid :
                    user__account.is_active=True
                    user__account.save()
                    refresh = RefreshToken.for_user(user__account)
                    return JsonResponse({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        },status=200)
                else:
                    return JsonResponse({"error": "Vous avez inseré un code qui a expiré"}, status=400)
            except Exception:
                return JsonResponse({"error": "Code invalide"}, status=404)
        else :
            return JsonResponse({"error": "Méthode non autorisée"}, status=405)



    def generate_confirmation_code():
        """
        Génère un code de confirmation à 6 chiffres.
        
        Returns:
        str: Code de confirmation à 6 chiffres.
        """
        # Liste de caractères numériques
        digits = string.digits
        
        # Génère une chaîne alphanumérique de 6 chiffres
        code = ''.join(random.choice(digits) for _ in range(6))
        
        return code





    