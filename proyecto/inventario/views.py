from django.views.generic import ListView, DetailView
from .models import inventario_objetos
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .forms import objetoForm
from django.db.models import Q

# Create your views here.

class agregar_objeto(ListView):
    model = inventario_objetos
    template_name = 'agregar_objeto.html'
    context_object_name = 'inventario'

class detalles_objeto(ListView):
    model = inventario_objetos
    template_name = 'detalles_objeto.html'
    context_object_name = 'inventario'

class exportar(ListView):
    model = inventario_objetos
    template_name = 'exportar.html'
    context_object_name = 'inventario'

class inventarioListView(ListView):
    model = inventario_objetos
    template_name = 'inventario.html'
    context_object_name = 'inventario'

class inventarioDetailView(DetailView):
    model = inventario_objetos
    template_name = 'vista_objeto.html'
    context_object_name = 'inventario'


# Funciones
def inventario_inicio(request):
    objeto = inventario_objetos.objects.all()
    template = loader.get_template('inicio.html')
    context = {
            'inventario': objeto
        }
    return HttpResponse(template.render(context, request))

def agregar_objeto(request):
    if request.method == 'POST':
        form = objetoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = objetoForm()
    return render(request, 'agregar_objeto.html', {'form': form})

def detalles_objeto(request, pk):
    objeto = inventario_objetos.objects.get(pk=pk)
    return render(request, 'detalles_objeto.html', {'objeto': objeto})

def editar_objeto(request, pk):
    objeto = inventario_objetos.objects.get(pk=pk)
    
    if request.method == 'POST':
        # 2. Modificar los campos con la información del formulario
        objeto.nombre = request.POST.get('codigo_pddh')
        objeto.descripcion = request.POST.get('descripcion')
        objeto.marca = request.POST.get('marca')
        objeto.modelo = request.POST.get('modelo')
        objeto.serie = request.POST.get('serie')
        objeto.fecha_adquisicion = request.POST.get('fecha_adquisición')
        objeto.valor_unitario = request.POST.get('valor_unitario')
        objeto.save()
        
    return render(request, 'detalles_objeto.html', {'objeto': objeto})

def buscar_objetos(request):
    query = request.GET.get('q','')
    if query:
        resultados = inventario_objetos.objects.filter(
            Q(codigo_pddh__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(marca__icontains=query) |
            Q(modelo__icontains=query) |
            Q(serie__icontains=query)
        )
    else:
        resultados = inventario_objetos.objects.all()
    
    return render(request, 'inventario.html', {'object_list': resultados})

def borrar_objetos(request, pk):
    objeto = inventario_objetos.objects.get(pk=pk)
    objeto.delete()
    return redirect('inventario')