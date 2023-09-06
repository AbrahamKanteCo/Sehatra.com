from django.views.generic import TemplateView, FormView, CreateView
from ..models import Test
from django.shortcuts import redirect
from paiement.models import Billet


class TestView(TemplateView):
    template_name = "test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url"] = Test.objects.all()[0].video
        context['type'] = Test.objects.all()[0].type
        return context

    def dispatch(self, request, *args, **kwargs):
        if len (Billet.objects.filter(user=request.user, video__slug="tamberina-an-kira", valide=True)) == 0:
            return redirect('accueil')

        return super().dispatch(request, *args, **kwargs)
