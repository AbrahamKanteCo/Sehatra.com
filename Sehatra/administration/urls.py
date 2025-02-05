import datetime
from . import artiste, interface_administration
from . import data_load
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings



app_name = 'administration'

urlpatterns = [
    #token
    path('enregistrerToken/<str:token>/',interface_administration.enregistrerToken,name="enregistrerToken"), 
    path('logout/<str:token>/',interface_administration.logout,name="logout"), 
    #ajout
    path('artistes/ajouter/', interface_administration.ArtisteCreate.as_view(), name='artiste-create'),
    path('associations/ajouter/', interface_administration.AssociationCreate.as_view(), name='association-create'),
    path('lives/ajouter/', interface_administration.LiveCreate.as_view(), name='lives-create'),
    path('videos/ajouter/', interface_administration.VideosCreate.as_view(), name='videos-create'),
    path('organisateurs/ajouter/', interface_administration.OrganisateurCreate.as_view(), name='organisateur-create'),
    path('publications/ajouter/', interface_administration.PublicationCreate.as_view(), name='publications-create'),
    #update
    path('artistes/<int:pk>/update/', interface_administration.ArtisteUpdateView.as_view(), name='artiste-update'),
    path('videos/<int:pk>/update/', interface_administration.VideosUpdateView.as_view(), name='videos-update'),
    path('lives/<int:pk>/update/', interface_administration.LiveUpdateView.as_view(), name='live-update'),
    path('associations/<int:pk>/update/', interface_administration.AssociationUpdateView.as_view(), name='association-update'),
    path('organisateurs/<int:pk>/update/', interface_administration.OrganisateurUpdateView.as_view(), name='organisateur-update'),
    #detail
    path('artistes/<int:pk>/detail/', interface_administration.ArtisteUpdateView.as_view(), name='artiste-detail'),
    path('videos/<int:pk>/detail/', interface_administration.VideosUpdateView.as_view(), name='videos-detail'),
    path('lives/<int:pk>/detail/', interface_administration.LiveUpdateView.as_view(), name='live-detail'),
    path('associations/<int:pk>/detail/', interface_administration.AssociationUpdateView.as_view(), name='association-detail'),
    path('organisateurs/<int:pk>/detail/', interface_administration.OrganisateurUpdateView.as_view(), name='organisateur-detail'),
    #delete
    path('artistes/<int:pk>/delete/', interface_administration.ArtisteUpdateView.as_view(), name='artiste-delete'),
    path('associations/<int:pk>/delete/', interface_administration.AssociationUpdateView.as_view(), name='association-delete'),
    path('organisateurs/<int:pk>/delete/', interface_administration.OrganisateurUpdateView.as_view(), name='organisateur-delete'),
    path('videos/<int:pk>/delete/', interface_administration.VideosUpdateView.as_view(), name='videos-delete'),
    path('lives/<int:pk>/delete/', interface_administration.LiveUpdateView.as_view(), name='lives-delete'),
    #liste
    path('listeartiste', interface_administration.listeartiste, name='artiste-list'),
    path('listelive', interface_administration.listelive, name='live-list'),
    path('listevideos', interface_administration.listevideos, name='video-list'),
    path('listeorganisateurs', interface_administration.listeorganisteurs, name='organisateurs-list'),
    path('associations', interface_administration.associations, name='associations'),
    #recherche
    path('artiste/recherche', interface_administration.rechercheartiste, name='recherche-artiste'),
    path('live/recherche', interface_administration.recherchelive, name='recherche-live'),
    path('video/recherche', interface_administration.recherchevideos, name='recherche-videos'),
    path('video-artiste/recherche', artiste.rechercheartistevideo, name='recherche-videos-artiste'),
    path('association/recherche', interface_administration.rechercheassociations, name='recherche-association'),
    path('organisateur/recherche', interface_administration.searchorganisateur, name='recherche-organisateur'),
    path('detailorganisateur/', interface_administration.detailsorganisateur, name='detailorganisateur'),
    #sehatra.com
    path('', interface_administration.DashboardView.as_view(), name='dashboard'),
    path('switch/<str:user>/', interface_administration.switchUser, name='switch'),
    path('dashboard', interface_administration.dashboard, name='dashboard'),
    path('artistes', interface_administration.artistes, name='artistes'),
    path('facebook', interface_administration.facebook, name='facebook'),
    path('audiences', interface_administration.audiences, name='audiences'),
    path('compteutilisateur', interface_administration.compteutilisateur, name='compteutilisateur'),
    path('transactions', interface_administration.transactions, name='transactions'),
    path('ventes_video', interface_administration.ventes_video, name='ventes_video'),
    path('pages', interface_administration.pages, name='pages'),
    #graph
    path('earning-revenue/<int:annee>',interface_administration.statistiques_ventes_json,name='earning-revenue'),
    #notification
    path('last_notification',interface_administration.listernotification,name='last_notification'),
    #sample_data
    path('audience_pays',interface_administration.get_sample_data,name='audience_pays'),
    path('ventes_pays',interface_administration.ventes_data_pays,name='ventes_pays'),
    path('ventes_data',interface_administration.ventes_data,name='ventes_data'),
    path('audience_age_sexe',interface_administration.get_age_sexe,name='audience_age_sexe'),
    path('audience_langue',interface_administration.get_langue,name='audience_langue'),
    path('audience_sources',interface_administration.get_sources,name='audience_sources'),

    #dashboard load data
    path('dashboard_load_data',data_load.dashboard_data,name='dashboard_load_data'),
    path('audiences_admin_data',data_load.audiences_admin_data,name='audiences_admin_data'),
    path('dashboard_load_artiste',data_load.dashboard_load_artiste,name='dashboard_load_artiste'),
    path('video_statistique_load/<int:video>',data_load.video_statistique_load,name='video_statistique_load'),

    #notification
    path('notifications',interface_administration.notifications,name='notifications'),
    #artiste
    path('dashboard-artiste', artiste.dashboardartiste, name='dashboard-artiste'),
    path('artiste-video', artiste.artistevideo, name='artiste-video'),
    path('statistique-video-artiste/<int:video>', artiste.statistiquevideoartiste, name='statistique-video-artiste'),
    path('pages_artiste', artiste.pages_artistes, name='pages_artiste'),
    path('ventes_video_artiste', artiste.ventes_video_artiste, name='ventes_video_artiste'),
    path('transactions-artiste',artiste.transactions_artistes,name='transactions-artiste'),
    path('earning-revenue-artiste/<int:annee>',artiste.statistiques_ventes_artiste_json,name='earning-revenue-artiste'),
    path('stats_vue_users',artiste.statistiques_vues_nouveaux_utilisateurs_json,name='stats_vue_users'),
    #publication
    path('publications',interface_administration.publications,name='publications'),

    #tâche à executer
    path('recupererDataAnalytics',interface_administration.recupererData,name='recupererDataAnalytics'),# tous les jours à minuit
    path('envoiNotificationAdmin',interface_administration.envoi_notification_administrateur,name='envoiNotificationAdmin'),#tous les jours à 8
    path('envoiNotificationOrganisateur',artiste.envoi_notification_artiste,name='envoiNotificationOrganisateur'),# tous les jours à 16 heures

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)