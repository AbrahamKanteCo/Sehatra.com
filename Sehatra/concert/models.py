from django.db import models
from django_resized import ResizedImageField
from django.utils.text import slugify
from django.contrib.auth.models import User
import unicodedata
import uuid
import datetime

# Create your models here.
import os


def remove_accents(input_str):
    return ''.join((c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn'))


def upload_to (instance, filename):
    upload = instance.__class__.__name__.lower()
    filename = remove_accents(filename)
    return os.path.join(upload, filename)


class Artiste (models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom


class Concert (models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    artiste = models.ForeignKey(Artiste, on_delete=models.DO_NOTHING, related_name="artiste_concert")
    jour = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    mois = models.CharField(max_length=200)
    heure = models.CharField(max_length=200)
    tarif = models.CharField(max_length=200)
    photo_de_couverture_large = ResizedImageField(upload_to=upload_to,
                                                  quality=100,
                                                  force_format='PNG',
                                                  null=True,
                                                  blank=True,
                                                  )

    photo_de_couverture_slider = ResizedImageField(upload_to=upload_to,
                                                  quality=100,
                                                  force_format='PNG',
                                                  null=True,
                                                  blank=True,
                                                  )

    galerie1 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    galerie2 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    galerie3 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    galerie4 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    galerie5 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    galerie6 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    lien_video = models.URLField(null=True, blank=True)
    lien_video_dash = models.URLField(null=True, blank=True)
    lien_video_hls = models.URLField(null=True, blank=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    en_cours = models.BooleanField(default=False)
    actif = models.BooleanField(default=True)
    termine = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre) + "-"+ str(self.date)
        super(Concert, self).save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return "/concert/"+ str(self.slug)


class Video (models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    artiste = models.ForeignKey(Artiste, on_delete=models.DO_NOTHING, related_name="artiste_video")
    photo_de_couverture_large = ResizedImageField(upload_to=upload_to,
                                                  quality=100,
                                                  force_format='PNG',
                                                  null=True,
                                                  blank=True,
                                                  )
    photo_de_couverture_slider = ResizedImageField(upload_to=upload_to,
                                                  quality=100,
                                                  force_format='PNG',
                                                  null=True,
                                                  blank=True,
                                                  )
    galerie1 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    galerie2 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    galerie3 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    galerie4 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    galerie5 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    galerie6 = ResizedImageField(blank=True,
                                 null=True,
                                 upload_to=upload_to,
                                 # size=[1000,400],
                                 # crop=["middle", "center"],
                                 quality=75,
                                 force_format='PNG'
                                 # help_text="Veuillez choisir une image de taille: 1000x400 ou proportionnelle"
                                 )
    lien_video = models.URLField(null=True, blank=True)
    acces_libre = models.BooleanField(default=True)
    disponible = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return "/video/"+ str(self.slug)


class Billet(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user_billet", null=True)
    concert = models.ForeignKey(Concert, on_delete=models.DO_NOTHING, related_name="concert_billet")
    slug = models.CharField(max_length=50, unique=True, null=True, blank=True)
    valide = models.BooleanField(default=False)
    gratuit = models.BooleanField(default=False)

    def __str__(self):
        return str(self.concert) + " - " + str(self.user)

    def save(self, *args, **kwargs):
        if not self.slug:
            while True:
                try:
                    self.slug = uuid.uuid4().hex[:6].upper()
                    super(Billet, self).save(*args, **kwargs)
                    break
                except:
                    pass
        else:
            super(Billet, self).save(*args, **kwargs)


class Paiement(models.Model):
    billet = models.ForeignKey(Billet, on_delete=models.CASCADE, related_name="billet_concert")
    CHOICES = (
        ('MVola', 'MVola'),
        ('Orange Money', 'Orange Money'),
        ('Moobi Pay', 'Moobi Pay'),
        ('Espèce', 'Espèce')
    )
    date = models.DateField(auto_now=datetime.date.today())
    mode_de_paiement = models.CharField(max_length=300, choices=CHOICES)
    token = models.CharField(max_length=200, null=True, blank=True)
    valide = models.BooleanField(default=False)
    notif = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.billet) + " - " + self.mode_de_paiement


class ConcertAccueil (models.Model):
    titre = models.CharField(max_length=50)
    concert_1 = models.ForeignKey(Concert, on_delete=models.DO_NOTHING, related_name="concert_accueil_1", null=True, blank=True)
    concert_2 = models.ForeignKey(Concert, on_delete=models.DO_NOTHING, related_name="concert_accueil_2", null=True, blank=True)
    concert_3 = models.ForeignKey(Concert, on_delete=models.DO_NOTHING, related_name="concert_accueil_3", null=True, blank=True)

    def __str__(self):
        return self.titre


class VideoAccueil (models.Model):
    titre = models.CharField(max_length=50)
    video_1 = models.ForeignKey(Video, on_delete=models.DO_NOTHING, related_name="video_accueil_1", null=True, blank=True)
    video_2 = models.ForeignKey(Video, on_delete=models.DO_NOTHING, related_name="video_accueil_2", null=True, blank=True)
    video_3 = models.ForeignKey(Video, on_delete=models.DO_NOTHING, related_name="video_accueil_3", null=True, blank=True)

    def __str__(self):
        return self.titre


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.DO_NOTHING)
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username


class FormulaireReclamation(models.Model):
    CHOICES = (
        ('Problème de création de compte ou de connexion', "Problème de création de compte ou de connexion"),
        ("Problème avec l'achat de billet ou le paiement", "Problème avec l'achat de billet ou le paiement"),
        ("Problème avec la vidéo", "Problème avec la vidéo"),
        ("Autre", "Autre"),
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user_formulaire")
    motif = models.CharField(max_length=250, choices=CHOICES, null=True)
    message = models.TextField(null=True, verbose_name="Description de votre problème", blank=True)
    date = models.DateField(auto_now=True)

