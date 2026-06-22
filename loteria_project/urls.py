"""
URL configuration for loteria_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Redirige la raíz del sitio a la página pública de consulta de sorteos
    path("", RedirectView.as_view(pattern_name="loteria:consultar_sorteos", permanent=False)),
    # Cualquier URL que empiece con 'loteria/' será manejada por la app loteria
    path('loteria/', include('loteria.urls')),
]
