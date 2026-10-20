from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventarioListView.as_view(), name='inventario'),
    path('<int:pk>/', views.inventarioDetailView.as_view(), name='vista_objeto'),
    path('detalle_objeto/<int:pk>/', views.detalles_objeto, name='detalles_objeto'),
    path('editar_objeto/<int:pk>/', views.editar_objeto, name='editar_objeto'),
    path('borrar_objetos/<int:pk>/', views.borrar_objetos, name='borrar_objetos'),
    path('buscar_objetos/', views.buscar_objetos, name='buscar_objetos'),
    path('agregar_objeto/', views.agregar_objeto, name='agregar_objeto'),
    path('exportar/', views.exportar.as_view(), name='exportar')
]