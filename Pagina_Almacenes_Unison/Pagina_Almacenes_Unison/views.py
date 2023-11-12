from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import TemplateView

class Portal(TemplateView):
    template_name = 'portal.html'  # Ruta relativa a la plantilla en tu directorio de plantillas
