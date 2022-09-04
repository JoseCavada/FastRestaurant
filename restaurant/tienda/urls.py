from django.urls import path 
from . import views

urlpatterns=[
	path('',views.index, name = 'index'),
	path('mesa', views.registrarMesa, name = 'registrarMesa'),
	path('insumo', views.registrarInsumo, name = 'registrarInsumo')
]