from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Concert, Video


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['index' , 'politique', 'cgu']

    def location(self, item):
        return reverse(item)


class ConcertSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return Concert.objects.all()


class VideoSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return Video.objects.all()
