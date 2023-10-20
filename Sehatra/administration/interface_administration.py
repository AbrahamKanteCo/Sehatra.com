import datetime
import locale
import socket
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.humanize.templatetags.humanize import intcomma

from .facebook.facebookdata import (
    AudienceParAgeEtSexe,
    AudienceParSexe,
    contenu_recent,
    page_vue_ensemble,
    pageInformationData,
)
from .google_analytics.analytics import (
    SourceDesClics,
    dataVenteParPays,
    demographicsByLanguage,
    demographieParPays,
    getUtilisateurActive,
    pageStatistique,
)
from .models import (
    NotificationFCM,
    PageAnalytics,
    VenteParPays,
    Video_facebook,
)
from plateforme.models import Association,Action, Live, Organisateur, Artiste, Video
from paiement.models import  Billet,Paiement


from .serializers import (
    ArtisteSerializer,
    AssociationSerializer,
    LiveSerializer,
    OrganisteurSerializer,
    VideoSerializer,
)
from django.db.models import Q,Avg
from rest_framework import generics
from .serializers import ArtisteSerializer
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Case, When, F, IntegerField
from django.db.models.functions import Coalesce
from django.db.models.functions import TruncMonth
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from django.http import JsonResponse
import firebase_admin

country_mapping = {
    "Madagascar": "mg",
    "France": "fr",
    "Mauritius": "mu",
    "United States": "us",
    "Germany": "de",
    "Canada": "ca",
    "China": "cn",
    "Kuwait": "kw",
    "Réunion": "re",
    "Brazil": "br",
    "Netherlands": "nl",
    "Belgium": "be",
    "Indonesia": "id",
    "Italy": "it",
    "Saudi Arabia": "sa",
    "Switzerland": "ch",
    "Sweden": "se",
    "United Kingdom": "gb",
    "Jordan": "jo",
    "Iraq": "iq",
    "Ireland": "ie",
    "Congo - Kinshasa": "cd",
    "India": "in",
    "Morocco": "ma",
    "United Arab Emirates": "ae",
    "Algeria": "dz",
    "Austria": "at",
    "Burkina Faso": "bf",
    "Cameroon": "cm",
    "Comoros": "km",
    "Rwanda": "rw",
    "Sri Lanka": "lk",
    "Taiwan": "tw",
    "Czechia": "cz",
    "Côte d’Ivoire": "ci",
    "Equatorial Guinea": "gq",
    "Guinea": "gn",
    "Hungary": "hu",
    "Kenya": "ke",
    "Lebanon": "lb",
    "Lithuania": "lt",
    "Malawi": "mw",
    "Malaysia": "my",
    "Mali": "ml",
    "New Caledonia": "nc",
    "New Zealand": "nz",
    "Norway": "no",
    "Paraguay": "py",
    "Seychelles": "sc",
    "South Africa": "za",
    "South Korea": "kr",
    "Spain": "es",
    "Romania": "ro",
    "Mexico": "mx",
    "Philippines": "ph",
    "Egypt": "eg",
    "Portugal":"pt",
}

pagination = 10
prix_ariary_euro=4700

class DashboardView(View):
    def get(self, request):
        if request.user.is_superuser==True or request.user.is_staff== True:
            return redirect("/administration/dashboard")
        elif request.user.is_artist:
            return redirect("/administration/dashboard-artiste")


def pages(request):
    debut_28 = datetime.datetime.now() - datetime.timedelta(days=28)
    since = debut_28.strftime("%Y-%m-%d")
    pages = (
        PageAnalytics.objects.filter(date__range=(since,datetime.datetime.now() ))
        .values("path", "screenname")
        .annotate(total_vue=Coalesce(Sum("vue"), 0))
        .order_by("-total_vue")
    )
    total_vues = PageAnalytics.objects.filter(date__range=(since,datetime.datetime.now() )).aggregate(Sum('vue'))['vue__sum']

    temps_moyen = PageAnalytics.objects.filter(date__range=(since,datetime.datetime.now() )).aggregate(Avg('temps_moyenne'))['temps_moyenne__avg']

    total_nouveaux_utilisateurs = PageAnalytics.objects.filter(date__range=(since,datetime.datetime.now() )).aggregate(Sum('nouveauutilisateur'))['nouveauutilisateur__sum']

    taux_rebond_moyen = PageAnalytics.objects.filter(date__range=(since,datetime.datetime.now() )).aggregate(Avg('bouncerate'))['bouncerate__avg']

    notifications = NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[:5]
    context = {"pages": pages, "notifications": notifications,"total_vue":total_vues if total_vues is not None else 0,"temps_moyen":format(temps_moyen,'.2f') if temps_moyen is not None else 0.0,"total_nouveaux_utilisateurs":total_nouveaux_utilisateurs if total_nouveaux_utilisateurs is not None else 0,"taux_rebond_moyen":format(taux_rebond_moyen,'.2f') if taux_rebond_moyen is not None else 0.0}

    return render(request, "pages.html", context)


def ventes_video(request):
    debut_28 = datetime.datetime.now() - datetime.timedelta(days=28)
    since = debut_28.strftime("%Y-%m-%d")
    ventes_par_video = Video.objects.annotate(
        nombre_ventes=Count(
            "video_billet__billet_paiement__id",
            distinct=True,
            filter=Q(
                video_billet__billet_paiement__valide=True,
                video_billet__valide=True,
                video_billet__gratuit=False,
                video_billet__billet_paiement__date__range=(since,datetime.datetime.now()),
            ),
        )
    ).values("titre", "nombre_ventes", "photo_de_couverture", "artiste__nom")
    notifications = NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[:5]
    context = {"ventes_video": ventes_par_video, "notifications": notifications}

    return render(request, "ventes_video.html", context)


def compteutilisateur(request):
    debut_28 = datetime.datetime.now() - datetime.timedelta(days=28)
    since = debut_28.strftime("%Y-%m-%d")
    until = datetime.datetime.now().strftime("%Y-%m-%d")
    last_month = (debut_28 - datetime.timedelta(days=28)).strftime("%Y-%m-%d")
    comptes = User.objects.all().order_by("-date_joined")
    total_mois_dernier = User.objects.filter(
        date_joined__range=(last_month, since)
    ).count()
    notifications = NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[:5]
    total_comptes = comptes.count()
    context = {
        "comptes": comptes,
        "notifications": notifications,
        "total": total_comptes,
        "total_mois_dernier": total_mois_dernier,
    }
    return render(request, "comptes.html", context)


def transactions(request):
    transactions = Paiement.objects.filter(billet__gratuit=False).order_by("-date")
    transactions_valide = Paiement.objects.filter(
        billet__gratuit=False, billet__valide=True, billet__billet_paiement__valide=True
    ).count()
    mvola = Paiement.objects.filter(
        billet__gratuit=False,
        billet__valide=True,
        billet__billet_paiement__valide=True,
        billet__billet_paiement__mode__nom="Mvola",
    ).count()
    orange = Paiement.objects.filter(
        billet__gratuit=False,
        billet__valide=True,
        billet__billet_paiement__valide=True,
        billet__billet_paiement__mode__nom="Orange Money",
    ).count()
    stripe = Paiement.objects.filter(
        billet__gratuit=False,
        billet__valide=True,
        billet__billet_paiement__valide=True,
        billet__billet_paiement__mode__nom="Stripe",
    ).count()
    mvola_echec = Paiement.objects.filter(
        billet__gratuit=False,
        billet__valide=True,
        billet__billet_paiement__valide=True,
        billet__billet_paiement__mode__nom="Mvola",
    ).count()
    orange_echec = Paiement.objects.filter(
        billet__gratuit=False,
        billet__valide=True,
        billet__billet_paiement__valide=True,
        billet__billet_paiement__mode__nom="Orange Money",
    ).count()
    stripe_echec = Paiement.objects.filter(
        billet__gratuit=False,
        billet__valide=False,
        billet__billet_paiement__valide=False,
        billet__billet_paiement__mode__nom="Stripe",
    ).count()

    transactions_echec = Paiement.objects.filter(
        billet__gratuit=False,
        billet__valide=False,
        billet__billet_paiement__valide=False,
    ).count()
    total = transactions.count()
    context = {
        "transactions": transactions,
        "total": total,
        "mvola_valide": mvola,
        "orange_valide": orange,
        "stripe_valide": stripe,
        "mvola_echec": mvola_echec,
        "orange_echec": orange_echec,
        "stripe_echec": stripe_echec,
        "valide": transactions_valide,
        "echec": transactions_echec,
        "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
            :5
        ],
    }
    return render(request, "transactions.html", context)


def notifications(request):
    notifications = NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")
    paginator = Paginator(notifications, pagination)

    page_number = request.GET.get("page")
    listes = paginator.get_page(page_number)
    context = {"notifications": listes}
    return render(request, "notification.html", context)


def listernotification(request):
    notifications = NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[:5]

    notification_list = [
        {
            "title": notification.title,
            "body": notification.content,
            "is_read": notification.is_read,
        }
        for notification in notifications
    ]

    return JsonResponse({"notifications": notification_list})



def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False
    
def dashboard(request):
    marquer_notification_read(request)
    # compte créé
    aujourdhui = datetime.datetime.now().date()

    debut_journee = datetime.datetime.combine(aujourdhui, datetime.datetime.min.time())

    fin_journee = datetime.datetime.combine(aujourdhui, datetime.datetime.max.time())

    utilisateurs_crees_aujourd_hui = User.objects.filter(
        date_joined__range=(debut_journee, fin_journee)
    )

    nombre_utilisateurs_crees = utilisateurs_crees_aujourd_hui.count()

    # compte récent
    periode = datetime.timedelta(days=28)

    date_debut = datetime.datetime.now() - periode

    comptes_recents = User.objects.filter(date_joined__gte=date_debut).order_by(
        "-date_joined"
    )[:5]

    # 28 derniers jours
    debut_28 = datetime.datetime.now() - datetime.timedelta(days=28)
    since = debut_28.strftime("%Y-%m-%d")
    until = datetime.datetime.now().strftime("%Y-%m-%d")
    last_month = (debut_28 - datetime.timedelta(days=28)).strftime("%Y-%m-%d")

    # ventes par pays
    ventes_valides = VenteParPays.objects.filter(
        Q(slug__in=Billet.objects.filter(valide=True).values_list("slug", flat=True))
        & Q(
            slug__in=Paiement.objects.filter(valide=True).values_list(
                "billet__slug", flat=True
            )
        ),
        date_vente__range=(since, until),
    )
    ventes_groupees = ventes_valides.values("pays").annotate(nombre_ventes=Count("id"))


    # chiffre_affaire
    ca_aujourdhui = Paiement.objects.filter(
        valide=True, billet__gratuit=False, date__date=until
    )
    chiffre_affaire = Paiement.calculer_paiement(ca_aujourdhui)
    # revenus
    paiements = Paiement.objects.filter(
        valide=True, billet__gratuit=False, date__gte=since
    ).order_by("-date")
    somme = Paiement.calculer_paiement(paiements)
    revenus = somme * 40 / 100
    # revenus last_month
    paiements_last_month = Paiement.objects.filter(
        valide=True, billet__gratuit=False, date__range=(last_month, since)
    ).order_by("-date")
    revenus_last_month = (Paiement.calculer_paiement(paiements_last_month)) * 40 / 100
    difference_revenus = revenus - revenus_last_month

    if revenus_last_month > 0:
        revenus_difference_en_pourcentage = (
            difference_revenus / revenus_last_month
        ) * 100
    else:
        revenus_difference_en_pourcentage = 0

    depense = somme - revenus
    # oeuvre vendu
    oeuvre_vendu = len(paiements)
    oeuvre_vendu_last_month = len(paiements_last_month)
    oeuvre_difference = oeuvre_vendu - oeuvre_vendu_last_month

    if oeuvre_vendu_last_month > 0:
        oeuvre_difference_en_pourcentage = (
            oeuvre_difference / oeuvre_vendu_last_month
        ) * 100
    else:
        oeuvre_difference_en_pourcentage = 0

    # utilisateurs actifs
    if check_internet_connection():
        utilisateurs = getUtilisateurActive(since, until)
        utilisateurs_last_month = getUtilisateurActive(last_month, since)
        utilisateurs_difference = utilisateurs - utilisateurs_last_month

        if utilisateurs_last_month > 0:
            utilisateurs_difference_en_pourcentage = (
                utilisateurs_difference / utilisateurs_last_month
            ) * 100
        else:
            utilisateurs_difference_en_pourcentage = 0
        
        #facebook
        facebook = pageInformationData()


    # transactions
    transactions = Paiement.objects.filter(
        billet__gratuit=False, date__gte=since
    ).order_by("-date")[:4]

    # top video
    ventes_par_video = (
        Video.objects.annotate(
            nombre_ventes=Count(
                "video_billet__billet_paiement__id",
                distinct=True,
                filter=Q(
                    video_billet__billet_paiement__valide=True,
                    video_billet__valide=True,
                    video_billet__gratuit=False,
                    video_billet__billet_paiement__date__gte=since,
                ),
            )
        ).values("titre", "nombre_ventes", "photo_de_couverture", "artiste__nom")
    )[:4]

    # pages
    # pages=pageStatistique(since,until)
    pages = (
        PageAnalytics.objects.filter(date__gte=since)
        .values("path", "screenname")
        .annotate(total_vue=Coalesce(Sum("vue"), 0))
        .order_by("-total_vue")[:20]
    )

    date_actuelle = datetime.datetime.now()
    if check_internet_connection():
        context = {
        "utilisateur": utilisateurs,
        "utilisateur_last_month": utilisateurs_difference_en_pourcentage,
        "utilisateur_last_month_negative": utilisateurs_difference_en_pourcentage
        * (-1),
        "facebook": facebook,
        "venteparpays": ventes_groupees,
        "pages": pages,
        "compte": nombre_utilisateurs_crees,
        "comptes_recents": comptes_recents,
        "revenue": revenus,
        "revenue_difference_negative": difference_revenus * (-1),
        "revenue_difference": difference_revenus,
        "revenue_pourcentage": revenus_difference_en_pourcentage,
        "transactions": transactions,
        "oeuvre": oeuvre_vendu,
        "oeuvre_last_month": oeuvre_difference,
        "oeuvre_last_month_negative": oeuvre_difference * (-1),
        "oeuvre_pourcentage": oeuvre_difference_en_pourcentage,
        "chiffre_affaire": chiffre_affaire,
        "depense": depense,
        "ventes_par_video": ventes_par_video,
        "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
            :5
        ],
        "annees": list(range(2022, date_actuelle.year + 1)),
        "date_actuelle": date_actuelle,
        }
    else:
        context = {
        "venteparpays": ventes_groupees,
        "pages": pages,
        "compte": nombre_utilisateurs_crees,
        "comptes_recents": comptes_recents,
        "revenue": revenus,
        "revenue_difference_negative": difference_revenus * (-1),
        "revenue_difference": difference_revenus,
        "revenue_pourcentage": revenus_difference_en_pourcentage,
        "transactions": transactions,
        "oeuvre": oeuvre_vendu,
        "oeuvre_last_month": oeuvre_difference,
        "oeuvre_last_month_negative": oeuvre_difference * (-1),
        "oeuvre_pourcentage": oeuvre_difference_en_pourcentage,
        "chiffre_affaire": chiffre_affaire,
        "depense": depense,
        "ventes_par_video": ventes_par_video,
        "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
            :5
        ],
        "annees": list(range(2022, date_actuelle.year + 1)),
        "date_actuelle": date_actuelle,
    }
    return render(request, "dashboard.html", context)



def statistiques_ventes_json(request, annee):
    date_actuelle = datetime.datetime.now()
    if int(annee) == date_actuelle.year:
        statistiques_ventes = (
            Paiement.objects.filter(
                valide=True,
                billet__gratuit=False,
                date__year=annee,
                date__month__lte=date_actuelle.month,
            )
            .annotate(mois=TruncMonth("date"))
            .values("mois")
            .annotate(
                nombre_ventes=Count("id"),
                revenues=Sum(
                    Case(
                        When(mode=2, then=F("billet__video__tarif_euro") * prix_ariary_euro),
                        default=F("billet__video__tarif_ariary"),
                        output_field=IntegerField(),
                    )
                )
                * 60
                / 100,
            )
            .order_by("mois")
        )
    else:
        # Affiche tous les mois de l'année
        statistiques_ventes = (
            Paiement.objects.filter(
                valide=True, billet__gratuit=False, date__year=annee
            )
            .annotate(mois=TruncMonth("date"))
            .values("mois")
            .annotate(
                nombre_ventes=Count("id"),
                revenues=Sum(
                    Case(
                        When(mode=2, then=F("billet__video__tarif_euro") * prix_ariary_euro),
                        default=F("billet__video__tarif_ariary"),
                        output_field=IntegerField(),
                    )
                )
                * 60
                / 100,
            )
            .order_by("mois")
        )

    donnees_statistiques = {}
    locale.setlocale(locale.LC_TIME, "fr_FR")

    for mois in range(1, 13):
        mois_str = date_actuelle.replace(day=1, month=mois).strftime("%B")
        donnees_statistiques[mois_str] = {
            "mois": mois_str,
            "nombre_ventes": 0,
            "revenues": 0,
        }

    for resultat in statistiques_ventes:
        mois_str = resultat["mois"].strftime("%B")
        donnees_statistiques[mois_str] = {
            "mois": mois_str,
            "nombre_ventes": resultat["nombre_ventes"],
            "revenues": resultat["revenues"],
        }

    return JsonResponse({"statistiques_ventes": donnees_statistiques})


def facebook(request):
    if check_internet_connection():
        marquer_notification_read(request)
        since = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime("%Y-%m-%d")
        until = datetime.datetime.now().strftime("%Y-%m-%d")
        context = {
            "information": pageInformationData(),
            "vue_ensemble": page_vue_ensemble(since, until),
            "contenus": contenu_recent(since, until)["data"],
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
                :5
            ],
        }
    else:
        context={
            "erreur":"Un problème de connexion"
        }
    return render(request, "facebook.html", context)


def audiences(request):
    if check_internet_connection():
        marquer_notification_read(request)
        # 28 derniers jours
        since = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime("%Y-%m-%d")
        until = datetime.datetime.now().strftime("%Y-%m-%d")

        sexe = AudienceParSexe(since, until)
        countries = demographieParPays(since, until)
        agesexe = AudienceParAgeEtSexe(since, until)
        langues = demographicsByLanguage(since, until)
        sources = SourceDesClics(since, until)
        context = {
            "audience": "true",
            "sexe": sexe,
            "countries": countries,
            "ageSexes": agesexe,
            "langues": langues,
            "sources": sources,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
                :5
            ],
        }
    else:
        context={
            "erreur":"Un problème de connexion"
        }
    return render(request, "audiences.html", context)


def marquer_notification_read(request):
    if request.GET.get("read_notification"):
        notification = NotificationFCM.objects.get(id=request.GET.get("notification"))
        notification.mark_as_read()


def get_age_sexe(request):
    if request.GET.get("debut"):
        date_debut = datetime.datetime.strptime(
            request.GET.get("debut"), "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
        date_fin = datetime.datetime.strptime(
            request.GET.get("fin"), "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
    else:
        date_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        date_debut = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime(
            "%Y-%m-%d"
        )
    data = AudienceParAgeEtSexe(date_debut, date_fin)
    return JsonResponse(data)


def ventes_data_pays(request):
    if request.GET.get("debut"):
        date_debut = datetime.datetime.strptime(request.GET.get("debut"), "%Y-%m-%d")
        date_fin = datetime.datetime.strptime(request.GET.get("fin"), "%Y-%m-%d")
    else:
        date_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        date_debut = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime(
            "%Y-%m-%d"
        )
    ventes_valides = VenteParPays.objects.filter(
        Q(slug__in=Billet.objects.filter(valide=True).values_list("slug", flat=True))
        & Q(
            slug__in=Paiement.objects.filter(valide=True).values_list(
                "billet__slug", flat=True
            )
        ),
        date_vente__range=(date_debut, date_fin),
    )
    ventes_groupees = ventes_valides.values("pays").annotate(nombre_ventes=Count("id"))
    sample_data = {}

    for ventes in ventes_groupees:
        if ventes["pays"] not in [
            "Martinique",
            "Mayotte",
            "Singapore",
            "Luxembourg",
            "St. Pierre & Miquelon",
            "Türkiye",
            "(not set)",
        ] and ventes['pays'] in country_mapping:
            country = country_mapping[ventes["pays"]]
            nb_ventes = ventes["nombre_ventes"]

        sample_data[country] = nb_ventes
    return JsonResponse(sample_data)


def ventes_data(request):
    if request.GET.get("debut"):
        date_debut = datetime.datetime.strptime(
            request.GET.get("debut"), "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
        date_fin = datetime.datetime.strptime(
            request.GET.get("fin"), "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
    else:
        date_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        date_debut = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime(
            "%Y-%m-%d"
        )
    ventes_valides = VenteParPays.objects.filter(
        Q(
            slug__in=Billet.objects.filter(
                valide=True, video__artiste__user=request.user.id
            ).values_list("slug", flat=True)
        )
        & Q(
            slug__in=Paiement.objects.filter(valide=True).values_list(
                "billet__slug", flat=True
            )
        ),
        date_vente__range=(date_debut, date_fin),
    )
    ventes_groupees = ventes_valides.values("pays").annotate(nombre_ventes=Count("id"))
    sample_data = {}
    total = 0
    mada = 0
    international = 0
    for ventes in ventes_groupees:
        total = total + ventes["nombre_ventes"]
        if ventes["pays"] == "Madagascar":
            mada = mada + ventes["nombre_ventes"]
        else:
            international = international + ventes["nombre_ventes"]

    if total > 0:
        sample_data["Madagascar"] = mada * 100 / total
        sample_data["International"] = international * 100 / total

    else:
        sample_data["Madagascar"] = 0
        sample_data["International"] = 0
    return JsonResponse(sample_data)


def get_sample_data(request):
    if request.GET.get("debut"):
        date_debut = datetime.datetime.strptime(
            request.GET.get("debut"), "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
        date_fin = datetime.datetime.strptime(
            request.GET.get("fin"), "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
    else:
        date_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        date_debut = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime(
            "%Y-%m-%d"
        )
    data = demographieParPays(date_debut, date_fin)
    sample_data = {}

    for entry in data.values:
        if entry[0] not in [
            "Martinique",
            "Mayotte",
            "Singapore",
            "Luxembourg",
            "St. Pierre & Miquelon",
            "Türkiye",
            "(not set)",
        ] and entry[0] in country_mapping:
            country = country_mapping[entry[0]]
            users = entry[1]

        sample_data[country] = users
    return JsonResponse(sample_data)


def get_sources(request):
    if request.GET.get("debut"):
        date_debut = datetime.datetime.strptime(
            request.GET.get("debut"), "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
        date_fin = datetime.datetime.strptime(
            request.GET.get("fin"), "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
    else:
        date_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        date_debut = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime(
            "%Y-%m-%d"
        )
    data = SourceDesClics(date_debut, date_fin)
    sample_data = {}
    for entry in data.values:
        source = entry[0]
        users = entry[1]
        sample_data[source] = users

    return JsonResponse(sample_data)


def get_langue(request):
    if request.GET.get("debut"):
        date_debut = datetime.datetime.strptime(
            request.GET.get("debut"), "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
        date_fin = datetime.datetime.strptime(
            request.GET.get("fin"), "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
    else:
        date_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        date_debut = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime(
            "%Y-%m-%d"
        )
    data = demographicsByLanguage(date_debut, date_fin)
    sample_data = {}
    for entry in data.values:
        langue = entry[0]
        users = entry[1]
        sample_data[langue] = users

    return JsonResponse(sample_data)


def listeartiste(request):
    marquer_notification_read(request)
    artistes = Artiste.objects.all().order_by("id")
    total=artistes.count()
    total_artiste_actif=Artiste.objects.filter(en_ligne=True).count()
    utilisateurs = User.objects.all()

    paginator = Paginator(artistes, pagination)

    page_number = request.GET.get("page")
    paginated_artistes = paginator.get_page(page_number)

    context = {
        "artistes": paginated_artistes,
        "utilisateurs": utilisateurs,
        "total":total,
        "total_artiste_actif":total_artiste_actif,
        "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
            :5
        ],
    }
    return render(request, "artistes_crud.html", context)


def rechercheartiste(request):
    if request.GET.get("search"):
        keyword = request.GET.get("search")
        artistes = Artiste.objects.filter(
            Q(nom__icontains=keyword) | Q(slug__icontains=keyword)
        )
    else:
        artistes = Artiste.objects.all().order_by("id")

    utilisateurs = User.objects.all()

    paginator = Paginator(artistes, pagination)

    page_number = request.GET.get("page")
    paginated_artistes = paginator.get_page(page_number)
    total=artistes.count()
    total_artiste_actif=Artiste.objects.filter(en_ligne=True).count()

    if request.GET.get("search"):
        context = {
            "search": request.GET.get("search"),
            "artistes": paginated_artistes,
            "utilisateurs": utilisateurs,
            "total":total,
            "total_artiste_actif":total_artiste_actif,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by(
                "-created_at"
            )[:5],
        }
    else:
        context = {
            "search": request.GET.get("search"),
            "artistes": paginated_artistes,
            "utilisateurs": utilisateurs,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by(
                "-created_at"
            )[:5],
        }
    return render(request, "artistes_crud.html", context)

# from django.contrib.auth.decorators import permission_required

class ArtisteCreate(generics.CreateAPIView):
    queryset = Artiste.objects.all()
    serializer_class = ArtisteSerializer


class ArtisteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artiste.objects.all()
    serializer_class = ArtisteSerializer
    lookup_field = "pk"


def associations(request):
    marquer_notification_read(request)
    associations = Association.objects.all().order_by("id")
    utilisateurs = User.objects.all()
    paginator = Paginator(associations, pagination)
    total=associations.count()
    total_association_actif= Association.objects.filter(en_ligne=True).count()

    page_number = request.GET.get("page")
    paginated_associations = paginator.get_page(page_number)

    context = {
        "associations": paginated_associations,
        "utilisateurs": utilisateurs,
        "total":total,
        "total_association_actif":total_association_actif,
        "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
            :5
        ],
    }

    return render(request, "associations_crud.html", context)


def rechercheassociations(request):
    if request.GET.get("search"):
        keyword = request.GET.get("search")
        associations = Association.objects.filter(
            Q(nom__icontains=keyword) | Q(description__icontains=keyword)
        )
    else:
        associations = Association.objects.all().order_by("id")

    utilisateurs = User.objects.all()

    paginator = Paginator(associations, pagination)

    page_number = request.GET.get("page")
    paginated_associations = paginator.get_page(page_number)

    total=associations.count()
    total_association_actif= Association.objects.filter(en_ligne=True).count()

    if request.GET.get("search"):
        context = {
            "search": request.GET.get("search"),
            "associations": paginated_associations,
            "utilisateurs": utilisateurs,
            "total":total,
            "total_association_actif":total_association_actif,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by(
                "-created_at"
            )[:5],
        }
    else:
        context = {
            "associations": paginated_associations,
            "utilisateurs": utilisateurs,
            "total":total,
            "total_association_actif":total_association_actif,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by(
                "-created_at"
            )[:5],
        }
    return render(request, "associations_crud.html", context)


def switchUser(request, user):
    request.session["utilisateur"] = user
    response_data = {"message": "Utilisateur enregistré avec succès"}
    return JsonResponse(response_data)

def recupererData(request):
    debut_28 = datetime.datetime.now() - datetime.timedelta(days=28)
    since = debut_28.strftime("%Y-%m-%d")
    dataVenteParPays(since,datetime.datetime.now())
    pageStatistique(since,datetime.datetime.now())

def envoi_notification_administrateur(request):
    aujourd_hui = datetime.date.today()
    hier = aujourd_hui - datetime.timedelta(days=1)
    debut_journee = datetime.datetime.combine(hier, datetime.datetime.min.time())

    fin_journee = datetime.datetime.combine(hier, datetime.datetime.max.time())
    comptes = User.objects.filter(date_joined__range=(debut_journee,fin_journee)).count()
    paiements = Paiement.objects.filter(
        valide=True, billet__gratuit=False, date__range=(debut_journee,fin_journee)
    ).order_by("-date")
    somme = Paiement.calculer_paiement(paiements)
    revenus = somme * 40 / 100
    ventes=paiements.count()
    body1 = "Il y a "+str(ventes)+" ventes hier, ce qui fait un revenu de "+str(intcomma(revenus))+"Ariary."
    body2 = "Il y a eu "+str(comptes)+" crées hier"
    if(ventes>0) :
        send_notification(
        "http://localhost:8000/ventes_video",
        2,
        "Ventes",
        body1,
    )
    if(comptes>0) :
        send_notification(
        "http://localhost:8000/compteutilisateur",
        2,
        "Comptes crées",
        body2,
    )

def send_notification(url, user, titre, message):
    firebase_app = firebase_admin.get_app()
    device = FCMDevice.objects.filter(user_id=user).first()
    if device:
        NotificationFCM.objects.create(
            title=titre,
            content=message,
            destination_url=url,
            user=User.objects.filter(id=user).first(),
        )
        message = Message(
            notification=Notification(
                title=titre, body=message, image="../../assets/images/brand/favicon.png"
            ),
            token=device.registration_id,
            data={"click_action": url},
        )

        response = device.send_message(message, app=firebase_app)
        if response:
            return True
        else:
            return False
    else:
        return False


class AssociationCreate(generics.CreateAPIView):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer


class OrganisateurCreate(generics.CreateAPIView):
    queryset = Organisateur.objects.all()
    serializer_class = OrganisteurSerializer


class LiveCreate(generics.CreateAPIView):
    queryset = Live.objects.all()
    serializer_class = LiveSerializer

    def perform_create(self, serializer):
        instance = serializer.save()


class VideosCreate(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class AssociationUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer
    lookup_field = "pk"


class LiveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Live.objects.all()
    serializer_class = LiveSerializer
    lookup_field = "pk"


class VideosUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = "pk"


class OrganisateurUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organisateur.objects.all()
    serializer_class = OrganisteurSerializer
    lookup_field = "pk"


def listevideos(request):
    marquer_notification_read(request)
    videos = Video.objects.all().order_by("id")
    artistes = Artiste.objects.all()
    organisateurs = Organisateur.objects.all()
    actions = Action.objects.all()
    lives = Live.objects.all()

    paginator = Paginator(videos, pagination)

    page_number = request.GET.get("page")
    paginated_videos = paginator.get_page(page_number)

    total=videos.count()
    total_gratuit=Video.objects.filter(en_ligne=True,gratuit=True).count()
    total_film=Video.objects.filter(en_ligne=True,is_film=True).count()
    total_live=Video.objects.filter(en_ligne=True,is_live=True).count()
    total_levee_de_fond=Video.objects.filter(en_ligne=True,levee_de_fond=True).count()
    context = {
        "total":total,
        'total_film':total_film,
        'total_gratuit':total_gratuit,
        'total_live':total_live,
        'total_levee_de_fond':total_levee_de_fond,
        "videos": paginated_videos,
        "artistes": artistes,
        "organisateurs": organisateurs,
        "actions": actions,
        "lives": lives,
        "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
            :5
        ],
    }
    return render(request, "video_crud.html", context)


def recherchevideos(request):
    if request.GET.get("search"):
        keyword = request.GET.get("search")
        videos = Video.objects.filter(
            Q(titre__icontains=keyword) | Q(description_longue__icontains=keyword)
        )
    else:
        videos = Video.objects.all().order_by("id")

    artistes = Artiste.objects.all()
    organisateurs = Organisateur.objects.all()
    actions = Action.objects.all()
    lives = Live.objects.all()

    paginator = Paginator(videos, pagination)

    page_number = request.GET.get("page")
    paginated_videos = paginator.get_page(page_number)
    total=videos.count()
    total_gratuit=Video.objects.filter(en_ligne=True,gratuit=True).count()
    total_film=Video.objects.filter(en_ligne=True,is_film=True).count()
    total_live=Video.objects.filter(en_ligne=True,is_live=True).count()
    total_levee_de_fond=Video.objects.filter(en_ligne=True,levee_de_fond=True).count()

    if request.GET.get("search"):
        context = {
            "total":total,
            'total_film':total_film,
            'total_gratuit':total_gratuit,
            'total_live':total_live,
            'total_levee_de_fond':total_levee_de_fond,
            "search": request.GET.get("search"),
            "videos": paginated_videos,
            "artistes": artistes,
            "organisateurs": organisateurs,
            "actions": actions,
            "lives": lives,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by(
                "-created_at"
            )[:5],
        }
    else:
        context = {
            "total":total,
            'total_film':total_film,
            'total_gratuit':total_gratuit,
            'total_live':total_live,
            'total_levee_de_fond':total_levee_de_fond,
            "search": request.GET.get("search"),
            "videos": paginated_videos,
            "artistes": artistes,
            "organisateurs": organisateurs,
            "actions": actions,
            "lives": lives,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by(
                "-created_at"
            )[:5],
        }
    return render(request, "video_crud.html", context)


def listeorganisteurs(request):
    marquer_notification_read(request)
    organisateurs = Organisateur.objects.all().order_by("id")
    details = organisateurs.first()

    total=organisateurs.count()
    total_actif=Organisateur.objects.filter(en_ligne=True).count()
    total_association=Organisateur.objects.filter(en_ligne=True,is_association=True).count()

    utilisateurs = User.objects.all()

    context = {
        "total":total,
        "total_actif":total_actif,
        "total_association":total_association,
        "organisateurs": organisateurs,
        "details": details,
        "utilisateurs": utilisateurs,
        "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
            :5
        ],
    }

    return render(request, "organisateurs_crud.html", context)


def rechercheorganisateur(request):
    if request.GET.get("search"):
        keyword = request.GET.get("search")
        organisateurs = Organisateur.objects.filter(
            Q(nom__icontains=keyword) | Q(description__icontains=keyword)
        )
    else:
        organisateurs = Organisateur.objects.all().order_by("id")

    utilisateurs = User.objects.all()
    details = organisateurs.first()
    if request.GET.get("search"):
        context = {
            "search": request.GET.get("search"),
            "organisateurs": organisateurs,
            "details": details,
            "utilisateurs": utilisateurs,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by(
                "-created_at"
            )[:5],
        }
    else:
        context = {
            "organisateurs": organisateurs,
            "details": details,
            "utilisateurs": utilisateurs,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by(
                "-created_at"
            )[:5],
        }
    return render(request, "organisateurs_crud.html", context)


from django.core import serializers


def searchorganisateur(request):
    if request.GET.get("search"):
        keyword = request.GET.get("search")
        organisateurs = Organisateur.objects.filter(
            Q(nom__icontains=keyword) | Q(description__icontains=keyword)
        )
    else:
        organisateurs = Organisateur.objects.all().order_by("id")

    serialized_organisateurs = serializers.serialize("python", organisateurs)

    organisateurs_data = []
    for entry in serialized_organisateurs:
        org_data = entry["fields"]
        org_data["id"] = entry["pk"]

        user_id = org_data.pop("user")

        user = User.objects.get(pk=user_id)
        user_data = {
            "id": user.id,
            "username": user.username,
        }

        org_data["user"] = user_data
        organisateurs_data.append(org_data)

    return JsonResponse({"organisateurs": organisateurs_data}, safe=False)


def detailsorganisateur(request):
    if request.GET.get("id"):
        idorganisateur = request.GET.get("id")
        organisateur = Organisateur.objects.filter(id=idorganisateur).first()
    else:
        organisateur = Organisateur.objects.all().order_by("id").first()

    org_serialized = serializers.serialize("python", [organisateur])
    user_id = org_serialized[0]["fields"].pop("user")

    user = User.objects.get(pk=user_id)
    user_data = {
        "id": user.id,
        "username": user.username,
    }

    org_serialized[0]["fields"]["user"] = user_data
    org_serialized[0]["fields"]["id"] = organisateur.id

    return JsonResponse({"details": org_serialized[0]["fields"]}, safe=False)


def listelive(request):
    marquer_notification_read(request)
    lives = Live.objects.all().order_by("id")
    paginator = Paginator(lives, pagination)

    page_number = request.GET.get("page")
    paginated_live = paginator.get_page(page_number)
    total=lives.count()
    total_live_en_ligne=Live.objects.filter(en_ligne=True).count()
    total_live_en_ligne_debut=Live.objects.filter(en_ligne=True,debut=True).count()

    context = {
        "lives": paginated_live,
        "total":total,
        "total_live_en_ligne":total_live_en_ligne,
        "total_live_en_ligne_debut":total_live_en_ligne_debut,
        "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
            :5
        ],
    }
    return render(request, "live_crud.html", context)


def recherchelive(request):
    if request.GET.get("search"):
        keyword = request.GET.get("search")
        lives = Live.objects.filter(
            Q(titre__icontains=keyword) | Q(date__icontains=keyword)
        )
    else:
        lives = Live.objects.all().order_by("id")

    paginator = Paginator(lives, pagination)

    page_number = request.GET.get("page")
    paginated_lives = paginator.get_page(page_number)
    total=lives.count()
    total_live_en_ligne=Live.objects.filter(en_ligne=True).count()
    total_live_en_ligne_debut=Live.objects.filter(en_ligne=True,debut=True).count()
    if request.GET.get("search"):
        context = {
            "total":total,
            "total_live_en_ligne":total_live_en_ligne,
            "total_live_en_ligne_debut":total_live_en_ligne_debut,
            "search": request.GET.get("search"),
            "lives": paginated_lives,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by(
                "-created_at"
            )[:5],
        }
    else:
        context = {
            "total":total,
            "total_live_en_ligne":total_live_en_ligne,
            "total_live_en_ligne_debut":total_live_en_ligne_debut,
            "lives": paginated_lives,
            "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by(
                "-created_at"
            )[:5],
        }
    return render(request, "live_crud.html", context)


def artistes(request):
    marquer_notification_read(request)
    performances_artiste = (
        Artiste.objects.annotate(
            nombre_ventes=Count(
                "artiste_video__video_billet__billet_paiement__id",
                distinct=True,
                filter=Q(
                    artiste_video__video_billet__billet_paiement__valide=True,
                    artiste_video__video_billet__valide=True,
                    artiste_video__video_billet__gratuit=False,
                ),
            )
        ).values("nom", "nombre_ventes", "photo_de_profil", "user__date_joined")
    ).order_by("-nombre_ventes")

    meilleur_artiste = performances_artiste.first()
    if meilleur_artiste:
        nombre_ventes_meilleur_artiste = meilleur_artiste["nombre_ventes"]
    else:
        nombre_ventes_meilleur_artiste = 0

    # Calculer le pourcentage de performances pour chaque artiste
    performances_avec_pourcentage = []
    for artiste in performances_artiste:
        nombre_ventes_artiste = artiste["nombre_ventes"]
        if nombre_ventes_meilleur_artiste>0:
            pourcentage_performance = (
                nombre_ventes_artiste / nombre_ventes_meilleur_artiste
            ) * 100
        else :
            pourcentage_performance=0
        artiste["pourcentage_performance"] = round(pourcentage_performance, 2)
        performances_avec_pourcentage.append(artiste)

    context = {
        "artistes": performances_avec_pourcentage,
        "notifications": NotificationFCM.objects.filter(user=request.user.id).order_by("-created_at")[
            :5
        ],
    }

    return render(request, "artistes.html", context)