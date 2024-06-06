# serializers.py
from rest_framework import serializers
from .models import Video_facebook
from plateforme.models import Action, Association, Live, Organisateur, Artiste, Video
from django.contrib.auth.models import User


class VideoArtisteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__' 

class ArtisteMobileSerializer(serializers.ModelSerializer):
    video_user = VideoArtisteSerializer(many=True, read_only=True) 
    class Meta:
        model = Artiste
        fields = ('nom', 'photo_de_profil', 'photo_de_couverture', 'youtube', 'slug', 'en_ligne', 'video_user')

class OrganisateurMobileSerializer(serializers.ModelSerializer):
    video_user = VideoArtisteSerializer(many=True, read_only=True) 
    class Meta:
        model = Organisateur
        fields = ('nom', 'photo_de_profil', 'description', 'video_user')
        
class AssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = '__all__'
    

class AssociationMobileSerializer(serializers.ModelSerializer):
    video_user = AssociationSerializer(many=True, read_only=True) 
    class Meta:
        model = Organisateur
        fields = ('nom', 'photo_de_profil', 'description', 'video_user')


class ArtisteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artiste
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = '__all__'

class OrganisteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisateur
        fields = '__all__'

class OrganisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisateur
        fields = ('id', 'nom') 

class VideoSerializer(serializers.ModelSerializer):
    organisateur_detail = OrganisateurSerializer(source='organisateur', read_only=True)
    
    class Meta:
        model = Video
        fields = '__all__'  
        extra_fields = ['organisateur_detail']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(VideoSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video_facebook
        fields = '__all__'