from django.db import models

# Create your models here.


class Mesa(models.Model):
	id_mesa = models.IntegerField(
		primary_key=True,
		db_column = 'ID_MESA')
	cantidad_personas = models.IntegerField()
	disponibilidad = models.BooleanField(default=True)
	

	class Meta:
		managed = False
		db_table = 'MESA'

class Plato(models.Model):
	id_plato = models.IntegerField(
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

	class Meta:
		managed = False
		db_table = 'PLATO'

class Ingrediente(models.Model):
	id_ingrediente = models.IntegerField(
		primary_key=True,
		db_column = 'ID_INGREDIENTE')
	id_plato = models.ForeignKey('Plato', models.DO_NOTHING, db_column='id_plato')
	id_insumo = models.ForeignKey('Insumo', models.DO_NOTHING, db_column='id_insumo')
	cantidad = models.BigIntegerField()

	def __str__(self):
		return self.id_ingrediente

	class Meta:
		managed = False
		db_table = 'INGREDIENTE'
		unique_together = (('id_ingrediente', 'id_plato'),)

class Insumo(models.Model):
	id_insumo = models.IntegerField(
		primary_key=True,
		db_column = 'ID_INSUMO',
		default = 0)
	nombre = models.CharField(max_length=255)
	cantidad = models.IntegerField()

	def __str__(self):
		return self.nombre

	class Meta:
		managed = False
		db_table = 'INSUMO'