from django import forms
from .models import Mesa, DetallePedidoPlato

class MesaCreationForm(forms.ModelForm):
	class Meta:
		model = Mesa
		fields = ['cantidad_personas','disponibilidad'] #parametros de la clase a crear, no está la ID ya que es automatica

class QrMesaForm(forms.Form):
	id_mesa = forms.CharField()

class DetallePedidoPlatoForm(forms.ModelForm):
	class Meta:
		model = DetallePedidoPlato
		fields = ['id_pedido','id_plato','cantidad', 'estado','puntuacion']

class EditarPlatoPedidoForm(forms.Form):
	cantidad = forms.IntegerField()