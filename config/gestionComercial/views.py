import json
from decimal import Decimal
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import (
    Q,
    F,
    Sum,
    Count
)
from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)


from .forms import (
    ProductoForm,
    ClienteForm,
    VentaForm
)

from .models import (
    Producto,
    Cliente,
    Venta,
    DetalleVenta
)


# ───────────────── REPORTES ─────────────────

@login_required
def reportes(request):

    return render(
        request,
        'reportes/index.html'
    )


# ───────── VENTAS DEL DÍA ─────────

@login_required
def ventasDia(request):

    hoy = now().date()

    ventas = Venta.objects.filter(
        fecha__date=hoy
    ).order_by('-fecha')

    total = ventas.aggregate(
        total=Sum('total')
    )['total'] or 0

    cantidad = ventas.count()

    return render(
        request,
        'reportes/ventasDia.html',
        {
            'ventas': ventas,
            'total': total,
            'cantidad': cantidad
        }
    )


# ───────── PRODUCTOS MÁS VENDIDOS ─────────

@login_required
def productosMasVendidos(request):

    productos = DetalleVenta.objects.all()

    filtro = request.GET.get('filtro','dia')

    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')

    hoy = now()

    if filtro == 'dia':

        productos = productos.filter(
            venta__fecha__date=hoy.date()
        )

    elif filtro == 'mes':

        productos = productos.filter(
            venta__fecha__month=hoy.month,
            venta__fecha__year=hoy.year
        )

    elif filtro == 'anio':

        productos = productos.filter(
            venta__fecha__year=hoy.year
        )

    elif filtro == 'personalizado':

        if fecha_desde and fecha_hasta:

            productos = productos.filter(
                venta__fecha__date__range=[
                    fecha_desde,
                    fecha_hasta
                ]
            )

    productos = productos.values(
        'producto__nombre'
    ).annotate(
        total_vendidos=Sum('cantidad')
    ).order_by(
        '-total_vendidos'
    )

    return render(request, 'reportes/productosMasVendidos.html', {
    'productos': productos,
    'filtro_activo': filtro,
    'desde_val': request.GET.get('desde', ''),
    'hasta_val': request.GET.get('hasta', ''),
    })


# ───────── STOCK BAJO ─────────

@login_required
def stockBajo(request):

    limite = request.GET.get('limite')

    if not limite:

        limite = 5

    productos = Producto.objects.filter(
        controlaStock=True,
        stock__lte=limite
    ).order_by('stock')

    return render(
        request,
        'reportes/stockBajo.html',
        {
            'productos': productos,
            'limite': limite
        }
    )


# ───────── MEJORES CLIENTES ─────────

@login_required
def mejoresClientes(request):

    clientes = Cliente.objects.all()

    filtro = request.GET.get('filtro','dia')

    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')

    hoy = now()

    ventas = Venta.objects.all()

    if filtro == 'dia':

        ventas = ventas.filter(
            fecha__date=hoy.date()
        )

    elif filtro == 'mes':

        ventas = ventas.filter(
            fecha__month=hoy.month,
            fecha__year=hoy.year
        )

    elif filtro == 'anio':

        ventas = ventas.filter(
            fecha__year=hoy.year
        )

    elif filtro == 'personalizado':

        if fecha_desde and fecha_hasta:

            ventas = ventas.filter(
                fecha__date__range=[
                    fecha_desde,
                    fecha_hasta
                ]
            )

    clientes = clientes.annotate(

        total_compras=Count(
            'venta',
            filter=Q(
                venta__in=ventas
            )
        ),

        total_gastado=Sum(
            'venta__total',
            filter=Q(
                venta__in=ventas
            )
        )

    ).order_by(
        '-total_compras',
        '-total_gastado'
    )

    return render(request, 'reportes/mejoresClientes.html', {
    'clientes': clientes,
    'filtro_activo': filtro,
    'desde_val': request.GET.get('desde', ''),
    'hasta_val': request.GET.get('hasta', ''),
})


# ───────────────── PRODUCTOS ─────────────────

@login_required(login_url='login')
def listaProductos(request):

    productos = Producto.objects.filter(
        activo=True
    ).order_by('nombre')

    return render(
        request,
        'gestionComercial.html',
        {
            'productos': productos
        }
    )


@login_required(login_url='login')
def nuevoProducto(request):

    if request.method == 'POST':

        form = ProductoForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Producto creado correctamente.'
            )

            return redirect(
                'gestionComercial:listaProductos'
            )

        messages.error(
            request,
            'Corregí los errores del formulario.'
        )

    else:

        form = ProductoForm()

    return render(
        request,
        'inventario/nuevo.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def editarProducto(request, id):

    producto = get_object_or_404(
        Producto,
        id=id
    )

    if request.method == 'POST':

        form = ProductoForm(
            request.POST,
            instance=producto
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Producto actualizado correctamente.'
            )

            return redirect(
                'gestionComercial:listaProductos'
            )

    else:

        form = ProductoForm(
            instance=producto
        )

    return render(
        request,
        'inventario/editar.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def eliminarProducto(request, id):

    producto = get_object_or_404(
        Producto,
        pk=id
    )

    producto.activo = False
    producto.save()

    messages.success(
        request,
        'Producto eliminado correctamente.'
    )

    return redirect(
        'gestionComercial:listaProductos'
    )


# ───────────────── CLIENTES ─────────────────

@login_required(login_url='login')
def listaClientes(request):

    clientes = Cliente.objects.filter(
        activo=True
    ).order_by('nombre')

    return render(
        request,
        'clientes.html',
        {
            'clientes': clientes
        }
    )


@login_required(login_url='login')
def nuevoCliente(request):

    if request.method == 'POST':

        form = ClienteForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Cliente creado correctamente.'
            )

            return redirect(
                'gestionComercial:listaClientes'
            )

        messages.error(
            request,
            'Corregí los errores del formulario.'
        )

    else:

        form = ClienteForm()

    return render(
        request,
        'clientes/nuevo.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def editarCliente(request, id):

    cliente = get_object_or_404(
        Cliente,
        id=id
    )

    if request.method == 'POST':

        form = ClienteForm(
            request.POST,
            instance=cliente
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Cliente actualizado correctamente.'
            )

            return redirect(
                'gestionComercial:listaClientes'
            )

    else:

        form = ClienteForm(
            instance=cliente
        )

    return render(
        request,
        'clientes/editar.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def eliminarCliente(request, id):

    cliente = get_object_or_404(
        Cliente,
        pk=id
    )

    cliente.activo = False
    cliente.save()

    messages.success(
        request,
        'Cliente eliminado correctamente.'
    )

    return redirect(
        'gestionComercial:listaClientes'
    )


# ───────────────── VENTAS ─────────────────

@login_required(login_url='login')
def listaVentas(request):

    ventas = Venta.objects.all().order_by('-id')

    return render(
        request,
        'ventas.html',
        {
            'ventas': ventas
        }
    )


@login_required(login_url='login')
@transaction.atomic
def nuevaVenta(request):

    if request.method == 'POST':

        form = VentaForm(request.POST)

        productos_json = request.POST.get(
            'productos'
        )

        if not productos_json:

            messages.error(
                request,
                'Debés agregar productos.'
            )

            return redirect(
                'gestionComercial:nuevaVenta'
            )

        productos = json.loads(productos_json)

        if form.is_valid():

            venta = form.save(
                commit=False
            )

            venta.usuario = request.user
            venta.total = Decimal('0.00')

            venta.save()

            total_general = Decimal('0.00')

            for item in productos:

                producto = Producto.objects.get(
                    id=item['producto']
                )

                cantidad = int(
                    item['cantidad']
                )

                precio = Decimal(
                    str(producto.precioVenta)
                )

                subtotal = precio * cantidad

                # ───────── CONTROL STOCK ─────────

                if producto.controlaStock:

                    if producto.stock < cantidad:

                        transaction.set_rollback(True)

                        messages.error(
                            request,
                            f'Stock insuficiente para {producto.nombre}.'
                        )

                        return redirect(
                            'gestionComercial:nuevaVenta'
                        )

                    Producto.objects.filter(
                        id=producto.id
                    ).update(
                        stock=F('stock') - cantidad
                    )

                # ───────── DETALLE ─────────

                DetalleVenta.objects.create(

                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio=precio,
                    subtotal=subtotal
                )

                total_general += subtotal

            venta.total = total_general
            venta.save()

            messages.success(
                request,
                'Venta registrada correctamente.'
            )

            return redirect(
                'gestionComercial:nuevaVenta'
            )

        messages.error(
            request,
            'Corregí los errores del formulario.'
        )

    else:

        form = VentaForm()

    return render(
        request,
        'ventas/nuevo.html',
        {
            'form': form
        }
    )





@login_required
def historialVentas(request):

    ventas = Venta.objects.select_related(
        'cliente',
        'usuario'
    )

    filtro = request.GET.get('filtro', 'dia')

    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')

    hoy = now()

    # ───────── FILTROS ─────────

    if filtro == 'dia':

        ventas = ventas.filter(
            fecha__date=hoy.date()
        )

    elif filtro == 'mes':

        ventas = ventas.filter(
            fecha__month=hoy.month,
            fecha__year=hoy.year
        )

    elif filtro == 'anio':

        ventas = ventas.filter(
            fecha__year=hoy.year
        )

    elif filtro == 'personalizado':

        if fecha_desde and fecha_hasta:

            ventas = ventas.filter(
                fecha__date__range=[
                    fecha_desde,
                    fecha_hasta
                ]
            )

    ventas = ventas.order_by('-fecha')

    # ───────── TOTALES ─────────

    total_general = ventas.aggregate(
        total=Sum('total')
    )['total'] or 0

    cantidad_ventas = ventas.count()

    efectivo = ventas.filter(
        metodo_pago='efectivo'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    debito = ventas.filter(
        metodo_pago='debito'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    credito = ventas.filter(
        metodo_pago='credito'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    transferencia = ventas.filter(
        metodo_pago='transferencia'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    return render(
    request,
    'ventas/historial.html',
    {
        'ventas': ventas,
        'total_general': total_general,
        'cantidad_ventas': cantidad_ventas,
        'efectivo': efectivo,
        'debito': debito,
        'credito': credito,
        'transferencia': transferencia,
        'filtro_activo': filtro or 'dia',
        'desde_val': fecha_desde or '',
        'hasta_val': fecha_hasta or '',
    }
)


@login_required
def detalleVenta(request, id):

    venta = get_object_or_404(
        Venta.objects.select_related(
            'cliente',
            'usuario'
        ),
        id=id
    )

    detalles = DetalleVenta.objects.select_related(
        'producto'
    ).filter(
        venta=venta
    )

    return render(
        request,
        'ventas/detalle.html',
        {
            'venta': venta,
            'detalles': detalles
        }
    )


# ───────────────── API CLIENTES ─────────────────

@login_required(login_url='login')
def buscarClientes(request):

    q = request.GET.get('q', '')

    clientes = Cliente.objects.filter(
        Q(nombre__icontains=q) |
        Q(dni__icontains=q),
        activo=True
    )[:10]

    data = []

    for cliente in clientes:

        data.append({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'dni': cliente.dni
        })

    return JsonResponse(
        data,
        safe=False
    )


# ───────────────── API PRODUCTOS ─────────────────

@login_required(login_url='login')
def buscarProductos(request):

    q = request.GET.get('q', '')

    productos = Producto.objects.filter(
        Q(nombre__icontains=q) |
        Q(codigo__icontains=q),
        activo=True
    )[:10]

    data = []

    for producto in productos:

        data.append({
            'id': producto.id,
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'precio': float(producto.precioVenta),
            'stock': producto.stock
        })

    return JsonResponse(
        data,
        safe=False
    )





@login_required
def cierreCaja(request):

    hoy = now().date()

    ventas = Venta.objects.filter(
        fecha__date=hoy
    ).select_related(
        'cliente',
        'usuario'
    ).order_by('-fecha')

    total_general = ventas.aggregate(
        total=Sum('total')
    )['total'] or 0

    cantidad_ventas = ventas.count()

    efectivo = ventas.filter(
        metodo_pago='efectivo'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    debito = ventas.filter(
        metodo_pago='debito'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    credito = ventas.filter(
        metodo_pago='credito'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    transferencia = ventas.filter(
        metodo_pago='transferencia'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    return render(
        request,
        'caja.html',
        {
            'ventas': ventas,
            'total_general': total_general,
            'cantidad_ventas': cantidad_ventas,
            'efectivo': efectivo,
            'debito': debito,
            'credito': credito,
            'transferencia': transferencia
        }
    )