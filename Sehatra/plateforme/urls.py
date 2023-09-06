from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from .views import *
from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    path('', HomeView.as_view(), name="accueil"),
    path('politique-de-confidentialite/', PolitiqueDeConfidentialiteView.as_view(), name="privacy-policy"),
    path('cgu/', CGUView.as_view(), name="cgu"),
    path('tamberina-an-kira-06-aout/', login_required(TestView.as_view()), name="test"),
    path('administration/',AdministrationView.as_view(), name="admin"),
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
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
