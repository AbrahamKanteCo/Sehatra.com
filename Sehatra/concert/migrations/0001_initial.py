# Generated by Django 3.1.7 on 2021-04-14 05:25

import concert.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artiste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Billet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('valide', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('jour', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=200)),
                ('mois', models.CharField(max_length=200)),
                ('heure', models.CharField(max_length=200)),
                ('tarif', models.CharField(max_length=200)),
                ('photo_de_couverture_large', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=100, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('photo_de_couverture_slider', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=100, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie1', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie2', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie3', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie4', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie5', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie6', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('lien_video', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('en_cours', models.BooleanField(default=False)),
                ('actif', models.BooleanField(default=True)),
                ('termine', models.BooleanField(default=False)),
                ('artiste', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='artiste_concert', to='concert.artiste')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('photo_de_couverture_large', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=100, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('photo_de_couverture_slider', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=100, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie1', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie2', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie3', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie4', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie5', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('galerie6', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, size=[1920, 1080], upload_to=concert.models.upload_to)),
                ('lien_video', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('acces_libre', models.BooleanField(default=True)),
                ('disponible', models.BooleanField(default=True)),
                ('artiste', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='artiste_video', to='concert.artiste')),
            ],
        ),
        migrations.CreateModel(
            name='VideoAccueil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=50)),
                ('video_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='video_accueil_1', to='concert.video')),
                ('video_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='video_accueil_2', to='concert.video')),
                ('video_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='video_accueil_3', to='concert.video')),
            ],
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('mode_de_paiement', models.CharField(choices=[('MVola', 'MVola'), ('Orange Money', 'Orange Money'), ('Moobi Pay', 'Moobi Pay'), ('Espèce', 'Espèce')], max_length=300)),
                ('token', models.CharField(blank=True, max_length=200, null=True)),
                ('valide', models.BooleanField(default=False)),
                ('billet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billet_concert', to='concert.billet')),
            ],
        ),
        migrations.CreateModel(
            name='LoggedInUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=32, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='logged_in_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConcertAccueil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=50)),
                ('concert_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='concert_accueil_1', to='concert.concert')),
                ('concert_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='concert_accueil_2', to='concert.concert')),
                ('concert_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='concert_accueil_3', to='concert.concert')),
            ],
        ),
        migrations.AddField(
            model_name='billet',
            name='concert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='concert_billet', to='concert.concert'),
        ),
        migrations.AddField(
            model_name='billet',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_billet', to=settings.AUTH_USER_MODEL),
        ),
    ]
