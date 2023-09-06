from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# Register your models here.
from .models import *


admin.site.unregister(User)
@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ('username', 'date_joined', "email")


admin.site.register(Profil)
admin.site.register(Artiste)
admin.site.register(Association)
admin.site.register(Organisateur)
admin.site.register(Video)
admin.site.register(Action)
admin.site.register(Actualite)
admin.site.register(Live)
admin.site.register(Test)


