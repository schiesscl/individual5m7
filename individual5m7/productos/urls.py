from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    # Ejercicio 1: Listar todos los productos
    path('', views.listar_productos, name='listar'),
    
    # Ejercicio 2: Productos con filtros
    path('filtrados/', views.productos_filtrados, name='filtrados'),
    
    # Ejercicio 3: Query SQL con raw()
    path('raw/', views.productos_raw, name='raw'),
    
    # Ejercicio 4: Mapeo de campos con raw()
    path('raw-mapeo/', views.productos_raw_mapeo, name='raw_mapeo'),
    
    # Ejercicio 6: Exclusión de campos
    path('sin-disponible/', views.productos_sin_disponible, name='sin_disponible'),
    
    # Ejercicio 7: Productos con impuesto (anotaciones)
    path('con-impuesto/', views.productos_con_impuesto, name='con_impuesto'),
    
    # Ejercicio 8: raw() con parámetros
    path('raw-parametros/', views.productos_raw_parametros, name='raw_parametros'),
    
    # Ejercicio 9: Insertar producto con SQL directo
    path('insertar-sql/', views.insertar_producto_sql, name='insertar_sql'),
    path('actualizar/<int:producto_id>/', views.actualizar_producto_sql, name='actualizar_sql'),
    
    # Ejercicio 10: Listar con cursor
    path('cursor/', views.listar_con_cursor, name='cursor'),
    
    # Ejercicio 11: Procedimientos almacenados
    path('procedimiento/', views.productos_procedimiento, name='procedimiento'),
]