from django.shortcuts import  render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import DeleteView
from .models import MyUser
from django.contrib.messages.views import SuccessMessageMixin 
from django.urls import reverse
# Create your views here.


"""
Vista para el formulario de creación de usuarios, falta validar para que solo administrador
pueda entrar a la página y crear los usuarios
"""
def register_request(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)#Evita el guardado para cambios abajo
			user.password = make_password(user.password)#Encripta la contraseña
			if user.rol == "adm": #Setea como administrador el usuario si así fuese necesario
				user.is_staff = True
			user = form.save()
			messages.success(request, "Usuario registrado" )
			return redirect("index")
		messages.error(request, form.errors)
	form = RegisterForm()
	return render (request=request, template_name="registration/register.html", context={"RegisterForm":form})

class UsuarioListar(ListView):
	model = MyUser
	fields = ["id_user","primer_nombre","primer_apellido","nombre_usuario","correo","rol"]
	paginate_by = 10

class UsuarioDetalle(DetailView):
	model = MyUser
	fields = ["primer_nombre","segundo_nombre","primer_apellido","segundo_apellido","nombre_usuario","correo","rol","last_login","is_staff"]

class UsuarioEliminar(SuccessMessageMixin,DeleteView):
    model = MyUser
    form = MyUser
    fields = "__all__"

    # Redireccionamos a la página principal luego de eliminar una Mesa
    def get_success_url(self): 
        success_message = 'Usuario eliminada correctamente !' # Mostramos este Mensaje luego de eliminar una Mesa  
        messages.success (self.request, (success_message))
        return reverse('listar_usuario')  
