from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from .views import HomeView, VideoDetailView, TestView, check_user, VenteBilletConcertView, paiement, \
    paiement_cancel, paiement_notif, paiement_success, ConcertView, AproposView, PolitiqueDeConfidentialiteView, CGUView, suppr_user, SupprimerUrl, FormulaireCreateProView, ConcertTestView, VideoView
from .sitemap import ConcertSitemap, VideoSitemap, StaticViewSitemap
from django.contrib.sitemaps.views import sitemap


sitemap_static = {
    'static': StaticViewSitemap
}

sitemap_concert = {
    'concert': ConcertSitemap
}

sitemap_video = {
    'video': VideoSitemap
}


urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('videos/', VideoView.as_view(), name="video"),
    path('a-propos/', AproposView.as_view(), name="a-propos"),
    path('supprimer-compte-utilisateur', SupprimerUrl.as_view(), name="supprimer"),
    path('supprimer-compte/', suppr_user, name="a-propos"),
    path('politique-de-confidentialite/', PolitiqueDeConfidentialiteView.as_view(), name="politique"),
    path('condition-d-utilisation/', CGUView.as_view(), name="cgu"),
    path('video/<slug:slug>', VideoDetailView.as_view(), name="video"),
    path('test/', login_required(TestView.as_view()), name="test"),
    path('formulaire-reclamation', login_required(FormulaireCreateProView.as_view()), name="formulaire-reclamation"),
    path('check-user/', check_user, name="check"),
    path('concert/<slug:slug>/', VenteBilletConcertView.as_view(), name="concert"),
    path('concert/<slug:slug>/<slug:billet>/', ConcertView.as_view(), name="concert-video"),
    path('concert-test/<slug:slug>/<slug:billet>/', ConcertTestView.as_view(), name="concert-test-video"),
    path('concert/<slug:slug>/billet/achat/<slug:mode>', paiement, name="paiement"),
    path('concert/<slug:slug>/billet/<slug:billet>/success', paiement_success, name="paiement-success"),
    path('concert/<slug:slug>/billet/<slug:billet>/notif', paiement_notif, name="paiement-notif"),
    path('concert/<slug:slug>/billet/<slug:billet>/cancel', paiement_cancel, name="paiement-cancel"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemap_static}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap-video.xml', sitemap, {'sitemaps': sitemap_video}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap-concert.xml', sitemap, {'sitemaps': sitemap_concert}, name='django.contrib.sitemaps.views.sitemap')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
