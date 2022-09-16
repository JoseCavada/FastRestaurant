from django.urls import path 
from . import views
from .views import InsumoListado, InsumoCrear, InsumoDetalle, InsumoActualizar, InsumoEliminar

urlpatterns=[
	path('',views.index, name = 'index'),
	path('mesa', views.registrarMesa, name = 'registrarMesa'),
	path('insumo/listar', InsumoListado.as_view(template_name = "crud_insumo/ListarInsumo.html"), name='listar_insumo'),
	path('insumo/crear',InsumoCrear.as_view(template_name = "crud_insumo/CrearInsumo.html"), name='crear_insumo'),
	path('insumo/detalle/<int:pk>', InsumoDetalle.as_view(template_name = "crud_insumo/DetalleInsumo.html"), name = 'detalle_insumo'),
	path('insumo/editar/<int:pk>', InsumoActualizar.as_view(template_name = "crud_insumo/EditarInsumo.html"), name = 'editar_insumo'),
	path('insumo/eliminar/<int:pk>', InsumoEliminar.as_view(), name='eliminar_insumo'),
	#path('insumo', views.registrarInsumo, name = 'registrarInsumo')
]