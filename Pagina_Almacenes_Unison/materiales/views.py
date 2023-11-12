from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView

from .models import Gasto, Material
from reportes.models import Reporte
from .forms import FormularioAgregarProducto, FormularioMaterial, FormularioTomarProducto

class ListaMateriales(ListView):
    model = Material
    template_name = 'materiales/lista_material.html'
    context_object_name = 'materiales'

    
class AñadirMaterial(CreateView):
    model = Material
    form_class = FormularioMaterial
    template_name = 'materiales/añadir_material.html'
    succes_url = reverse_lazy('lista_materiales')
    
    def post(self,request,*args,**kwargs):
        form = FormularioMaterial(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit = False)
            material.save()
            
            Gasto.objects.create(producto=material, cantidad= material.cantidad, gasto=(material.precio_unitario * material.cantidad))
            return HttpResponseRedirect(reverse_lazy("lista_materiales"))
                

        else:
            form = FormularioMaterial(request.POST, request.FILES)
            return render(request, 'materiales/añadir_material.html', {'form':form})

class EditarMaterial(UpdateView):
    model = Material
    template_name = 'materiales/editar_material.html'
    form_class = FormularioMaterial
    success_url = reverse_lazy('lista_materiales')

class AgregarProducto(FormView):
    template_name = 'materiales/agregar_producto.html'
    form_class = FormularioAgregarProducto
    success_url = reverse_lazy('lista_materiales')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['material'] = get_object_or_404(Material, pk=self.kwargs['pk'])
        return context
        
    
    def form_valid(self, form):
        material = get_object_or_404(Material, pk=self.kwargs['pk'])

        # Obtén la cantidad deseada del formulario
        cantidad = form.cleaned_data['cantidad_a_agregar']

        # Crea el gasto hecho por el producto agregado
        Gasto.objects.create(producto=material, cantidad=cantidad, gasto=(cantidad*material.precio_unitario))
        
        # Checa si había reporte, si había lo pone "completado" por agregar cantidad suficiente
        if material.cantidad + cantidad >= material.umbral:
            Reporte.objects.filter(producto=material).update(estado='Completado')
            
                
        # Realiza la operación de resta
        material.cantidad += cantidad
        material.save()
            
        return super().form_valid(form)

         
class TomarProducto(FormView):
    template_name = 'materiales/tomar_producto.html'
    form_class = FormularioTomarProducto
    success_url = reverse_lazy('lista_materiales')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['material'] = get_object_or_404(Material, pk=self.kwargs['pk'])
        return context
        
    
    def form_valid(self, form):
        material = get_object_or_404(Material, pk=self.kwargs['pk'])

        # Obtén la cantidad deseada del formulario
        cantidad_deseada = form.cleaned_data['cantidad_a_tomar']

        # Verifica si la cantidad deseada es menor o igual a la cantidad disponible
        if cantidad_deseada <= material.cantidad:
            # Realiza la operación de resta
            material.cantidad -= cantidad_deseada
            material.save()

            if material.cantidad <= material.umbral:
                # Esto hace un reporte/solicitud cuando la cantidad del artículo baja del umbral establecido al principio
                Reporte.objects.create(
                    solicitante =self.request.user,
                    producto = material,
                    cantidad = cantidad_deseada, # Esto hace que se solicite la misma cantidad que se tomó, pueden poner otra cantidad ustedes sis gustan
                    descripcion = 'Quedan pocos artículos',
                )
            return super().form_valid(form)
        else:
            # Si la cantidad deseada es mayor, muestra un mensaje de error
            form.add_error('cantidad_a_tomar', 'La cantidad deseada es mayor a la cantidad disponible.')
            return self.form_invalid(form)

    
    
class EliminarMaterial(DeleteView):
    model = Material
    success_url = reverse_lazy('lista_materiales')
    template_name = 'confirmar_eliminar.html'
        
class ListaGastos(ListView):
    model = Gasto
    template_name = 'materiales/lista_gastos.html'
    context_object_name = 'gastos'
    