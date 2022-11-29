from django.shortcuts import render, redirect
from .forms import MesaCreationForm, QrMesaForm, DetallePedidoPlatoForm, EditarPlatoPedidoForm
from .forms import EstadoPlatoPedidoForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Insumo, Mesa, Plato, PedidoPlato, DetallePedidoPlato,ReservaMesa
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin 
from django import forms
from django.http import HttpResponseRedirect
import qrcode
import os 
from pathlib import Path
from account.models import MyUser
from sesame.utils import get_query_string
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms.widgets import  DateTimeInput
import json

import mercadopago

sdk = mercadopago.SDK("TEST-4563605199678853-111816-ea7136dc430bc360cccb1b54ce59ef38-146275990")

# Create your views here.

def principal(request):
    return render(request, 'principal.html')

def index(request):
    if request.user.rol == "mesa":
        return menuTotem(request)
    elif request.user.rol =="coc":
        return verPedidos(request)
    return render(request,'index.html')

#TOTEM ↓↓↓
def inicioTotem(request):
    return render(request, 'totem/TotemPrincipal.html')

def mesasTotem(request):
    if request.method == 'POST':
        form = QrMesaForm(request.POST)
        if form.is_valid():
            id_mesa = form.cleaned_data['id_mesa']
            print ("existoooo"+id_mesa)
            User = get_user_model()
            user = User.objects.get(nombre_usuario = f'Mesa {id_mesa}')
            #user = User.objects.filter(nombre_usuario = id_mesa )
            print( f'existoooo {user.id_user}')
            domain = request.META['HTTP_HOST']
            login_url = domain + "/sesame/login/"
            login_url += get_query_string(user)
            img = qrcode.make(login_url)
            img.save(f'static/mesa{id_mesa}.png')
            print("antes redirect")
            #HttpResponseRedirect(f'/qrMesa/{id_mesa}')
            return HttpResponseRedirect(f'/totem/qrMesa/{id_mesa}')
            print("despues redirect")
    num_mesa = Mesa.objects.all()
    return render(request,'totem/TotemMesas.html',context = {"num_mesa":num_mesa})

def qrpantalla(request):
    domain = request.META['HTTP_HOST']
    dataQr = domain + "/totem/menu"
    img = qrcode.make(dataQr)
    img.save('static/menu.png')

    return render(request, 'totem/TotemQRMenu.html')

def menuTotem(request):
    num_plato = Plato.objects.all()

    user = request.user
    pedido = PedidoPlato()
    boton_pago = False

    try:
        pedido = PedidoPlato.objects.filter(id_mesa = user, pagado = False).first()
        platos = DetallePedidoPlato.objects.filter(id_pedido = pedido, estado = "lis").count()
        if platos > 0:
            boton_pago = True
        print(boton_pago)
    except pedido.DoesNotExist:
        boton_pago = False
        print(boton_pago)



    return render(request, 'totem/TotemVerMenu.html',context={"num_plato":num_plato,"boton_pago":boton_pago})
def mesaTotem(request, id):
    mesa = f'mesa{id}.png'
    return render(request, template_name="totem/TotemQRMesa.html",context = {"mesa":mesa} )

def qrReservarMesaTotem (request):
    domain = request.META['HTTP_HOST']
    dataQr = domain + "/totem/reservar"
    img = qrcode.make(dataQr)
    img.save('static/reservar.png')
    return render(request, template_name = "totem/TotemQRReservarMesa.html")

class reservaMesaTotem(SuccessMessageMixin, CreateView):
    model = ReservaMesa
    form = ReservaMesa
    fields = ["id_mesa","nombre","apellido","rut","correo","telefono","comentario", "fecha_reserva"]
    success_message = 'Reserva realizada correctamente, revise su correo'
    def get_success_url(self):
        return reverse("totem_reservado")
    def get_form(self, form_class=None):
        form = super(reservaMesaTotem, self).get_form(form_class)
        form.fields['fecha_reserva'].widget = DateTimeInput(attrs={'type':'datetime-local'})
        return form
    
def reservaHecha(request):
    return render(request, template_name = "totem/TotemReservaHecha.html")
#TOTEM ↑↑↑
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
'''
class MesaCrearr(SuccessMessageMixin, CreateView): 
    model = Mesa
    form = Mesa
    fields = ["cantidad_personas","disponibilidad"] #parametros de la clase a crear, no está la ID ya que es automatica
    success_message = 'Mesa creada correctamente !' # Mostramos este Mensaje luego de Crear una Mesa
 
    # Redireccionamos a la página de listado luego de crear un registro de Mesa
    def get_success_url(self):
        success_message = 'Mesa creada correctamente !' # Mostramos este Mensaje luego de Crear una Mesa
        return reverse('listar_mesa') # Redireccionamos a la vista listar Mesa
'''
def MesaCrear(request):
    if request.method == "POST":
        form = MesaCreationForm(request.POST)
        if form.is_valid():
            mesa = form.save()
            user = MyUser(primer_nombre = f'Mesa {mesa.id_mesa}',
             segundo_nombre = f'Mesa {mesa.id_mesa}',
             primer_apellido = f'Mesa {mesa.id_mesa}',
             segundo_apellido = f'Mesa {mesa.id_mesa}',
             nombre_usuario = f'Mesa {mesa.id_mesa}',
             correo = f'Mesa{mesa.id_mesa}@Mesa{mesa.id_mesa}.com',
             rol = "mesa",
             password = f'mesa{mesa.id_mesa}')
            user.save()
            messages.success(request, "Mesa registrada" )
            return redirect("listar_mesa")
        messages.error(request, form.errors)
    form = MesaCreationForm()
    return render (request=request, template_name="crud_mesa/CrearMesa.html", context={"MesaCreationForm":form})

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

#CRUD PLATO ↓↓↓
class PlatoListado(ListView):
    model = Plato
    paginate_by = 10

class PlatoDetalle(DetailView):
    model = Plato

class PlatoCrear(SuccessMessageMixin, CreateView): 
    model = Plato
    form = Plato
    fields = ["nombre","descripcion","precio","disponibilidad","imagen_producto","ingredientes","puntuacion"] #parametros de la clase a crear, no está la ID ya que es automatica
    success_message = 'Plato creada correctamente !' # Mostramos este Mensaje luego de Crear un Plato
 
    # Redireccionamos a la página de listado luego de crear un registro de Plato
    def get_success_url(self):
        success_message = 'Plato creado correctamente !' # Mostramos este Mensaje luego de Crear un Plato
        return reverse('listar_plato') # Redireccionamos a la vista listar Plato

class PlatoActualizar(SuccessMessageMixin, UpdateView):
    model = Plato
    form = Plato
    fields = ["nombre","descripcion","precio","disponibilidad","imagen_producto","ingredientes",]
    success_message = 'Plato Actualizada Correctamente !'
    def get_success_url(self):
        success_message = 'Plato Actualizada Correctamente !' # Mostramos este Mensaje luego de actualizar una Mesa
        return reverse('listar_plato')

class PlatoEliminar(SuccessMessageMixin, DeleteView): 
    model = Plato 
    form = Plato
    fields = "__all__"     
 
    # Redireccionamos a la página principal luego de eliminar un Plato
    def get_success_url(self): 
        success_message = 'Plato eliminada correctamente !' # Mostramos este Mensaje luego de eliminar una Mesa  
        messages.success (self.request, (success_message))
        return reverse('listar_plato')  

#CRUD PLATO ↑↑↑

#PEDIDOS PLATOS ↓↓↓
'''
Carrito para manejar los pedidos hechos, esto para tener un mejor control en los resúmenes
de datos
'''
def agregarCarrito(request, pk):
    plato = Plato.objects.get(id_plato = pk) #se obtiene el objeto referenciado para agregar al pedido
    comanda = PedidoPlato #se inicializa la variable comanda, la cual hace referencia a un objeto del tipo pedido plato
    user = request.user #se recupera el usuario que está logeado, esto para conocer la mesa la cual está pidiendo los platos

    if request.method == 'POST':
        '''
        TRY y EXCEPT:
        Para saber si la el plato pertenece a una misma orden de pedido, primero se busca
        una comanda(objeto del tipo PedidoPlato) que esté con un estado FALSE y que pertenezca
        a la misma mesa la cual se encuentra el usuario. Si esto no fuese así, se crea un
        nuevo objeto del tipo comanda para utilizar ese en su lugar.
        '''
        try:
            comanda = PedidoPlato.objects.get(
                id_mesa = user,
                estado = False)
        except comanda.DoesNotExist:
            comanda = PedidoPlato(
                id_mesa = user,
                estado = False)
            comanda.save()
        form = DetallePedidoPlatoForm(request.POST) #Linkeando el formulario de la vista con el hecho en sistema
        if form.is_valid():
            plato_pedido = form.save(commit = False)
            plato_pedido.id_pedido = comanda #se conecta la comanda con el plato, para identificarlo
            plato_pedido.save()
            messages.add_message(request, messages.INFO, 'plato agregado')
            return redirect('totem_vermenu')
        messages.error(request, form.errors)
    return render(request = request, template_name = "pedido/PedirPlato.html", context={"plato":plato})

'''
Funcion para visualizar carrito

1. Primero se instancian las variable "user" y "pedido", la primera para poder sincronizar el
carrito que se crea con el usuario específicio y la segunda crea una clase "PedidoPlato" vacía
para que pueda ser manejada en él.

2. Luego se comprueba mediante un "TRY - EXCEPT" si existe una instancia de carrito o "PedidoPlato"
que concuerde con la mesa y la cual se encuentra aún recibiendo platos dentro o con un "ESTADO = FALSE",
si no fuese así, se retorne un carrito vacío.

3. Si se presiona el botón de realizar pedido, el carrito cambia su estado a "TRUE" lo que lo deja
completado y cerrado para nuevas adiciones de platos (veáse punto 2), ademas de cambiar el estado
de los platos agregados a este a "PEN" o pendiente, esto para que puedan ser visualizados por
el usuario cocina en su sesión.

'''
def verCarrito(request):
    user = request.user
    pedido = PedidoPlato()
    subtotal = 0

    #Comprobador para saber si existe un 
    try:
        pedido = PedidoPlato.objects.get(id_mesa = user, estado = False)
    except pedido.DoesNotExist:
        return render(request = request, template_name = "pedido/VerCarrito.html")
    platos_pedidos = DetallePedidoPlato.objects.filter(id_pedido = pedido)
    for plato in platos_pedidos:
        precio = plato.id_plato.precio
        cantidad = plato.cantidad
        subtotal += precio * cantidad
    if request.method == 'POST' and 'pedir' in request.POST and pedido != None:
        for plato in platos_pedidos:
            plato.estado = "ped"
            plato.save()
        pedido.estado = True
        pedido.save()
        messages.add_message(request, messages.INFO, 'Pedido realizado')
        return redirect('totem_vermenu')


    return render(request = request, template_name = "pedido/VerCarrito.html", context={"pedido":pedido,"platos_pedidos":platos_pedidos, "subtotal":subtotal})

class carritoBorrar(SuccessMessageMixin, DeleteView):
    model = DetallePedidoPlato
    form = DetallePedidoPlato
    fields ="__all__"

    def get_success_url(self): 
        success_message = 'Plato eliminado correctamente!' # Mostramos este Mensaje luego de eliminar una Mesa  
        messages.success (self.request, (success_message))
        return reverse('ver_carrito')
#Mercadopago ↓↓↓
def mercadopago_checkout(request, **kwargs):


    user = request.user
    items=[]
    total = 0
    pedidos = PedidoPlato.objects.filter(id_mesa = user, pagado= False)
    for pedido in pedidos:
        platos = DetallePedidoPlato.objects.filter(id_pedido = pedido, estado = "lis")

        for item in platos:

            nomProducto = str(item.id_plato.nombre)
            print(item.id_plato.nombre)
            cantProducto = int(item.cantidad)
            print(item.cantidad)
            precProducto = int(item.id_plato.precio)
            print(item.id_plato.precio)
            monArt = 'CLP'
            datos = {'title':nomProducto, 'quantity':cantProducto, 'currency_id':monArt, 'unit_price':precProducto}
            items.append(datos)
            total += datos['unit_price'] * datos['quantity']

    preference_data = {
                "items": items,

                "back_urls": { 
                                "success": "http://localhost:8000/tienda/pagado",
                                "failure": "http://www.failure.com",
                                "pending": "http://www.pending.com"
                                
                },

                "auto_return": "approved",
            }    

    preference_response = sdk.preference().create(preference_data)
    print(preference_response)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(preference_response['response']['id'])
    print(total)
    preference = preference_response['response']['id']
    #preference_id = preference_response["id"]
    return render(request = request, template_name = "mercadopago/PagarBoton.html", context={"preferencia":preference, "platos":items,"aPagar":total})

def pagoRealizado(request):
    '''
    Redirigir a este link, comprueba con GET el estado en el URL, si es exitoso, cierra
    sesión y modifica estado en la base de datos de los platos a pagado. Modo de hacer la
    boleta aún en discución.
    Posibilidad de página diciendo pago exitoso, quizas cambiar el deslog para recibir
    parámetros, puede ser
    '''
    user = request.user

    mesa =  user.primer_nombre.lower()
    mesa = mesa.strip()
    print(mesa)
    if request.GET.get('collection_status',"approved"):
        ''' 
        Tiene que cambiar la contraseña del usuario mesa, así te fuerza a cerrar la sesión.
        Tambien borrar la imagen correspondiente y cambiar el estado de los platos a pagado
        para que así no le aparezcan a la siguiente persona que pida la mesa.
        '''
        #os.rmdir(f'static/{mesa}.png')
        pedidos = PedidoPlato.objects.filter(id_mesa = user, pagado= False)

        clave = MyUser.objects.make_random_password(length=8, allowed_chars='123456789')

        for pedido in pedidos:

            platos = DetallePedidoPlato.objects.filter(id_pedido = pedido, estado = "lis")
            pedido.pagado=True
            pedido.save()
            for plato in platos:

                plato.estado="pag"
                plato.save()

        user.password = clave
        user.save()
        



    return render(request = request, template_name = "mercadopago/PagoRealizado.html")

def pagoNoExitoso():
    pass




def carritoEditar(request, pk):
    user = request.user
    plato_pedido = DetallePedidoPlato.objects.get(id_detalle_pedido = pk)
   #plato = Plato.objects.get(id_plato = plato_pedido.id_plato)
    if request.method == 'POST':
        form = EditarPlatoPedidoForm(request.POST)
        if form.is_valid():
            plato_pedido.cantidad = form.cleaned_data['cantidad']
            if plato_pedido.cantidad == 0:
                plato_pedido.delete()
                messages.add_message(request, messages.INFO, 'Plato eliminado')
                return redirect('ver_carrito')
            plato_pedido.save()
            messages.add_message(request, messages.INFO,'Cantidad editada')
            return redirect('ver_carrito')
    return render(request = request, template_name = "pedido/EditarCarrito.html", context={"plato":plato_pedido})



#PEDIDOS PLATOS ↑↑↑
#Vista cocina ↓↓↓
def verPedidos(request):
    pedidos = DetallePedidoPlato.objects.filter(
        Q(estado = "ped") | Q(estado = "pre")).order_by('id_pedido','id_plato__puntuacion')
    plato = DetallePedidoPlato()
    if request.method == 'POST':
        form = EstadoPlatoPedidoForm(request.POST)
        print("form method es post")
        if form.is_valid():
            print("form valido")
            id_plato_form = form.cleaned_data['id_plato'] 
            id_detalle_pedido_form = form.cleaned_data['id_detalle_pedido']
            #plato = Plato.objects.filter(id_plato = id_plato_form)
            plato = DetallePedidoPlato.objects.get(id_plato = id_plato_form, id_detalle_pedido = id_detalle_pedido_form)
            if plato.estado == "ped":
                print("form es pedido")
                plato.estado = "pre"
                plato.save()
                return render(request = request, template_name = "cocina/VerComandas.html", context = {"pedidos":pedidos})
            elif plato.estado == "pre":
                print("form es preparado")
                plato.estado = "lis"
                plato.save()
                return render(request = request, template_name = "cocina/VerComandas.html", context = {"pedidos":pedidos})

    return render(request = request, template_name = "cocina/VerComandas.html", context = {"pedidos":pedidos})
#Informe
#Vista Informe
def GenerarInforme(request):
    # total = Plato.id_plato
    # for total in 
    informe = Plato.objects.count() 
    informe2 = Insumo.objects.count()
    totalDiario = 0
    pedidos = PedidoPlato.objects.filter(pagado = True)

    for pedido in pedidos:
        platos = DetallePedidoPlato.objects.filter(id_pedido = pedido)

        for plato in platos:
            totalDiario = totalDiario + plato.id_plato.precio

    print(f'La cantidad de platos es {informe} ')
    print(f'Total diario ganado es {totalDiario} ')
    return render(request= request, template_name= "informe/PruebaInforme.html",context= {"informe":informe,"informe2":informe2,"totalDiario":totalDiario})

