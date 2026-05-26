from django import forms

from .models import (
    Producto,
    Cliente,
    Venta
)


# ───────── PRODUCTOS ─────────

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto

        fields = [
            'codigo',
            'nombre',
            'precioVenta',
            'controlaStock',
            'stock',
            'activo'
        ]

        widgets = {

            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código del producto'
            }),

            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),

            'precioVenta': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),

            'controlaStock': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0'
            }),

            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'codigo': 'Código',
            'nombre': 'Nombre',
            'precioVenta': 'Precio de venta',
            'controlaStock': 'Controla stock',
            'stock': 'Stock',
            'activo': 'Producto activo',
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if nombre:
            return nombre.strip().title()

        return nombre

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')

        if codigo:
            return codigo.strip().upper()

        return codigo


# ───────── CLIENTES ─────────

class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente

        fields = [
            'nombre',
            'dni',
            'telefono',
            'activo'
        ]

        widgets = {

            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente'
            }),

            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'DNI'
            }),

            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),

            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'nombre': 'Nombre',
            'dni': 'DNI',
            'telefono': 'Teléfono',
            'activo': 'Cliente activo',
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if nombre:
            return nombre.strip().title()

        return nombre


# ───────── VENTAS ─────────

class VentaForm(forms.ModelForm):

    class Meta:
        model = Venta

        fields = [
            'cliente',
            'metodo_pago'
        ]

        widgets = {

            'cliente': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_cliente'
            }),

            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        labels = {
            'cliente': 'Cliente',
            'metodo_pago': 'Método de pago'
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['cliente'].queryset = Cliente.objects.filter(
            activo=True
        ).order_by('nombre')

        self.fields['cliente'].empty_label = 'Seleccioná un cliente'