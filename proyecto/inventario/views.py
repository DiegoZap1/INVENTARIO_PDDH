from django.views.generic import ListView, DetailView
from .models import inventario_objetos

# Create your views here.
class inventarioListView(ListView):
    model = inventario_objetos
    template_name = 'inventario_list.html'
    context_object_name = 'inventario'

class inventarioDetailView(DetailView):
    model = inventario_objetos
    template_name = 'inventario_detail.html'
    context_object_name = 'inventario'
