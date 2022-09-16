from django.urls import path 
from . import views
from .views import UsuarioListar, UsuarioDetalle

urlpatterns=[
	path('listar', UsuarioListar.as_view(template_name = "registration/UsuarioListar.html"), name = 'listar_usuario'),
	path('detalle/<int:pk>', UsuarioDetalle.as_view(template_name = "registration/UsuarioDetalle.html"), name = 'detalle_usuario')
]