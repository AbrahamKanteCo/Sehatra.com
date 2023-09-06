from django.db import models
from plateforme.models import Video
from django.contrib.auth.models import User
import uuid


class Billet (models.Model):
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, related_name="video_billet")
    date = models.DateTimeField(auto_now=True)
    valide = models.BooleanField(default=False)
    gratuit = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="utilisateur_billet")
    slug = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            while True:
                try:
                    self.slug = uuid.uuid4().hex[:8].upper()
                    super(Billet, self).save(*args, **kwargs)
                    break
                except:
                    pass
        else:
            super(Billet, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class ModePaiement (models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class Paiement (models.Model):
    billet = models.ForeignKey(Billet, on_delete=models.CASCADE, related_name="billet_paiement")
    mode = models.ForeignKey(ModePaiement, on_delete=models.CASCADE, related_name="mode_paiement")
    valide = models.BooleanField(default=False)
    telephone = models.CharField(null=True, blank=True, max_length=150)
    date = models.DateTimeField(auto_now=True)
    token = models.TextField(null=True)
    notif_token = models.TextField(null=True)

    def __str__(self):
        return self.mode.nom
