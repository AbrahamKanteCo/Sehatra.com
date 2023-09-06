from paiement.models import Billet
from plateforme.models import Video
from django.shortcuts import redirect


def billet_create (request, video):
    billet= Billet()
    video = Video.objects.get(slug=video)
    billet.video = video
    billet.user = request.user
    billet.save()
    return redirect("/paiement/{}/".format(billet.slug))

