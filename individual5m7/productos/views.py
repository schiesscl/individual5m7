from django.shortcuts import render
from .models import Producto
from django.db.models import F, ExpressionWrapper, DecimalField, Q, Value
from django.db import connection
from decimal import Decimal

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
    """
    Ejercicio 3: Ejecutando Queries SQL desde Django
    Muestra productos con precio menor a $50 usando raw()
    """
    productos = Producto.objects.raw('SELECT * FROM productos_producto WHERE precio < 50')
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
    """
    Ejercicio 7: Añadiendo Anotaciones en Consultas
    Agrega un campo calculado con el precio más 16% de impuesto
    """
    productos = Producto.objects.annotate(
        precio_con_impuesto=ExpressionWrapper(
            F('precio') * Value(Decimal('1.19')),
            output_field=DecimalField(max_digits=10, decimal_places=2)
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

# Ejercicio 9: SQL personalizado con cursor
def insertar_producto_sql(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        disponible = request.POST.get('disponible', True)
        
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO productos_producto (nombre, precio, disponible) VALUES (%s, %s, %s)",
                [nombre, precio, disponible]
            )
        
        return HttpResponse("Producto insertado correctamente")
    
    return render(request, 'productos/insertar_sql.html')

def actualizar_producto_sql(request, producto_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE productos_producto SET precio = precio * 1.10 WHERE id = %s",
            [producto_id]
        )
    
    return HttpResponse(f"Producto {producto_id} actualizado")

# Ejercicio 10: Conexiones y cursores
def listar_con_cursor(request):
    productos_data = []
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nombre, precio, disponible FROM productos_producto")
        
        # Recuperar datos
        columns = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            productos_data.append(dict(zip(columns, row)))
    
    return render(request, 'productos/cursor.html', {'productos': productos_data})

# Ejercicio 11: Procedimientos almacenados
def productos_procedimiento(request):
    precio_minimo = request.GET.get('precio_min', 50)
    productos_data = []
    
    with connection.cursor() as cursor:
        # Llamar al procedimiento almacenado
        cursor.callproc('obtener_productos_por_precio', [precio_minimo])
        
        # Obtener resultados
        for row in cursor.fetchall():
            productos_data.append({
                'id': row[0],
                'nombre': row[1],
                'precio': row[2],
                'disponible': row[3]
            })
    
    return render(request, 'productos/procedimiento.html', {
        'productos': productos_data,
        'precio_minimo': precio_minimo
    })
