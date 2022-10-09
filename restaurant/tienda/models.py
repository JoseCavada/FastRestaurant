from django.db import models
from account.models import MyUser

# Create your models here.


class Mesa(models.Model):
	id_mesa = models.AutoField(
		primary_key=True,
		db_column = 'ID_MESA')
	cantidad_personas = models.IntegerField()
	disponibilidad = models.BooleanField(default=True)
	

	class Meta:
		managed = False
		db_table = 'MESA'

class Insumo(models.Model):
	id_insumo = models.AutoField(
		primary_key=True,
		db_column = 'ID_INSUMO')
	nombre = models.CharField(max_length=255)
	cantidad = models.IntegerField()

	def __str__(self):
		return self.nombre

	def __unicode__(self):
		return self.nombre
		
	class Meta:
		managed = True
		db_table = 'INSUMO'

class Plato(models.Model):
	id_plato = models.AutoField(
		primary_key=True,
		db_column = 'ID_PLATO')
	nombre = models.CharField(max_length=255)
	descripcion = models.CharField(max_length=255)
	precio = models.IntegerField()
	disponibilidad = models.BooleanField(default=False)
	imagen_producto = models.ImageField(
		upload_to='platos',
		null=True, 
		blank=True,
		default = '/noimage.png'
		)
	ingredientes = models.ManyToManyField('Insumo')

	puntuacion = models.IntegerField()

	def __str__(self):
		return self.nombre

	class Meta:
		managed = True
		db_table = 'PLATO'

class PedidoPlato(models.Model):
	id_pedido = models.AutoField(
		primary_key = True,
		db_column = 'ID_PEDIDO')

	id_mesa = models.ForeignKey(
		MyUser,
		on_delete = models.CASCADE,
		db_column = 'ID_MESA' )	

	estado = models.BooleanField(
		default = False)


	fecha_pedido_plato = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return f'{self.id_pedido} | {self.id_mesa}'

	class Meta:
		managed = True
		db_table = 'PEDIDO_PLATO'


class DetallePedidoPlato(models.Model):
	id_detalle_pedido = models.AutoField(
		primary_key = True,
		db_column = 'ID_DETALLE_PEDIDO')
	id_pedido = models.ForeignKey(
		PedidoPlato,
		on_delete = models.CASCADE,
		db_column = 'ID_PEDIDO',
		blank = True)

	id_plato = models.ForeignKey(
		Plato,
		on_delete = models.CASCADE,
		db_column = 'ID_PLATO')

	cantidad = models.IntegerField()

	ENUM_ESTADO = (
		('pen','pendiente'),
		('ped','pedido'),
		('pre','preparando'),
		('lis','listo'),)
	estado = models.CharField(
		verbose_name = "estado",
		choices = ENUM_ESTADO,
		default = "pen",
		max_length = 20,
		blank = True
		)

	def __str__(self):
		return f'ID: {self.id_detalle_pedido} | Pedido N°{self.id_pedido} | Plato: {self.id_plato} | Cantidad {self.cantidad} | Estado {self.estado}'
	class Meta:
		managed = True
		db_table = 'DETALLE_PEDIDO_PLATO'
