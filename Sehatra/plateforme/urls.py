from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

from plateforme.users_mobile import *
from plateforme.authentification import LoginView
from .views import *
from django.contrib.sitemaps.views import sitemap
from .authentification import AuthenticationUser
from .authentification import GoogleLoginView


urlpatterns = [
    path('', HomeView.as_view(), name="accueil"),
    path('politique-de-confidentialite/', PolitiqueDeConfidentialiteView.as_view(), name="privacy-policy"),
    path('cgu/', CGUView.as_view(), name="cgu"),
    path('tamberina-an-kira-06-aout/', login_required(TestView.as_view()), name="test"),
    path('administration1/',AdministrationView.as_view(), name="admin"),
    path('mes-videos/', login_required(MesVideosView.as_view()), name="mes-videos-view"),
    path('profil/', login_required(ProfilView.as_view()), name="profil-view"),
    path('profil/creer/', login_required(ProfilCreateView.as_view()), name="profil-create"),
    path('profil/<pk>/editer/', login_required(ProfilUpdateView.as_view()), name="profil-update"),
    path('action/', ActionListView.as_view(), name="action"),
    path('action/<slug:slug>/', ActionDetailView.as_view(), name="action-detail"),
    path('artiste/', ArtisteListView.as_view(), name="artiste"),
    path('artiste/<slug:slug>/', ArtisteDetailView.as_view(), name="artiste-detail"),
    path('association/', AssociationListView.as_view(), name="association"),
    path('association/<slug:slug>/', AssociationDetailView.as_view(), name="association-detail"),
    path('organisateur/', OrganisateurListView.as_view(), name="organisateur"),
    path('organisateur/<slug:slug>/', OrganisateurDetailView.as_view(), name="organisateur-detail"),
    path('video/', VideoListView.as_view(), name="video"),
    path('video/<slug:slug>/', VideoDetailView.as_view(), name="video-detail"),
    path('video/<slug:slug>/regarder/', login_required(VideoPlayerView.as_view()), name="video-player"),
    path('video/<slug:slug>/regarder-test/', login_required(VideoPlayerTestView.as_view()), name="video-player-test"),
    path('video/<slug:video>/billet/', login_required(billet_create), name="achat-billet"),
    path("csrf/", HomeView.csrf, name="create_csrf"),
    path('register/', AuthenticationUser.register, name='register'),
    path('forgot_password/', AuthenticationUser.forgot_password, name='forgot_password'),
    path('reinitialize_password/', AuthenticationUser.reinitialize_password, name='reinitialize_password'),
    path('confirm_codeinitialization/',AuthenticationUser.confirm_CodeInitialization,name='confirm_codeinitialization'),
    path('registerbysocialaccount/', GoogleLoginView.as_view(), name='registerbysocialaccount'),
    path('user_information/', get_user_info, name='user_information'),
    path('concert_live/',get_list_concert_live,name='concert_live'),
    path('list_film/',get_list_film,name='list_film'),
    path('list_live/',get_list_live,name='list_live'),
    path('live_a_la_une/',get_live_a_la_une,name='live_a_la_une'),
    path('liste_artiste/',getArtiste,name='liste_artiste'),
    path('liste_organisateur/',getOrganisateur,name='liste_organisateur'),
    path('liste_association/',getAssociation,name='liste_association'),
    path('mes_video_films/',getMesVideosFilm,name='mes_video_films'),
    path('mes_video_concert/',getMesVideosConcert,name='mes_video_concert'),
    path('login/', LoginView.as_view(), name='login'),
    path('confirmationcode/', AuthenticationUser.activateAccount, name='confirmationcode'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
