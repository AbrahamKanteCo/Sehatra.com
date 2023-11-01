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

from plateforme.models import Organisateur, Video

def is_artist(self):
        if self.is_authenticated:
            try:
                artiste = Organisateur.objects.get(user=self, en_ligne=True)
                return True
            except Organisateur.DoesNotExist:
                return False
        return False

User.add_to_class("is_artist", is_artist)
class Video_facebook(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="liens_facebook")
    facebook = models.URLField()
    date_publication=models.DateTimeField()

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
    codepays = models.TextField(max_length=2,null=True)


class PageAnalytics(models.Model):
    path = models.CharField(max_length=50)
    screenname = models.TextField()
    utilisateur =models.PositiveIntegerField(null=True, blank=True)
    bouncerate = models.PositiveIntegerField(null=True, blank=True)
    temps_moyenne = models.PositiveIntegerField(null=True, blank=True)
    nouveauutilisateur=models.PositiveIntegerField(null=True, blank=True)
    vue=models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField()

