from django.urls import path 
from . import views
from .views import InsumoListado, InsumoCrear, InsumoDetalle, InsumoActualizar, InsumoEliminar
from .views import MesaListado, MesaCrear, MesaDetalle, MesaActualizar, MesaEliminar
from .views import PlatoListado, PlatoDetalle

urlpatterns=[
	path('',views.index, name = 'index'),
#urls de crud insumo
	path('insumo/listar', InsumoListado.as_view(template_name = "crud_insumo/ListarInsumo.html"), name='listar_insumo'),
	path('insumo/crear',InsumoCrear.as_view(template_name = "crud_insumo/CrearInsumo.html"), name='crear_insumo'),
	path('insumo/detalle/<int:pk>', InsumoDetalle.as_view(template_name = "crud_insumo/DetalleInsumo.html"), name = 'detalle_insumo'),
	path('insumo/editar/<int:pk>', InsumoActualizar.as_view(template_name = "crud_insumo/EditarInsumo.html"), name = 'editar_insumo'),
	path('insumo/eliminar/<int:pk>', InsumoEliminar.as_view(), name='eliminar_insumo'),
#urls crud mesa
	path('mesa/crear', MesaCrear.as_view(template_name = "crud_mesa/CrearMesa.html"), name = 'crear_mesa'),
	path('mesa/listar', MesaListado.as_view(template_name = "crud_mesa/ListarMesa.html"), name='listar_mesa'),
	#path('mesa/detalle/<int:pk>', MesaDetalle.as_view(template_name = "crud_mesa/DetalleMesa.html"), name = 'detalle_mesa'),
	path('mesa/editar/<int:pk>', MesaActualizar.as_view(template_name = "crud_mesa/EditarMesa.html"), name = 'editar_mesa'),
#urls crud plato
	path('plato/listar', PlatoListado.as_view(template_name = "crud_plato/ListarPlato.html"), name = 'listar_plato'),
	path('plato/detalle/<int:pk>', PlatoDetalle.as_view(template_name = "crud_plato/DetallePlato.html"), name = 'detalle_plato'),


]