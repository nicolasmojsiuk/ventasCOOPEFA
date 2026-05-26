from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "gestionComercial"

urlpatterns = [

    # ───────────────── PRODUCTOS ─────────────────

    path(
        "",
        login_required(views.listaProductos),
        name="listaProductos"
    ),

    path(
        "productos/nuevo/",
        login_required(views.nuevoProducto),
        name="nuevoProducto"
    ),

    path(
        "productos/editar/<int:id>/",
        login_required(views.editarProducto),
        name="editarProducto"
    ),

    path(
        "productos/eliminar/<int:id>/",
        login_required(views.eliminarProducto),
        name="eliminarProducto"
    ),

    # ───────────────── CLIENTES ─────────────────

    path(
        "clientes/",
        login_required(views.listaClientes),
        name="listaClientes"
    ),

    path(
        "clientes/nuevo/",
        login_required(views.nuevoCliente),
        name="nuevoCliente"
    ),

    path(
        "clientes/editar/<int:id>/",
        login_required(views.editarCliente),
        name="editarCliente"
    ),

    path(
        "clientes/eliminar/<int:id>/",
        login_required(views.eliminarCliente),
        name="eliminarCliente"
    ),

    # ───────────────── VENTAS ─────────────────


    path(
        "ventas/nueva/",
        login_required(views.nuevaVenta),
        name="nuevaVenta"
    ),

    path(
        'ventas/detalle/<int:id>/',
        views.detalleVenta,
        name='detalleVenta'
    ),
    path(
        'ventas/',
        views.historialVentas,
        name='historialVentas'      
    ),


    # ───────── REPORTES ─────────

    path(
        'reportes/',
        views.reportes,
        name='reportes'
    ),

    path(
        'reportes/ventas-dia/',
        views.ventasDia,
        name='ventasDia'
    ),

    path(
        'reportes/productos-mas-vendidos/',
        views.productosMasVendidos,
        name='productosMasVendidos'
    ),

    path(
        'reportes/stock-bajo/',
        views.stockBajo,
        name='stockBajo'
    ),

    path(
        'reportes/mejores-clientes/',
        views.mejoresClientes,
        name='mejoresClientes'
    ),
    # ───────────────── API AJAX ─────────────────

    path(
        "api/clientes/",
        login_required(views.buscarClientes),
        name="buscarClientes"
    ),

    path(
        "api/productos/",
        login_required(views.buscarProductos),
        name="buscarProductos"
    ),
        
    path(
        'caja/cierre/',
        views.cierreCaja,
        name='cierreCaja'
    ),

]

