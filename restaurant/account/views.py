from django.shortcuts import  render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password
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
			messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = RegisterForm()
	return render (request=request, template_name="register.html", context={"RegisterForm":form})