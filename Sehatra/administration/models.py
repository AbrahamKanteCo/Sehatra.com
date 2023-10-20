# models.py
import datetime
import os
from django.db import models
import unicodedata
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django_countries.fields import CountryField
from django.utils.text import slugify
import uuid

from plateforme.models import Video


# def custom_upload_path(instance, filename):
#     base_filename, file_extension = os.path.splitext(filename)
#     timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#     new_filename = f"{timestamp}_{base_filename}{file_extension}"
#     return f'{new_filename}'


# def remove_accents(input_str):
#     return ''.join((c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn'))


# def upload_to (instance, filename):
#     upload = instance.__class__.__name__.lower() + "/" + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
#     filename = remove_accents(filename)
#     return os.path.join(upload, filename)


# #profil utilisateur
# class Profil (models.Model):
#     DEVIS_CHOICES = [("Ar", "Ar"),
#                      ("USD", "USD"),
#                      ("EUR", "EUR")]
#     nom = models.CharField(max_length=200)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profil")
#     photo_de_profil = ResizedImageField(upload_to=upload_to,
#                                                       quality=100,
#                                                       force_format='PNG',
#                                                       null=True,
#                                                       blank=True,
#                                                       size=[500,500],
#                                                       crop=["middle", "center"],
#                                         )
#     pays = CountryField(null=True, blank=True)
#     devise = models.CharField(max_length=50, choices=DEVIS_CHOICES, default="Ar")
#     age = models.PositiveIntegerField(null=True, blank=True)
#     class Meta:
#         db_table = 'Profil'

#     def __str__(self):
#         return self.nom


# class Artiste (models.Model):
#     nom = models.CharField(max_length=200)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_artiste", null=True, blank=True)
#     photo_de_profil = ResizedImageField(upload_to=upload_to,
#                                                       quality=100,
#                                                       force_format='PNG',
#                                                       null=True,
#                                                       blank=True,
#                                                       size=[500,500],
#                                                       crop=["middle", "center"],
#                                         )
#     photo_de_couverture = ResizedImageField(upload_to=upload_to,
#                                                       quality=100,
#                                                       force_format='PNG',
#                                                       null=True,
#                                                       blank=True,
#                                                       size=[1920,1080],
#                                                       crop=["middle", "center"],
#                                         )
#     youtube = models.URLField(null=True, blank=True)
#     slug = models.SlugField(unique=True, null=True, blank=True)
#     en_ligne = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.nom)
#         super(Artiste, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.nom
#     class Meta:
#         db_table = 'Artiste'


# class Organisateur (models.Model):
#     nom = models.CharField(max_length=200, unique=True)
#     description = models.TextField(null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_organisateur", null=True, blank=True)
#     photo_de_profil = ResizedImageField(upload_to=upload_to,
#                                                       quality=100,
#                                                       force_format='PNG',
#                                                       null=True,
#                                                       blank=True,
#                                                       size=[500,500],
#                                                       crop=["middle", "center"],
#                                         )
#     photo_de_couverture = ResizedImageField(upload_to=upload_to,
#                                                       quality=100,
#                                                       force_format='PNG',
#                                                       null=True,
#                                                       blank=True,
#                                                       size=[1920,1080],
#                                                       crop=["middle", "center"],
#                                         )
#     is_association = models.BooleanField(default=False)
#     siteweb = models.URLField(null=True, blank=True)
#     facebook = models.URLField(null=True, blank=True)
#     youtube = models.URLField(null=True, blank=True)
#     slug = models.SlugField(unique=True, null=True, blank=True)
#     en_ligne = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.nom)
#         super(Organisateur, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.nom
#     class Meta:
#         db_table = 'Organisateur'


# class Association (models.Model):
#     nom = models.CharField(max_length=200, unique=True)
#     description = models.TextField(null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_association" , null=True, blank=True)
#     photo_de_profil = ResizedImageField(upload_to=upload_to,
#                                                       quality=100,
#                                                       force_format='PNG',
#                                                       null=True,
#                                                       blank=True,
#                                                       size=[500,500],
#                                                       crop=["middle", "center"],
#                                         )
#     photo_de_couverture = ResizedImageField(upload_to=upload_to,
#                                                       quality=100,
#                                                       force_format='PNG',
#                                                       null=True,
#                                                       blank=True,
#                                                       size=[1920,1080],
#                                                       crop=["middle", "center"],
#                                         )
#     siteweb = models.URLField(null=True, blank=True)
#     facebook = models.URLField(null=True, blank=True)
#     youtube = models.URLField(null=True, blank=True)
#     slug = models.SlugField(unique=True, null=True, blank=True)
#     en_ligne = models.BooleanField(default=False)
#     lien_don = models.URLField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.nom)
#         super(Association, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.nom
#     class Meta:
#         db_table = 'Association'


# class Action (models.Model):
#     TYPE_CHOICES = [("Sociale", "Sociale"),
#                     ("Environnementale", "Environnementale")]
#     titre = models.CharField(max_length=200, unique=True)
#     description_courte = models.TextField()
#     description_longue = models.TextField()
#     photo_de_couverture = ResizedImageField(upload_to=upload_to,
#                                                       quality=100,
#                                                       force_format='PNG',
#                                                       null=True,
#                                                       blank=True,
#                                                       size=[1920,1080],
#                                                       crop=["middle", "center"],
#                                         )
#     association = models.ForeignKey(Association, on_delete=models.CASCADE, related_name="association_action")
#     type = models.CharField(max_length=50, choices=TYPE_CHOICES)
#     youtube = models.URLField(null=True, blank=True)
#     facebook = models.URLField(null=True, blank=True)
#     siteweb = models.URLField(null=True, blank=True)
#     slug = models.SlugField(unique=True, null=True, blank=True)
#     en_ligne = models.BooleanField(default=False)
#     lien_don = models.URLField(null=True, blank=True)
#     lien_details = models.URLField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.titre)
#         super(Action, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.titre
#     class Meta:
#         db_table = 'Action'


# class Live (models.Model):
#     titre = models.CharField(max_length=200)
#     en_ligne = models.BooleanField(default=False)
#     date = models.DateField(null=True, blank=True)
#     heure = models.TimeField(null=True, blank=True)
#     debut = models.BooleanField(default=False)

#     def __str__(self):
#         return self.titre

#     class Meta:
#         db_table = 'Live'


# class Video (models.Model):
#     titre = models.CharField(max_length=200, unique=True)
#     artiste = models.ForeignKey(Artiste, on_delete=models.SET_NULL, related_name="artiste_video", null=True, blank=True)
#     artistes = models.ManyToManyField(Artiste, related_name="artistes_video")
#     organisateur = models.ForeignKey(Organisateur, on_delete=models.CASCADE, related_name="organisateur_video", null=True, blank=True)
#     levee_de_fond = models.BooleanField(default=False)
#     gratuit = models.BooleanField(default=False)
#     duree = models.CharField(max_length=200, null=True, blank=True)
#     description_courte = models.TextField()
#     description_longue = models.TextField()
#     action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="action_video", null=True, blank=True)
#     tarif_ariary = models.PositiveIntegerField(null=True, blank=True)
#     tarif_dollar = models.FloatField(null=True, blank=True)
#     tarif_euro = models.FloatField(null=True, blank=True)
#     date_sortie = models.DateField(null=True, blank=True)
#     youtube = models.URLField(null=True, blank=True)
#     a_la_une  = models.BooleanField(default=False)
#     photo_de_couverture = ResizedImageField(upload_to=upload_to,
#                                                       quality=100,
#                                                       force_format='PNG',
#                                                       null=True,
#                                                       blank=True,
#                                                       size=[1920,1080],
#                                                       crop=["middle", "center"],
#                                         )
#     lien_video = models.URLField(null=True, blank=True)
#     slug = models.SlugField(unique=True, null=True, blank=True)
#     en_ligne = models.BooleanField(default=False)
#     stripe_price_id = models.CharField(null=True, blank=True, max_length=150)
#     is_live = models.BooleanField(default=False)
#     live = models.ForeignKey(Live, on_delete=models.CASCADE, related_name="live_video", null=True, blank=True)
#     is_film = models.BooleanField(default=False)


#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.titre)
#         super(Video, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.titre
#     class Meta:
#         db_table = 'Video'

class Video_facebook(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="liens_facebook")
    facebook = models.URLField()
    date_publication=models.DateTimeField()

# class Contrat (models.Model):
#     video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_contrat")
#     description = models.TextField()
#     sehatra = models.PositiveIntegerField()
#     organisateur = models.PositiveIntegerField(null=True, blank=True)
#     action = models.PositiveIntegerField(null=True, blank=True)

#     def __str__(self):
#         return "Contrat {}".format(self.video.titre)
#     class Meta:
#         db_table = 'Contrat'


# class Actualite (models.Model):
#     titre = models.CharField(max_length=200, unique=True)
#     description_courte = models.TextField()
#     description_longue = models.TextField()
#     photo_de_couverture = ResizedImageField(upload_to=upload_to,
#                                                       quality=100,
#                                                       force_format='PNG',
#                                                       null=True,
#                                                       blank=True,
#                                                       size=[1920,1080],
#                                                       crop=["middle", "center"],
#                                         )
#     date = models.DateField()
#     youtube = models.URLField(null=True, blank=True)
#     facebook = models.URLField(null=True, blank=True)
#     siteweb = models.URLField(null=True, blank=True)
#     en_ligne = models.BooleanField(default=False)

#     def __str__(self):
#         return self.titre
#     class Meta:
#         db_table = 'Actualite'


# class Vue(models.Model):
#     video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_vue")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_vue")
#     date = models.DateTimeField(auto_now=True)
#     class Meta:
#         db_table = 'Vue'


# class Test (models.Model):
#     video = models.URLField()
#     type = models.CharField(max_length=100, null=True, blank=True)
#     class Meta:
#         db_table = 'Test'

# class Billet (models.Model):
#     video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, related_name="video_billet")
#     date = models.DateTimeField(auto_now=True)
#     valide = models.BooleanField(default=False)
#     gratuit = models.BooleanField(default=False)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="utilisateur_billet",db_column="user")
#     slug = models.CharField(max_length=50, unique=True, null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             while True:
#                 try:
#                     self.slug = uuid.uuid4().hex[:8].upper()
#                     super(Billet, self).save(*args, **kwargs)
#                     break
#                 except:
#                     pass
#         else:
#             super(Billet, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.slug
#     class Meta:
#         db_table = 'Billet'


# class ModePaiement (models.Model):
#     nom = models.CharField(max_length=50)

#     def __str__(self):
#         return self.nom
#     class Meta:
#         db_table = 'Modepaiement'


# class Paiement (models.Model):
#     billet = models.ForeignKey(Billet, on_delete=models.CASCADE, related_name="billet_paiement",db_column="billet")
#     mode = models.ForeignKey(ModePaiement, on_delete=models.CASCADE, related_name="mode_paiement",db_column="mode")
#     valide = models.BooleanField(default=False)
#     telephone = models.CharField(null=True, blank=True, max_length=150)
#     date = models.DateTimeField(auto_now=True)
#     token = models.TextField(null=True)
#     notif_token = models.TextField(null=True)
#     class Meta:
#         db_table = 'Paiement'
    
#     def calculer_paiement(paiements):
#         somme = 0
#         cours_euro = 4700

#         for paiement in paiements:
#             if paiement.mode == 2:
#                 somme += paiement.billet.video.tarif_euro * cours_euro
#             else:
#                 somme += paiement.billet.video.tarif_ariary
        
#         return somme

class NotificationFCM(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    destination_url = models.URLField()
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="utilisateur_notification",db_column="user")

    def __str__(self):
        return self.title
    def mark_as_read(self):
        self.is_read = True
        self.save() 

class VenteParPays(models.Model):
    slug = models.CharField(max_length=50,unique=True)
    pays = models.TextField()
    date_vente = models.DateTimeField()
    codepays = models.TextField(max_length=2)


class PageAnalytics(models.Model):
    path = models.CharField(max_length=50)
    screenname = models.TextField()
    utilisateur =models.PositiveIntegerField(null=True, blank=True)
    bouncerate = models.PositiveIntegerField(null=True, blank=True)
    temps_moyenne = models.PositiveIntegerField(null=True, blank=True)
    nouveauutilisateur=models.PositiveIntegerField(null=True, blank=True)
    vue=models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField()

