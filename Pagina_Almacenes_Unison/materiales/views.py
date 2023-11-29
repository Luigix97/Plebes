from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView, DetailView, TemplateView, View

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
    
class AgregarAlCarritoView(View):
    def post(self, request, pk):
        # Obtén el material
        material = get_object_or_404(Material, pk=pk)

        # Filtra los objetos Carrito para el usuario y el material especificados que no estén confirmados
        carrito_items = Carrito.objects.filter(usuario=request.user, material=material, confirmado=False)

        # Verifica si hay algún objeto Carrito que cumpla con los criterios
        if carrito_items.exists():
            # Si hay al menos uno, toma el primero
            carrito_item = carrito_items.first()
        else:
            # Si no hay ninguno, crea uno nuevo
            carrito_item = Carrito(usuario=request.user, material=material, confirmado=False, cantidad=0)

        carrito_item.cantidad += 1  # O ajusta según tus necesidades
        carrito_item.save()

        # Mensaje de éxito
        return HttpResponseRedirect(reverse_lazy('lista_materiales') + '?taken=true')
    
    
def confirmar_pedido(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)

    for item in carrito_items:
        if not item.verificar_disponibilidad():
            # Aquí puedes manejar el error, por ejemplo, redireccionar a una página de error.
            return render(request, 'materiales/error_disponibilidad.html')

        # Reducir la cantidad en el modelo Material
        item.material.cantidad -= item.cantidad
        item.material.save()

    # Marcar los elementos del carrito como confirmados
    carrito_items.update(confirmado=True)

    return redirect('ver_carrito')
    
def ver_carrito(request):
    carrito_items = Carrito.objects.filter(usuario=request.user, confirmado=False)
    total_items = carrito_items.count()

    context = {
        'carrito_items': carrito_items,
        'total_items': total_items,
    }

    return render(request, 'materiales/ver_carrito.html', context)  

def eliminar_del_carrito(request, pk):
    item = Carrito.objects.get(pk=pk)
    item.delete()
    return redirect('ver_carrito')

def borrar_carrito(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)
    carrito_items.delete()
    return redirect('ver_carrito')