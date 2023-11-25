from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView, DetailView, TemplateView

from .models import Gasto, Material, Carrito
from reportes.models import Reporte
from .forms import FormularioAgregarProducto, FormularioMaterial, FormularioTomarProducto, FormularioAgregarAlCarrito

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

class AgregarProducto(LoginRequiredMixin, FormView):
    template_name = 'materiales/agregar_producto.html'
    form_class = FormularioAgregarAlCarrito
    success_url = reverse_lazy('lista_materiales')

    def form_valid(self, form):
        material = get_object_or_404(Material, pk=self.kwargs['pk'])
        cantidad = form.cleaned_data['cantidad']

        # Añadir el producto al carrito
        carrito, created = Carrito.objects.get_or_create(usuario=self.request.user, material=material)
        carrito.cantidad += cantidad
        carrito.save()

        # Opcional: Puedes mostrar un mensaje de éxito o redirigir a la página del carrito
        return super().form_valid(form)
         
class TomarProductoView(TemplateView):  # Cambia a TemplateView para manejar solicitudes GET
    template_name = 'materiales/tomar_producto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material'] = get_object_or_404(Material, pk=self.kwargs['pk'])
        context['form'] = FormularioTomarProducto()
        return context

    def post(self, request, *args, **kwargs):
        form = FormularioTomarProducto(request.POST)
        if form.is_valid():
            material = get_object_or_404(Material, pk=self.kwargs['pk'])
            cantidad_deseada = form.cleaned_data['cantidad_a_tomar']

            if cantidad_deseada < 0:
                form.add_error('cantidad_a_tomar', 'La cantidad a tomar no puede ser negativa.')
                return self.render_to_response(self.get_context_data(form=form))

            if cantidad_deseada <= material.cantidad:
                material.cantidad -= cantidad_deseada
                material.save()

                if material.cantidad <= material.umbral:
                    Reporte.objects.create(
                        solicitante=self.request.user,
                        producto=material,
                        cantidad=cantidad_deseada,
                        descripcion='Quedan pocos artículos',
                    )
                return HttpResponseRedirect(reverse_lazy('lista_materiales') + '?taken=true')
            else:
                form.add_error('cantidad_a_tomar', 'La cantidad deseada es mayor a la cantidad disponible.')

        return self.render_to_response(self.get_context_data(form=form))
    
class EliminarMaterial(DeleteView):
    model = Material
    success_url = reverse_lazy('lista_materiales')
    template_name = 'confirmar_eliminar.html'
        
class ListaGastos(ListView):
    model = Gasto
    template_name = 'materiales/lista_gastos.html'
    context_object_name = 'gastos'
    
class VerProducto(DetailView):
    model = Material
    template_name = 'materiales/ver_producto.html'  # Cambia al nombre correcto de tu plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puedes agregar más contexto según sea necesario
        return context 
    
class VerCarrito(LoginRequiredMixin, TemplateView):
    template_name = 'materiales/ver_carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carrito'] = Carrito.objects.filter(usuario=self.request.user)
        return context

class ConfirmarPedido(TemplateView):
    template_name = 'materiales/confirmar_pedido.html'  # Ajusta el nombre según tu implementación