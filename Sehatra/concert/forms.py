from django import forms
from django.forms import ModelForm
from .models import FormulaireReclamation


class FormulaireProCreateForm(ModelForm):
    class Meta:
        model = FormulaireReclamation
        fields = ["motif", 'message']
