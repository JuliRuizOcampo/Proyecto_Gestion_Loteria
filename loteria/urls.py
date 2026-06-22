from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import CustomAuthenticationForm

app_name = 'loteria'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='loteria/login.html',
            authentication_form=CustomAuthenticationForm,
        ),
        name='login',
    ),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('dashboard/', views.listado_sorteos, name='listado'),
    path('registrar/', views.registrar_numero, name='registrar'),
    path('editar/<int:id>/', views.editar_sorteo, name='editar_sorteo'),
    path('eliminar/<int:id>/', views.eliminar_sorteo, name='eliminar_sorteo'),
    path('exito/', views.registro_exitoso, name='registro_exitoso'),
    path('', views.listar_sorteos_publico, name='consultar_sorteos'),
]
