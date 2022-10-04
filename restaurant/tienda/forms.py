from django import forms
from .models import Mesa

class MesaCreationForm(forms.ModelForm):
	class Meta:
		model = Mesa
		fields = ['cantidad_personas','disponibilidad'] #parametros de la clase a crear, no está la ID ya que es automatica

class QrMesaForm(forms.Form):
	id_mesa = forms.CharField()