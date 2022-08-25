from django.db import models
from django.contrib.auth.model import AbstractBaseUser, BaseUserManager #import para crear usuarios custom

# Create your models here.

class MyUserManager(BaseUserManager):

	"""
	Clase para crear usuarios mediante consola. Utiliza el mismo formato de los usuarios descrito mas abajo
	-La función "create_user" es para crear un usuario "común" o base
	-La función "create_super_user" es para crear un "superusuario" o "admin" para ingresar a la página de
	administrador que proporciona Django
	"""

	def create_user(self, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,nombre_usuario,correo,password,rol):
		user = self.model(
			primer_nombre = primer_nombre,
			segundo_nombre = segundo_nombre,
			primer_apellido = primer_apellido,
			nombre_usuario = normalize_username(nombre_usuario),
			correo = normalize_email(correo),
			rol = rol)
		user.set_password(password)
		user.save(using=self._db)
		return user
	def create_super_user(self, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,nombre_usuario,correo,password):
		user = self.create_user(
            primer_nombre = primer_nombre,
			segundo_nombre = segundo_nombre,
			primer_apellido = primer_apellido,
			nombre_usuario = normalize_username(nombre_usuario),
			correo = normalize_email(correo),
			rol = "Administrador")
        user.set_password(password)

        #user.is_admin = True //Añadir este parámetro si hace conflicto con la pagina de admin

        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
	"""
	Creación de usuario personalizado por medio de AbstracBaseUser, con sus caracteristicas, nombres,
	apellidos, correo, contraseña y rol. La ID se da por PL/SQL en la base de datos.
	El parametro DB_column sirve para identificar a que columna pertenece dentro de la base de datos ese
	atributo, es necesario para la llave primaria y contraseña, ya que si no django por defecto modifica
	la base de datos y eso no queremos. 
	"""
	id_user = models.IntegerField( primary_key = True, db_column= 'id_user')
	primer_nombre = models.CharField(
		verbose_name = "Primer nombre",
		max_length = 60  )
	segundo_nombre = models.CharField(
		verbose_name = "Segundo nombre",
		max_length = 60)
	primer_apellido = models.CharField(
		verbose_name = "Primer apellido",
		max_length = 60)
	segundo_apellido = models.CharField(
		verbose_name = "Segundo apellido",
		max_length = 60)
	nombre_usuario = models.CharField(
		verbose_name = "Nombre de usuario",
		max_length = 20)
	correo = models.EmailField(
		"Direcion de correo",)
	password = models.CharField(
		verbose_name = "Contraseña",
		max_length = 20, db_column = 'contraseña')
	rol = models.CharField(
		verbose_name = "rol",
		max_length = 20)

	"""
	Para manejar la sesion con el sistema propio de "django auth" es necesario identificar cual es el atributo
	que hace la funcion de username, ademas del email, esto para la implementacion de las notificaciones.
	"""
	USERNAME_FIELD = 'nombre_usuario'
	EMAIL_FIELD = 'correo'

	"""
	"Class Meta" para decirle a django que no modifique la tabla en la base de datos, ademas de identificar el nombre 
	de la misma.
	"""

	class Meta:
       managed = False
       db_table = 'USUARIO'