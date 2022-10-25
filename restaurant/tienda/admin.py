from django.contrib import admin
from tienda.models import *

# Register your models here.
admin.site.register(Mesa)
admin.site.register(Plato)
admin.site.register(Insumo)
admin.site.register(PedidoPlato)
admin.site.register(DetallePedidoPlato)
admin.site.register(ReservaMesa)