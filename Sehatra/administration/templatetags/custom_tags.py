from django import template
from django.conf import settings
import os

register = template.Library()

@register.filter
def file_exists(filepath):
    return os.path.exists(os.path.join(settings.MEDIA_ROOT, filepath))
