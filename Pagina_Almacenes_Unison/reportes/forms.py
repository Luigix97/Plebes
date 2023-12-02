from django import forms

from .models import *

class FormularioReporte(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['producto', 'descripcion', 'cantidad',]
        