from django.contrib import admin
from .models import *


class PaiementAdmin(admin.ModelAdmin):
    list_display = ["billet", "video", "date", "valide", "mode", "user"]

    def video(self, obj):
        return obj.billet.video

    def user(self, obj):
        return obj.billet.user


class BilletAdmin(admin.ModelAdmin):
    list_display = ["__str__", "valide", "video", "date", "user"]
    list_filter = ["video", "valide", "date", "gratuit"]

# Register your models here.
admin.site.register(Billet, BilletAdmin)
admin.site.register(ModePaiement)
admin.site.register(Paiement, PaiementAdmin)



