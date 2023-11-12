from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from .models import Reporte
from .forms import FormularioReporte

class ListaReportes(ListView):
    model = Reporte
    template_name = 'reportes/lista_reportes.html'
    context_object_name = 'reportes'
    
class CrearReporte(CreateView):
    model = Reporte
    form_class = FormularioReporte
    template_name = 'reportes/hacer_reporte.html'
    succes_url = reverse_lazy('lista_reportes')
    
    def post(self,request,*args,**kwargs):
        form = FormularioReporte(request.POST)
        if form.is_valid():
            reporte = form.save(commit = False)
            reporte.solicitante = request.user
            reporte.save()
            return HttpResponseRedirect(reverse_lazy("lista_reportes"))

        else:
            form = FormularioReporte()
            return render(request, 'reportes/hacer_reporte', {'form':form})
        
class EliminarReporte(DeleteView):
    model = Reporte
    success_url = reverse_lazy('lista_reportes')
    template_name = 'confirmar_eliminar.html'

