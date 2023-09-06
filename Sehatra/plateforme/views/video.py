from django.views.generic.detail import DetailView
from ..models import Video
from paiement.models import Billet
from django.views.generic.list import ListView
from django.shortcuts import redirect


class VideoListView(ListView):
    model = Video
    template_name = "video_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Vidéo Sehatra.com - Plateforme de vidéo Vita Malagasy"
        context["image"] = "https://sehatra.com/static/images/couverture.png"
        return context

    def get_queryset(self):
        return Video.objects.filter(en_ligne=True)


class VideoDetailView(DetailView):
    model = Video
    template_name = "video_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['billet'] = False
        if self.request.user.is_authenticated:
            billets = Billet.objects.filter(video=context['object'], user=self.request.user)
            if len(billets) > 0:
                for billet in billets:
                    if billet.valide:
                        context['billet'] = True
        context["title"] = "{} - Sehatra.com ".format(context['object'].titre)
        context["image"] = context['object'].photo_de_couverture.url
        return context


class VideoPlayerView(DetailView):
    model = Video
    template_name = "video_watch.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            Billet.objects.get(user=self.request.user, video=context['object'], valide=True)
        except Billet.DoesNotExist:
            redirect("/video/{}".format(context['object.slug']))
        except Billet.MultipleObjectsReturned:
            pass
        context["title"] = ""
        context["image"] = context['object'].photo_de_couverture.url
        return context


class VideoPlayerTestView(DetailView):
    model = Video
    template_name = "video_watch.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            Billet.objects.get(user=self.request.user, video=context['object'], valide=True)
        except Billet.DoesNotExist:
            redirect("/video/{}".format(context['object.slug']))
        except Billet.MultipleObjectsReturned:
            pass
        context["title"] = ""
        context["image"] = context['object'].photo_de_couverture.url
        return context
