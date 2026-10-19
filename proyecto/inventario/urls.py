from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventarioListView.as_view(), name='inventario-list'),
    path('<int:pk>/', views.inventarioDetailView.as_view(), name='inventario-detail'),
]