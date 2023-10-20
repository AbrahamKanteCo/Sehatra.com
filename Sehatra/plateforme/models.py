from django.db import models
import unicodedata
import uuid
import os
from django.contrib.auth.models import User
from django_resized import ResizedImageField
import datetime
from django_countries.fields import CountryField
from django.utils.text import slugify


def custom_upload_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{timestamp}_{base_filename}{file_extension}"
    return f'{new_filename}'


def remove_accents(input_str):
    return ''.join((c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn'))


def upload_to (instance, filename):
    upload = instance.__class__.__name__.lower() + "/" + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    filename = remove_accents(filename)
    return os.path.join(upload, filename)


#profil utilisateur
class Profil (models.Model):
    DEVIS_CHOICES = [("Ar", "Ar"),
                     ("USD", "USD"),
                     ("EUR", "EUR")]
    nom = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profil")
    photo_de_profil = ResizedImageField(upload_to=upload_to,
                                                      quality=100,
                                                      force_format='PNG',
                                                      null=True,
                                                      blank=True,
                                                      size=[500,500],
                                                      crop=["middle", "center"],
                                        )
    pays = CountryField(null=True, blank=True)
    devise = models.CharField(max_length=50, choices=DEVIS_CHOICES, default="Ar")
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nom


class Artiste (models.Model):
    nom = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_artiste", null=True, blank=True)
    photo_de_profil = ResizedImageField(upload_to=upload_to,
                                                      quality=100,
                                                      force_format='PNG',
                                                      null=True,
                                                      blank=True,
                                                      size=[500,500],
                                                      crop=["middle", "center"],
                                        )
    photo_de_couverture = ResizedImageField(upload_to=upload_to,
                                                      quality=100,
                                                      force_format='PNG',
                                                      null=True,
                                                      blank=True,
                                                      size=[1920,1080],
                                                      crop=["middle", "center"],
                                        )
    youtube = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    en_ligne = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super(Artiste, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Organisateur (models.Model):
    nom = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_organisateur", null=True, blank=True)
    photo_de_profil = ResizedImageField(upload_to=upload_to,
                                                      quality=100,
                                                      force_format='PNG',
                                                      null=True,
                                                      blank=True,
                                                      size=[500,500],
                                                      crop=["middle", "center"],
                                        )
    photo_de_couverture = ResizedImageField(upload_to=upload_to,
                                                      quality=100,
                                                      force_format='PNG',
                                                      null=True,
                                                      blank=True,
                                                      size=[1920,1080],
                                                      crop=["middle", "center"],
                                        )
    is_association = models.BooleanField(default=False)
    siteweb = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    en_ligne = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super(Organisateur, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Association (models.Model):
    nom = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_association" , null=True, blank=True)
    photo_de_profil = ResizedImageField(upload_to=upload_to,
                                                      quality=100,
                                                      force_format='PNG',
                                                      null=True,
                                                      blank=True,
                                                      size=[500,500],
                                                      crop=["middle", "center"],
                                        )
    photo_de_couverture = ResizedImageField(upload_to=upload_to,
                                                      quality=100,
                                                      force_format='PNG',
                                                      null=True,
                                                      blank=True,
                                                      size=[1920,1080],
                                                      crop=["middle", "center"],
                                        )
    siteweb = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    en_ligne = models.BooleanField(default=False)
    lien_don = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super(Association, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Action (models.Model):
    TYPE_CHOICES = [("Sociale", "Sociale"),
                    ("Environnementale", "Environnementale")]
    titre = models.CharField(max_length=200, unique=True)
    description_courte = models.TextField()
    description_longue = models.TextField()
    photo_de_couverture = ResizedImageField(upload_to=upload_to,
                                                      quality=100,
                                                      force_format='PNG',
                                                      null=True,
                                                      blank=True,
                                                      size=[1920,1080],
                                                      crop=["middle", "center"],
                                        )
    association = models.ForeignKey(Association, on_delete=models.CASCADE, related_name="association_action")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    youtube = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    siteweb = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    en_ligne = models.BooleanField(default=False)
    lien_don = models.URLField(null=True, blank=True)
    lien_details = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super(Action, self).save(*args, **kwargs)

    def __str__(self):
        return self.titre


class Live (models.Model):
    titre = models.CharField(max_length=200)
    en_ligne = models.BooleanField(default=False)
    date = models.DateField(null=True, blank=True)
    heure = models.TimeField(null=True, blank=True)
    debut = models.BooleanField(default=False)

    def __str__(self):
        return self.titre


class Video (models.Model):
    titre = models.CharField(max_length=200, unique=True)
    artiste = models.ForeignKey(Artiste, on_delete=models.SET_NULL, related_name="artiste_video", null=True, blank=True)
    artistes = models.ManyToManyField(Artiste, related_name="artistes_video")
    organisateur = models.ForeignKey(Organisateur, on_delete=models.CASCADE, related_name="organisateur_video", null=True, blank=True)
    levee_de_fond = models.BooleanField(default=False)
    gratuit = models.BooleanField(default=False)
    duree = models.CharField(max_length=200, null=True, blank=True)
    description_courte = models.TextField()
    description_longue = models.TextField()
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="action_video", null=True, blank=True)
    tarif_ariary = models.PositiveIntegerField(null=True, blank=True)
    tarif_dollar = models.FloatField(null=True, blank=True)
    tarif_euro = models.FloatField(null=True, blank=True)
    date_sortie = models.DateField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    a_la_une  = models.BooleanField(default=False)
    photo_de_couverture = ResizedImageField(upload_to=upload_to,
                                                      quality=100,
                                                      force_format='PNG',
                                                      null=True,
                                                      blank=True,
                                                      size=[1920,1080],
                                                      crop=["middle", "center"],
                                        )
    lien_video = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    en_ligne = models.BooleanField(default=False)
    stripe_price_id = models.CharField(null=True, blank=True, max_length=150)
    is_live = models.BooleanField(default=False)
    live = models.ForeignKey(Live, on_delete=models.CASCADE, related_name="live_video", null=True, blank=True)
    is_film = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.titre


class Contrat (models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_contrat")
    description = models.TextField()
    sehatra = models.PositiveIntegerField()
    organisateur = models.PositiveIntegerField(null=True, blank=True)
    action = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return "Contrat {}".format(self.video.titre)


class Actualite (models.Model):
    titre = models.CharField(max_length=200, unique=True)
    description_courte = models.TextField()
    description_longue = models.TextField()
    photo_de_couverture = ResizedImageField(upload_to=upload_to,
                                                      quality=100,
                                                      force_format='PNG',
                                                      null=True,
                                                      blank=True,
                                                      size=[1920,1080],
                                                      crop=["middle", "center"],
                                        )
    date = models.DateField()
    youtube = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    siteweb = models.URLField(null=True, blank=True)
    en_ligne = models.BooleanField(default=False)

    def __str__(self):
        return self.titre


class Vue(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_vue")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_vue")
    date = models.DateTimeField(auto_now=True)


class Test (models.Model):
    video = models.URLField()
    type = models.CharField(max_length=100, null=True, blank=True)