from django.shortcuts import render
from .forms import MesaCreationForm,InsumoCreationForm
from django.contrib import messages
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

def registrarInsumo(request):
	if request.method == "POST":
		form = InsumoCreationForm(request.POST)
		if form.is_valid():
			messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = InsumoCreationForm()
	return render (request=request, template_name="crear_insumo.html", context={"InsumoCreationForm":form})