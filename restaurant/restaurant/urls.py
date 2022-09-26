"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from account import views
from tienda import views as views2
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tienda/', include('tienda.urls')), #URL para visualiar la pagina, WIP
    path("accounts/register", views.register_request, name="register")#URL para registrar usuarios
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # URL para visualizar imagenes subidas


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')), #URLs para cuentas
]
urlpatterns += [
    path('accounts/', include('account.urls')), #URLs para cuentas
]
urlpatterns += [
    path('',views2.principal, name = 'principal'),
    path('totem',views2.inicioTotem, name='totem_inicio'),
    path('totem/mesas',views2.mesasTotem, name = "totem_mesas"),
    path('totem/menu',views2.menuTotem, name = "totem_verMenu"),
]