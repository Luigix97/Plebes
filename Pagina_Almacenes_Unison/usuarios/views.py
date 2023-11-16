from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static



from .models import *
from .forms import *
# Create your views here.

class CrearUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'crear_usuario.html'
    url_redirect = reverse_lazy('inicio_sesion')

    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse_lazy("inicio_sesion"))
        else:
            return render(request, self.template_name, context={'form': form})


# Iniciar Sesión
class InicioSesionView(LoginView):
    template_name = 'iniciar_sesion.html'
    authentication_form = FormularioLogin
    next_page = reverse_lazy('portal')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('portal'))

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request,form.get_user())
        return super(InicioSesionView,self).form_valid(form)

class CerrarSesionView(LogoutView):
    next_page = reverse_lazy ('portal')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)