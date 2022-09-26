from django import forms
from .models import Plato, Insumo

class PlatoCreationForm(forms.ModelForm):
	id_plato = 0
	class Meta:
		model = Plato
		fields = ["nombre","descripcion","precio","disponibilidad","imagen_producto","ingredientes",] #parametros de la clase a crear, no está la ID ya que es automatica

class PlatoCrearForm(forms.Form):
	id_plato = 0
	ingredientes = forms.ModelMultipleChoiceField(Insumo.objects.all())
	class Meta:
		model = Plato
		fields = ["nombre","descripcion","precio","disponibilidad","imagen_producto"] #parametros de la clase a crear, no está la ID ya que es automatica
