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
    path('exportar/', views.exportar.as_view(), name='exportar'),
    path('exportar_pdf/', views.exportar_tabla_pdf, name='exportar_pdf'),
    path('exportar_word/', views.exportar_a_word, name='exportar_word'),
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
]