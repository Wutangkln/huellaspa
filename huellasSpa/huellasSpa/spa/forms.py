# spa/forms.py

from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria']

class BusquedaForm(forms.Form):
    busqueda = forms.CharField(required=False, label='Buscar')
