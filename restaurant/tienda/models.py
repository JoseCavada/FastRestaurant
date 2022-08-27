from django.db import models

# Create your models here.


class Mesa(models.Model):
	id_mesa = models.IntegerField(
		primary_key=True,
		db_column = 'id_mesa')
	cantidad_personas = models.IntegerField()
	disponibilidad = models.BooleanField(default=True)

	class Meta:
		managed = False
		db_table = 'MESA'

class Plato(models.Model):
	id_plato = models.IntegerField(
		primary_key=True,
		db_column = 'id_plato')
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

