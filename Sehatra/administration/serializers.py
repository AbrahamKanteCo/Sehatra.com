# serializers.py
from rest_framework import serializers
from plateforme.models import Association, Live, Organisateur, Artiste, Video
from django.contrib.auth.models import User


class ArtisteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artiste
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class AssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = '__all__'
    
class LiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = '__all__'

class OrganisteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisateur
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

