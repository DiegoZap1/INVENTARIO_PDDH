from django import forms
from .models import inventario_objetos

class objetoForm(forms.ModelForm):
    class Meta:
        model = inventario_objetos
        fields = '__all__'
        labels = {
            'codigo_pddh': 'Código PDDH',
            'descripcion': 'Descripción',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'serie': 'Serie',
            'fecha_adquisición': 'Fecha de adquisición',
            'valor_unitario': 'Valor unitario',
        }
        widgets = {
            'fecha_adquisición': forms.DateInput(attrs={'type': 'date'}),
        }