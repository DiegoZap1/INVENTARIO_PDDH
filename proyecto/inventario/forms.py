from django import forms
from .models import inventario_objetos

class objetoForm(forms.ModelForm):
    class Meta:
        model = inventario_objetos
        fields = '__all__'
        widgets = {
            'fecha_adquisición': forms.DateInput(attrs={'type': 'date'}),
        }