import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from paiement.models import Paiement,Billet
from plateforme.models import Video
from .facebook.facebookdata import AudienceParAgeEtSexe, AudienceParSexe, pageInformationData
from .google_analytics.analytics import SourceDesClics, demographicsByLanguage, demographieParPays, getUtilisateurActive
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models.functions import Coalesce

from .models import  PageAnalytics,VenteParPays, Video_facebook

from django.db.models import Q,Count,Sum



def dashboard_data (request): 
    date_debut=datetime.datetime.strptime(request.GET.get('debut'), "%Y-%m-%d")
    date_fin=datetime.datetime.strptime(request.GET.get('fin'), "%Y-%m-%d")
    difference_en_jours = (date_fin - date_debut).days
    last_month=(date_debut-datetime.timedelta(days=difference_en_jours)).strftime('%Y-%m-%d')

    #compte créé

    debut_journee = datetime.datetime.combine(date_debut, datetime.datetime.min.time())

    fin_journee = datetime.datetime.combine(date_fin, datetime.datetime.max.time())

    utilisateurs_crees = User.objects.filter(date_joined__range=(debut_journee, fin_journee))

    nombre_utilisateurs_crees = utilisateurs_crees.count()

    compte_html="<p class='mb-1'>Comptes crées</p><h2 class='mb-0 font-weight-bold'>"+str(nombre_utilisateurs_crees)+"</h2>"

    #chiffre_affaire
    ca_aujourdhui = Paiement.objects.filter(valide=True,billet__gratuit=False,date__range=(date_debut,date_fin))
    chiffre_affaire=Paiement.calculer_paiement(ca_aujourdhui)

    ca_html="<p class='mb-1'>CA </p><h2 class='mb-0 font-weight-bold'>"+str(intcomma(chiffre_affaire))+" Ar</h2>"

    #revenus
    paiements = Paiement.objects.filter(valide=True,billet__gratuit=False,date__range=(date_debut,date_fin)).order_by("-date")
    somme=Paiement.calculer_paiement(paiements)
    revenus = somme *40 / 100
    #revenus last_month
    paiements_last_month = Paiement.objects.filter(valide=True,billet__gratuit=False,date__range=(last_month,date_debut)).order_by("-date")
    revenus_last_month=(Paiement.calculer_paiement(paiements_last_month))*40/100
    difference_revenus=revenus-revenus_last_month

    if revenus_last_month > 0:
        revenus_difference_en_pourcentage = (difference_revenus / revenus_last_month) * 100
    else:
        revenus_difference_en_pourcentage = 0

    
    revenus_html="<p class='mb-1'>Revenue</p><h2 class='mb-1 font-weight-bold'>"+str(intcomma(revenus))+" Ar</h2>"
    if difference_revenus > 0:
        revenus_html+="<span class='mb-1 text-muted'><span class='text-success'><i class='fa fa-caret-up  me-1'></i>"+str(intcomma(difference_revenus))+" </span></span>"
    else:
        revenus_html+="<span class='mb-1 text-muted'><span class='text-danger'><i class='fa fa-caret-down  me-1'></i> "+str(intcomma(difference_revenus*(-1)))+"</span></span>"
    

    revenus_html+="<div class='progress progress-sm mt-3 bg-success-transparent'><div class='progress-bar progress-bar-striped progress-bar-animated bg-success' style='width: "+str(revenus_difference_en_pourcentage)+"%'></div></div>"

    #dépense
    
    depense=somme-revenus
    depense_html=" <p class='mb-1'>Dépenses </p><h2 class='mb-0 font-weight-bold'>"+str(intcomma(depense))+" Ar</h2>"


    #pages
    pages = (
        PageAnalytics.objects.filter(date__range=(date_debut,date_fin))
        .values("path", "screenname")
        .annotate(total_vue=Coalesce(Sum("vue"), 0))
        .order_by("-total_vue")[:20]
    )
    pages_html=""
    for page in pages:
        pages_html+=" <tr><td class='font-weight-bold'>"+str(page['screenname'])+"</td><td>"+str(page['path'])+"</td><td>"+str(page['total_vue'])+"</td></tr>"


    #oeuvre vendu
    oeuvre_vendu= len(paiements)
    oeuvre_vendu_last_month=len(paiements_last_month)
    oeuvre_difference=oeuvre_vendu-oeuvre_vendu_last_month

    if oeuvre_vendu_last_month > 0:
        oeuvre_difference_en_pourcentage = (oeuvre_difference / oeuvre_vendu_last_month) * 100
    else:
        oeuvre_difference_en_pourcentage = 0

    oeuvre_html="<p class='mb-1'>Oeuvres vendues </p><h2 class='mb-1 font-weight-bold'>"+str(oeuvre_vendu)+"</h2>"
    if oeuvre_difference > 0:
        oeuvre_html+="<span class='mb-1 text-muted'><span class='text-success'><i class='fa fa-caret-up  me-1'></i>"+str(oeuvre_difference)+" </span></span>"
    else:
        oeuvre_html+="<span class='mb-1 text-muted'><span class='text-danger'><i class='fa fa-caret-down  me-1'></i> "+str(oeuvre_difference*(-1))+"</span></span>"

    

    oeuvre_html+="<div class='progress progress-sm mt-3 bg-success-transparent'><div class='progress-bar progress-bar-striped progress-bar-animated bg-success' style='width: "+str(oeuvre_difference_en_pourcentage)+"%'></div></div>"


    #ventes par pays
    ventes_valides = VenteParPays.objects.filter(
    Q(slug__in=Billet.objects.filter(valide=True).values_list('slug', flat=True)) &
    Q(slug__in=Paiement.objects.filter(valide=True).values_list('billet__slug', flat=True)),date_vente__range=(date_debut,date_fin))
    ventes_groupees = ventes_valides.values('pays').annotate(nombre_ventes=Count('id'))
    vente_html=""
    if len(ventes_groupees)>0:
        for ventes_groupee in ventes_groupees:
            vente_html+="<tr><td class='w-1 text-center ps-5'><i class='flag flag-"+str(ventes_groupee['codepays'])+"'></i></td><td>"+str(ventes_groupee['pays'])+"</td><td class='text-end'><span class='font-weight-bold'>"+str(ventes_groupee['nombre_ventes'])+" ventes </span></td></tr>"
    else :
        vente_html+="<tr><td colspan='3'>Aucune vente durant cette période.</td></tr>"

    #utilisateurs actifs
    utilisateurs=getUtilisateurActive(date_debut.strftime('%Y-%m-%d'),date_fin.strftime('%Y-%m-%d'))
    utilisateurs_last_month=getUtilisateurActive(last_month,date_debut.strftime('%Y-%m-%d'))
    utilisateurs_difference=utilisateurs-utilisateurs_last_month

    if utilisateurs_last_month > 0:
        utilisateurs_difference_en_pourcentage = (utilisateurs / utilisateurs_last_month) * 100
    else:
        utilisateurs_difference_en_pourcentage = 0
    

    utilisateurs_html="<p class='mb-1'>Utilisateurs actifs </p><h2 class='mb-1 font-weight-bold'>"+str(utilisateurs)+"</h2>"
    if utilisateurs_difference > 0:
        utilisateurs_html+="<span class='mb-1 text-muted'><span class='text-success'><i class='fa fa-caret-up  me-1'></i>"+str(format(utilisateurs_difference_en_pourcentage,'.2f'))+" %</span></span>"
    else:
        utilisateurs_html+="<span class='mb-1 text-muted'><span class='text-danger'><i class='fa fa-caret-down  me-1'></i> "+str(format(utilisateurs_difference_en_pourcentage*(-1),'.2f'))+" %</span></span>"

    utilisateurs_html+="<div class='progress progress-sm mt-3 bg-success-transparent'><div class='progress-bar progress-bar-striped progress-bar-animated bg-success' style='width: "+str(utilisateurs_difference_en_pourcentage)+"%'></div></div>"

    return JsonResponse({'utilisateurs':utilisateurs_html,'compte':compte_html,'chiffre_affaire':ca_html,'depense':depense_html,'revenue':revenus_html,'oeuvre':oeuvre_html,'ventes':vente_html,'pages':pages_html})

    
def audiences_admin_data(request):
    # datetime.strptime(date_str, "%Y-%m-%d")
    date_debut=datetime.datetime.strptime(request.GET.get('debut'), "%Y-%m-%d")
    date_fin=datetime.datetime.strptime(request.GET.get('fin'), "%Y-%m-%d")

    sexe=AudienceParSexe(date_debut.strftime('%Y-%m-%d'),date_fin.strftime('%Y-%m-%d'))
    countries=demographieParPays(date_debut.strftime('%Y-%m-%d'),date_fin.strftime('%Y-%m-%d'))
    agesexe=AudienceParAgeEtSexe(date_debut.strftime('%Y-%m-%d'),date_fin.strftime('%Y-%m-%d'))
    langues=demographicsByLanguage(date_debut.strftime('%Y-%m-%d'),date_fin.strftime('%Y-%m-%d'))
    sources=SourceDesClics(date_debut.strftime('%Y-%m-%d'),date_fin.strftime('%Y-%m-%d'))

    homme_html="<div class='col mb-lg-4 mb-xl-0'> <div class='mb-2 fs-18 text-muted'>Homme</div> <h1 class='font-weight-bold mb-1'>"+str(sexe['nb_masculin'])+"</h1> </div> <div class='col col-auto'><div class='mx-auto chart-circle chart-circle-md chart-circle-primary mt-sm-0 mb-0' id='chart-circle-primary' data-value='"+sexe['m']+"' data-thickness='12' data-color=''><div class='mx-auto chart-circle-value text-center fs-20'>"+str("{:.2f}".format(sexe['masculin']))+"%</div></div></div>"
    femme_html="<div class='col mb-lg-4 mb-xl-0'><div class='mb-2 fs-18 text-muted'>Femme</div><h1 class='font-weight-bold mb-1'>"+str(sexe['nb_feminin'])+"</h1></div><div class='col col-auto'><div class='mx-auto chart-circle chart-circle-md chart-circle-success mt-sm-0 mb-0'  data-value='"+str(sexe['f'])+"' data-thickness='12' data-color=''><div class='mx-auto chart-circle-value text-center fs-20'>"+str("{:.2f}".format(sexe['feminin']))+"</div></div></div>"
    autre_html="<div class='col mb-lg-4 mb-xl-0'><div class='mb-2 fs-18 text-muted'>Non défini</div><h1 class='font-weight-bold mb-1'>"+str(sexe['nb_autre'])+"</h1></div><div class='col col-auto'><div class='mx-auto chart-circle chart-circle-md chart-circle-warning mt-sm-0 mb-0'  data-value='"+str(sexe['u'])+"' data-thickness='12' data-color=''><div class='mx-auto chart-circle-value text-center fs-20'>"+str("{:.2f}".format(sexe['autre']))+"</div></div></div>"

    countries_html="<table class='table table-hover mb-0'><tbody><tr><td></td><td>Pays</td><td>Utilisateurs</td><td>Nouveaux utilisateurs</td></tr>"
    for country in countries.values:
        countries_html+="<tr class='border-bottom'><td></td><td class='p-3 d-flex'> "+str(country[0])+"</td><td class='p-3'> "+str(country[1])+"</td><td class='p-3'>"+str(country[2])+"</td></tr>"
    countries_html+="</tbody></table>"

    langues_html="<table class='table table-hover mb-0'><tbody><tr><td></td><td>Langue</td><td>Utilisateurs</td><td>Nouveaux utilisateurs</td></tr>"
    for langue in langues.values:
        langues_html+="<tr class='border-bottom'><td></td><td class='p-3 d-flex'> "+str(langue[0])+"</td><td class='p-3'> "+str(langue[1])+"</td><td class='p-3'>"+str(langue[2])+"</td></tr>"
    langues_html+="</tbody></table>"

    sources_html="<table class='table table-hover mb-0'><tbody><tr><td></td><td>Source des clicks</td><td>Utilisateurs</td></tr>"
    for source in sources.values:
        sources_html+="<tr class='border-bottom'><td></td><td class='p-3 d-flex'> "+str(source[0])+"</td><td class='p-3'> "+str(source[1])+"</td></tr>"

    agesexe_html="<table class='table table-hover mb-0'><tbody><tr><td></td><td>Age/Sexe</td><td>Utilisateurs</td></tr>"

    for age_group, count in agesexe.items():
        agesexe_html+="<tr class='border-bottom'><td></td><td class='p-3 d-flex'> "+str(age_group)+"</td><td class='p-3'> "+str(count)+"</td></tr>"
    agesexe_html+="</tbody></table>"

    
    return JsonResponse({'homme':homme_html,'femme':femme_html,'autre': autre_html,'countries':countries_html,'agesexe':agesexe_html,'langues':langues_html,'sources':sources_html})

def dashboard_load_artiste (request): 
    artiste_id = 2
    date_debut=datetime.datetime.strptime(request.GET.get('debut'), "%Y-%m-%d")
    date_fin=datetime.datetime.strptime(request.GET.get('fin'), "%Y-%m-%d")
    last_month=(date_debut-datetime.timedelta(days=28)).strftime('%Y-%m-%d')
  

    #revenue
    paiements = Paiement.objects.filter(valide=True,billet__gratuit=False,date__range=(date_debut,date_fin),billet__video__artiste__user=artiste_id).order_by("-date")
    somme=Paiement.calculer_paiement(paiements)
    revenus = somme * 60 / 100

    #revenu last month
    paiements_last_month = Paiement.objects.filter(valide=True,billet__gratuit=False,date__range=(last_month,date_debut),billet__video__artiste__user=artiste_id).order_by("-date")
    revenus_last_month=(Paiement.calculer_paiement(paiements_last_month))* 60 / 100
    revenus_difference=revenus-revenus_last_month

    revenus_html="<h2 class='mb-1 fs-40 font-weight-bold'>"+str(intcomma(revenus))+" Ar</h2>"
    if revenus_difference > 0 :
        revenus_html+="<small class='mb-1 text-muted'><small class='text-success'><i class='fa fa-caret-up  me-1'></i>"+str(intcomma(revenus))+"</small> vs "+str(intcomma(revenus_last_month))+" le mois dernier</small>"   
    elif revenus_difference < 0 :
        revenus_html+= "<small class='mb-1 text-muted'><small class='text-danger'><i class='fa fa-caret-down  me-1'></i>"+str(intcomma(revenus))+"</small> vs "+str(intcomma(revenus_last_month))+" le mois dernier</small>" 
    else:
        revenus_html+= "<small class='mb-1 text-muted'>Aucun évolution</small>"                              

    #vente
    ventes=len(paiements)
    ventes_last_month=len(paiements_last_month)
    ventes_difference=ventes-ventes_last_month

    ventes_html="<h2 class='mb-1 fs-40 font-weight-bold'>"+str(ventes)+" </h2>"
    if ventes_difference > 0 :
        ventes_html+="<small class='mb-1 text-muted'><small class='text-success'><i class='fa fa-caret-up  me-1'></i>"+str(ventes)+"</small> vs "+str(ventes_last_month)+" le mois dernier</small>"   
    elif ventes_difference < 0 :
        ventes_html+= "<small class='mb-1 text-muted'><small class='text-danger'><i class='fa fa-caret-down  me-1'></i>"+str(ventes)+"</small> vs "+str(ventes_last_month)+" le mois dernier</small>" 
    else:
        ventes_html+= "<small class='mb-1 text-muted'>Aucun évolution</small>"

    #nombre de contenues
    videos=Video.objects.filter(artiste__user=2)
    contenus=len(videos)

    #nombre de contenues le mois dernier
    videos_last_month=Video.objects.filter(artiste__user=2,date_sortie__range=(last_month,date_debut))
    contenus_last_month=len(videos_last_month)
    contenus_difference=contenus-contenus_last_month


    contenus_html="<h2 class='mb-1 fs-40 font-weight-bold'>"+str(contenus)+" </h2>"
    if contenus_difference > 0 :
        contenus_html+="<small class='mb-1 text-muted'><small class='text-success'><i class='fa fa-caret-up  me-1'></i>"+str(contenus)+"</small> vs "+str(contenus_last_month)+" le mois dernier</small>"   
    elif contenus_difference < 0 :
        contenus_html+= "<small class='mb-1 text-muted'><small class='text-success'><i class='fa fa-caret-down  me-1'></i>"+str(contenus)+"</small> vs "+str(contenus_last_month)+" le mois dernier</small>" 
    else:
        contenus_html+= "<small class='mb-1 text-muted'>Aucun évolution</small>"

    #publications
    publications=Video_facebook.objects.filter(video__artiste__user=2,date_publication__range=(date_debut,date_fin))
    pub=len(publications)

    #publication le mois dernier

    publications_last_month=Video_facebook.objects.filter(video__artiste__user=2,date_publication__range=(last_month,date_debut))
    pub_last_month=len(publications_last_month)
    pub_difference=pub-pub_last_month

    pub_html="<h2 class='mb-1 fs-40 font-weight-bold'>"+str(pub)+"</h2>"
    if pub_difference > 0 :
        pub_html+="<small class='mb-1 text-muted'><small class='text-success'><i class='fa fa-caret-up  me-1'></i>"+str(pub)+"</small> vs "+str(pub_last_month)+" le mois dernier</small>"   
    elif pub < 0 :
        pub_html+= "<small class='mb-1 text-muted'><small class='text-danger'><i class='fa fa-caret-down  me-1'></i>"+str(pub_difference)+"</small> vs "+str(pub_last_month)+" le mois dernier</small>" 
    else:
        pub_html+= "<small class='mb-1 text-muted'>Aucun évolution</small>"


    # Récupérez les ventes valides pour cet artiste
    ventes_valides = VenteParPays.objects.filter(
        Q(slug__in=Billet.objects.filter(valide=True, user_id=artiste_id).values_list('slug', flat=True)) &
        Q(slug__in=Paiement.objects.filter(valide=True).values_list('billet__slug', flat=True)),
        date_vente__range=(date_debut,date_fin))

    # Groupez les ventes par pays et comptez le nombre de ventes
    ventes_groupees = ventes_valides.values('pays').annotate(nombre_ventes=Count('id'))

    ventes_pays_html="<table class='table card-table text-nowrap'><tbody>"
    if len(ventes_groupees):
        for vente_groupe in ventes_groupees:
            ventes_pays_html+="<tr><td class='w-1'><i class='flag flag-"+str(vente_groupe['codepays'])+"'></i></td><td>"+str(vente_groupe['pays'])+"</td><td class='w-3 text-end'><span class=''>"+str(vente_groupe['nombre_ventes'])+"</span></td></tr>"
        ventes_pays_html+="</tbody></table>"
    else:
        ventes_pays_html+="<tr><td colspan='3'>Aucune vente durant cette période.</td></tr>"

    videos = Video.objects.filter(artiste__user=2)

    resultats = []

    for video in videos:
            slug_video = video.slug

            total_vues = (
                PageAnalytics.objects.filter(
                    path__icontains=slug_video, date__range=(date_debut,date_fin)
                ).aggregate(total_vues=Sum("vue"))["total_vues"]
                or 0
            )
            nb_ventes = Paiement.objects.filter(
                valide=True,
                billet__gratuit=False,
                date__range=(date_debut,date_fin),
                billet__video_id=video.id,
            ).order_by("-date")
            resultats.append(
                {"titre": video.titre, "total_vues": total_vues, "ventes": len(nb_ventes)}
            )

    pages_html=""
    if len(resultats)>0:
        for page in resultats:
            pages_html+=" <tr><td class='font-weight-bold'>"+str(page['titre'])+"</td><td>"+str(page['total_vues'])+"</td><td>"+str(page['ventes'])+"</td></tr>"
    else:
        pages_html="<p class='text center'>Aucune donnée</p>"


    return JsonResponse({'revenue':revenus_html,'contenue':contenus_html,'ventes': ventes_html,'ventes_pays':ventes_pays_html,'pub':pub_html,"pages":pages_html})


def video_statistique_load(request,video):
    date_debut=datetime.datetime.strptime(request.GET.get('debut'), "%Y-%m-%d")
    date_fin=datetime.datetime.strptime(request.GET.get('fin'), "%Y-%m-%d")
    videos=Video.objects.filter(id=video).first()
    #revenus
    paiements=Paiement.objects.filter(valide=True,billet__gratuit=False,date__range=(date_debut,date_fin),billet__video__id=video).order_by("-date")
    somme=Paiement.calculer_paiement(paiements)
    revenus = somme *60 / 100

    revenue_html="<h1 class='font-weight-bold mb-1'>"+str(intcomma(revenus))+" Ar</h1>"

    ventes_html="<h1 class='font-weight-bold mb-1'>"+str(len(paiements))+"</h1>"

    #publication lié
    publications=Video_facebook.objects.filter(video=videos.id)

    publication_html=""
    for publication in publications:
        publication_html+="<div class='col-md-6'><iframe src='"+publication.facebook+"' width='500' height='712' style='border:none;overflow:hidden' scrolling='no' frameborder='0' allowfullscreen='true' allow='autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share'></iframe></div>"

    #nombre de vue
    total_vues = PageAnalytics.objects.filter(path__icontains=videos.slug,date__range=(date_debut,date_fin)).aggregate(total_vues=Sum('vue'))['total_vues'] or 0


    vues_html="<h1 class='font-weight-bold mb-1'>"+str(total_vues)+"</h1>"


    return JsonResponse({'revenue':revenue_html,'vues':vues_html,'ventes': ventes_html,'publication':publication_html})
   

