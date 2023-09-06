from django.contrib import admin
from .models import Artiste, Billet, Concert, Paiement, Video, ConcertAccueil, VideoAccueil
from django_object_actions import DjangoObjectActions
import requests


def validate_token(token):
    access_token = "f3644d524e292a191fb0c8d64df6696cf5481d9daf7b6e7afc802882e187831a"
    url_paiement = "https://api.moobipay.com/v1/paiment-status"
    header = {"Authorization": "Bearer " + access_token}
    data= {}
    data['pay_token'] = token
    res = requests.post(url_paiement, json=data, headers= header)
    if res.json()['status'] == "success":
        return True
    else:
        return False


class BilletAdmin(DjangoObjectActions, admin.ModelAdmin):
    def valider_billet(self, request, obj):
        paiement = Paiement.objects.get(billet=obj)
        if validate_token(paiement.token):
            obj.valide = True
            paiement.valide = True
            obj.save()
            paiement.save()

    valider_billet.label = "Valider billet"
    valider_billet.short_description = "Valider si le paiement a été effectué avec succès"
    list_display = ["slug", "user", "valide", "concert"]
    list_filter = ['valide']
    change_actions = ('valider_billet', )


class PaiementAdmin(admin.ModelAdmin):
    list_display = ["__str__", "date", "valide", "token"]
    list_filter = ['valide', "date"]


class VideoAdmin(admin.ModelAdmin):
    list_display = ["titre", "artiste", "disponible", "acces_libre"]


admin.site.register(Artiste)
admin.site.register(Concert)
admin.site.register(Billet, BilletAdmin)
admin.site.register(Paiement, PaiementAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(VideoAccueil)
admin.site.register(ConcertAccueil)


admin.site.site_header = 'SEHATRA.COM - Administration'
admin.site.index_title = 'Administration Sehatra.com'                 # default: "Site administration"
admin.site.site_title = 'Administration'