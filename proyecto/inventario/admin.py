from django.contrib import admin
from .models import inventario_objetos

# Register your models here.
@admin.register(inventario_objetos)
class inventarioAdmin(admin.ModelAdmin):
    list_display = ('codigo_pddh', 'descripcion', 'marca', 'modelo', 'serie', 'fecha_adquisición', 'valor_unitario')
    search_fields = ('codigo_pddh', 'descripcion', 'marca', 'modelo', 'serie')