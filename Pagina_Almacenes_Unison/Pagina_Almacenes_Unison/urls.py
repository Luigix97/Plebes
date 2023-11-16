"""Pagina_Almacenes_Unison URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from .views import *
from usuarios.views import *
from materiales.views import *
from reportes.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/',login_required(Portal.as_view()), name='portal'),
    path('', RedirectView.as_view(url='portal/')),
]

urlpatterns += [
    path('iniciar-sesion/', InicioSesionView.as_view(), name='inicio_sesion'),
    path('crear-usuario/', CrearUsuario.as_view(), name='crear_usuario'),
    path('cerrar-sesion/', CerrarSesionView.as_view(), name='cerrar_sesion'),   
]

urlpatterns += [
    path('lista-materiales/', login_required(ListaMateriales.as_view()), name='lista_materiales'),
    path('gastos/', login_required(ListaGastos.as_view()), name='lista_gastos'),
    path('añadir-material/', login_required(AñadirMaterial.as_view()), name='añadir_material'),
    path('agregar-material/<int:pk>/', login_required(AgregarProducto.as_view()), name='agregar_material'),
    path('editar-material/<int:pk>/', login_required(EditarMaterial.as_view()), name='editar_material'),
    path('tomar-material/<int:pk>/', login_required(TomarProducto.as_view()), name='tomar_producto'),
    path('eliminar-material/<int:pk>/', login_required(EliminarMaterial.as_view()), name = 'eliminar_material'),
]

urlpatterns += [
    path('lista-reportes/', login_required(ListaReportes.as_view()), name='lista_reportes'),
    path('añadir-reporte/', login_required(CrearReporte.as_view()), name='hacer_reporte'),
    path('eliminar-reporte/<int:pk>/', login_required(EliminarReporte.as_view()), name = 'eliminar_reporte'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]
