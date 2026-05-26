from django.contrib import admin
from .models import Producto, Cliente


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'precioVenta',
        'controlaStock',
        'stock',
        'activo',
    )

    list_filter = (
        'activo',
        'controlaStock',
    )

    search_fields = (
        'nombre',
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'dni',
        'telefono',
        'activo',
    )

    list_filter = (
        'activo',
    )

    search_fields = (
        'nombre',
        'dni',
    )