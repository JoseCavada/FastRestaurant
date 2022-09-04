from django import forms
from .models import Mesa, Insumo

class MesaCreationForm(forms.ModelForm):
	id_mesa = 0
	class Meta:
		model = Mesa
		fields = ('cantidad_personas','disponibilidad')

class InsumoCreationForm(forms.ModelForm):
	id_insumo = 0
	class Meta:
		model = Insumo
		fields = ('nombre', 'cantidad')