from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from datetime import datetime

from .forms import RegistroLoteriaForm
from .models import RegistroLoteria


@login_required
def registrar_numero(request):
    """Vista para registrar un número de lotería."""
    if request.method == 'POST':
        form = RegistroLoteriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Número ganador registrado exitosamente.')
            return redirect('loteria:listado')
    else:
        form = RegistroLoteriaForm()

    return render(request, 'loteria/registro.html', {'form': form})


@login_required
def listado_sorteos(request):
    registros = RegistroLoteria.objects.all().order_by('-fecha')
    return render(request, 'loteria/listado.html', {'registros': registros})


def cerrar_sesion(request):
    logout(request)
    return redirect('loteria:login')


def registro_exitoso(request):
    return render(request, 'loteria/exito.html')


def listar_sorteos_publico(request):
    """Vista pública para consultar números ganadores (CU-02)."""
    # Obtener parámetro de filtro por fecha
    fecha_filtro = request.GET.get('fecha', '')
    
    # Iniciar con todos los registros ordenados por fecha descendente
    sorteos = RegistroLoteria.objects.all().order_by('-fecha')
    
    # Aplicar filtro si se proporciona fecha (FA-01)
    if fecha_filtro:
        try:
            fecha_obj = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
            sorteos = sorteos.filter(fecha=fecha_obj)
        except ValueError:
            # Si fecha inválida, ignorar filtro
            fecha_filtro = ''
    
    # Implementar paginación de 10 registros (FA-02)
    paginator = Paginator(sorteos, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'sorteos': page_obj.object_list,
        'fecha_filtro': fecha_filtro,
        'total_sorteos': paginator.count,
    }
    
    return render(request, 'loteria/listado_publico.html', context)


@login_required
def editar_sorteo(request, id):
    """Vista para editar un número ganador (CU-03)."""
    # FE-01: Manejo de registro no encontrado
    sorteo = get_object_or_404(RegistroLoteria, pk=id)
    
    if request.method == 'POST':
        form = RegistroLoteriaForm(request.POST, instance=sorteo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sorteo actualizado correctamente.')
            return redirect('loteria:listado')
        else:
            # FE-02: Errores de validación (fecha duplicada, etc.)
            pass
    else:
        form = RegistroLoteriaForm(instance=sorteo)
    
    context = {
        'form': form,
        'sorteo': sorteo,
        'es_edicion': True,
    }
    
    return render(request, 'loteria/editar_sorteo.html', context)


@login_required
def eliminar_sorteo(request, id):
    """Vista para eliminar un número ganador (CU-04)."""
    # FE-01: Manejo de registro no encontrado
    sorteo = get_object_or_404(RegistroLoteria, pk=id)
    
    if request.method == 'POST':
        numero = sorteo.numero
        fecha = sorteo.fecha
        sorteo.delete()
        messages.success(request, f'Sorteo (Nº {numero} - {fecha}) eliminado permanentemente.')
        return redirect('loteria:listado')
    
    # Si no es POST, redirigir al listado (seguridad)
    return redirect('loteria:listado')
