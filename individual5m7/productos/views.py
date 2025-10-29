from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField
from .models import Producto

# Ejercicio 1: Recuperar todos los productos
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar.html', {'productos': productos})

# Ejercicio 2: Filtros
def productos_filtrados(request):
    # Productos con precio mayor a 50
    productos_caros = Producto.objects.filter(precio__gt=50)
    
    # Productos que empiezan con "A"
    productos_a = Producto.objects.filter(nombre__startswith='A')
    
    # Productos disponibles
    productos_disponibles = Producto.objects.filter(disponible=True)
    
    contexto = {
        'productos_caros': productos_caros,
        'productos_a': productos_a,
        'productos_disponibles': productos_disponibles
    }
    return render(request, 'productos/filtrados.html', contexto)

# Ejercicio 3: Query SQL con raw()
def productos_raw(request):
    productos = Producto.objects.raw('SELECT * FROM productos_producto WHERE precio < 100')
    return render(request, 'productos/raw.html', {'productos': productos})

# Ejercicio 4: Mapeo de campos con raw()
def productos_raw_mapeo(request):
    # Consulta SQL personalizada con campos específicos
    productos = Producto.objects.raw(
        'SELECT id, nombre, precio, disponible FROM productos_producto WHERE precio BETWEEN 20 AND 80'
    )
    return render(request, 'productos/raw_mapeo.html', {'productos': productos})

# Ejercicio 6: Exclusión de campos
def productos_sin_disponible(request):
    # defer() excluye campos de la consulta inicial
    productos = Producto.objects.defer('disponible').all()
    return render(request, 'productos/sin_disponible.html', {'productos': productos})

# Ejercicio 7: Anotaciones
def productos_con_impuesto(request):
    productos = Producto.objects.annotate(
        precio_con_impuesto=ExpressionWrapper(
            F('precio') * 1.16,
            output_field=DecimalField(max_digits=7, decimal_places=2)
        )
    )
    return render(request, 'productos/con_impuesto.html', {'productos': productos})

# Ejercicio 8: raw() con parámetros
def productos_raw_parametros(request):
    precio_minimo = request.GET.get('precio_min', 30)
    # Usando parámetros para evitar SQL injection
    productos = Producto.objects.raw(
        'SELECT * FROM productos_producto WHERE precio > %s',
        [precio_minimo]
    )
    return render(request, 'productos/raw_parametros.html', {
        'productos': productos,
        'precio_minimo': precio_minimo
    })
