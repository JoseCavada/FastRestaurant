from django.db import models

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


'''
class Ingrediente(models.Model):
	id_ingrediente = models.IntegerField(
		primary_key=True,
		db_column = 'ID_INGREDIENTE'
		,null = True)
	id_plato = models.ForeignKey('Plato', models.DO_NOTHING, db_column='ID_PLATO',null = True)
	id_insumo = models.ForeignKey('Insumo', models.DO_NOTHING, db_column='ID_INSUMO',null = True)

	def __str__(self):
		return self.id_ingrediente

	class Meta:
		managed = False
		db_table = 'INGREDIENTE'
'''

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

	def __str__(self):
		return self.nombre

	class Meta:
		managed = True
		db_table = 'PLATO'



