from django.shortcuts import render
from .forms import MesaCreationForm,InsumoCreationForm
from django.contrib import messages
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Insumo, Mesa
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin 
from django import forms

# Create your views here.
def index(request):
	return render(request,'index.html')
	


def registrarMesa(request):
	if request.method == "POST":
		form = MesaCreationForm(request.POST)
		if form.is_valid():
			messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = MesaCreationForm()
	return render (request=request, template_name="crear_mesa.html", context={"MesaCreationForm":form})

#CRUD Insumo ↓↓↓
class InsumoListado(ListView): 
    model = Insumo   
    paginate_by = 10 #Parametro para listar por páginas

class InsumoCrear(SuccessMessageMixin, CreateView): 
    model = Insumo
    form = Insumo
    fields = ["nombre","cantidad"] #parametros de la clase a crear, no está la ID ya que es automatica
    success_message = 'Insumo creado correctamente !' # Mostramos este Mensaje luego de Crear un Inumo
 
    # Redireccionamos a la página de listado luego de crear un registro de Insumo
    def get_success_url(self):
        success_message = 'Insumo Creado Correctamente !' # Mostramos este Mensaje luego de Crear un Insumo
        return reverse('listar_insumo') # Redireccionamos a la vista listar Insumo
 
class InsumoActualizar(SuccessMessageMixin, UpdateView): 
    model = Insumo
    form = Insumo
    fields = ["nombre","cantidad"]
    success_message = 'Insumo actualizado correctamente !' # Mostramos este Mensaje luego de Editar un Insumo
 
    # Redireccionamos a la página listado luego de actualizar un registro de Insumo
    def get_success_url(self):
        return reverse('listar_insumo') # Redireccionamos a la vista listar insumo

class InsumoDetalle(DetailView): 
    model = Insumo
 
class InsumoEliminar(SuccessMessageMixin, DeleteView): 
    model = Insumo 
    form = Insumo
    fields = "__all__"     
 
    # Redireccionamos a la página principal luego de eliminar un registro o postre
    def get_success_url(self): 
        success_message = 'Insumo eliminado correctamente !' # Mostramos este Mensaje luego de Editar un Postre 
        messages.success (self.request, (success_message))
        return reverse('listar_insumo')       
#CRUD insumo ↑↑↑

#CRUD mesa ↓↓↓
class MesaListado(ListView):
    model = Mesa
    paginated_by = 10

class MesaCrear(SuccessMessageMixin, CreateView): 
    model = Mesa
    form = Mesa
    fields = ["cantidad_personas","disponibilidad"] #parametros de la clase a crear, no está la ID ya que es automatica
    success_message = 'Mesa creada correctamente !' # Mostramos este Mensaje luego de Crear una Mesa
 
    # Redireccionamos a la página de listado luego de crear un registro de Mesa
    def get_success_url(self):
        success_message = 'Mesa creada correctamente !' # Mostramos este Mensaje luego de Crear una Mesa
        return reverse('listar_mesa') # Redireccionamos a la vista listar Mesa

class MesaActualizar(SuccessMessageMixin, UpdateView): 
    model = Mesa
    form = Mesa
    fields = ["cantidad_personas","disponibilidad"] #parametros de la clase a actualizar
    success_message = 'Mesa actualizada correctamente !' # Mostramos este Mensaje luego de actualizar una Mesa
 
    # Redireccionamos a la página de listado luego de actualizar un registro de Mesa
    def get_success_url(self):
        success_message = 'Mesa Creada Correctamente !' # Mostramos este Mensaje luego de actualizar una Mesa
        return reverse('listar_mesa') # Redireccionamos a la vista listar Mesa

class MesaDetalle(DetailView): 
    model = Mesa
 
class MesaEliminar(SuccessMessageMixin, DeleteView): 
    model = Mesa 
    form = Mesa
    fields = "__all__"     
 
    # Redireccionamos a la página principal luego de eliminar una Mesa
    def get_success_url(self): 
        success_message = 'Mesa eliminada correctamente !' # Mostramos este Mensaje luego de eliminar una Mesa  
        messages.success (self.request, (success_message))
        return reverse('listar_mesa')  
#CRUD MESA ↑↑↑