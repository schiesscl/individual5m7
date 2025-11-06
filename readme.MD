# Ejercicio Individual - Módulo 7: Django ORM y SQL con MySQL
## Hans Schiess

Proyecto Django que implementa 11 ejercicios prácticos sobre el uso del ORM de Django, consultas SQL personalizadas, cursores y procedimientos almacenados con MySQL.

## 📋 Descripción del Proyecto

Este proyecto demuestra diferentes técnicas para interactuar con una base de datos MySQL desde Django, incluyendo:

- Uso del ORM de Django para operaciones CRUD
- Filtros y consultas avanzadas
- Consultas SQL directas con `raw()`
- Manejo de cursores y conexiones manuales
- Procedimientos almacenados
- Anotaciones y campos calculados
- Optimización de consultas con índices

## 🛠️ Tecnologías Utilizadas

- **Python 3.12**
- **Django 5.2.7**
- **MySQL 8.0+**
- **mysqlclient** (conector MySQL para Python)
- **Bootstrap 5.3.2** (Frontend)

## 📁 Estructura del Proyecto

```
individual5m7/
├── manage.py
├── individual5m7/
│   ├── __init__.py
│   ├── settings.py          # Configuración con MySQL
│   ├── urls.py              # URLs principales
│   ├── wsgi.py
│   └── asgi.py
└── productos/
    ├── models.py            # Modelo Producto
    ├── views.py             # Vistas para los 11 ejercicios
    ├── urls.py              # URLs de la app
    ├── admin.py             # Configuración del admin
    ├── migrations/
    │   └── 0001_initial.py
    └── templates/
        └── productos/
            ├── base.html
            ├── listar.html
            ├── filtrados.html
            ├── raw.html
            ├── raw_mapeo.html
            ├── sin_disponible.html
            ├── con_impuesto.html
            ├── raw_parametros.html
            ├── insertar_sql.html
            ├── cursor.html
            └── procedimiento.html
```

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd "M7_AE5_ABP-Ejercicio individual"
```

### 2. Crear y activar entorno virtual

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install django mysqlclient
```

### 4. Configurar MySQL

**Crear la base de datos:**

```sql
mysql -u root -p
```

```sql
CREATE DATABASE individual5m7_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Crear el procedimiento almacenado:**

```sql
USE individual5m7_db;

DELIMITER //
CREATE PROCEDURE obtener_productos_por_precio(IN precio_minimo DECIMAL(5,2))
BEGIN
    SELECT * FROM productos_producto WHERE precio >= precio_minimo;
END //
DELIMITER ;
```

### 5. Configurar Django

El archivo [`individual5m7/settings.py`](individual5m7/individual5m7/settings.py) ya está configurado con:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'individual5m7_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**Nota:** Ajusta `USER` y `PASSWORD` según tu configuración de MySQL.

### 6. Aplicar migraciones

```bash
cd individual5m7
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

### 8. Cargar datos de prueba (opcional)

Puedes agregar productos desde el panel de administración o usar el shell de Django:

```bash
python manage.py shell
```

```python
from productos.models import Producto

Producto.objects.create(nombre="Laptop", precio=899.99, disponible=True)
Producto.objects.create(nombre="Mouse", precio=25.50, disponible=True)
Producto.objects.create(nombre="Teclado", precio=45.00, disponible=False)
Producto.objects.create(nombre="Monitor", precio=299.99, disponible=True)
Producto.objects.create(nombre="Audífonos", precio=79.99, disponible=True)
Producto.objects.create(nombre="Webcam", precio=59.99, disponible=False)
Producto.objects.create(nombre="Alfombrilla", precio=15.99, disponible=True)
exit()
```

### 9. Ejecutar el servidor

```bash
python manage.py runserver
```

Accede a: `http://127.0.0.1:8000/productos/`

## 📚 Ejercicios Implementados

### Ejercicio 1: Recuperando Registros con Django ORM
**URL:** `/productos/`

Muestra todos los productos usando `Producto.objects.all()`

**Vista:** [`listar_productos`](individual5m7/productos/views.py)
**Template:** [`listar.html`](individual5m7/productos/templates/productos/listar.html)

---

### Ejercicio 2: Aplicando Filtros en Recuperación de Registros
**URL:** `/productos/filtrados/`

Implementa tres filtros diferentes:
- Productos con precio > $50: `filter(precio__gt=50)`
- Productos que empiezan con "A": `filter(nombre__startswith='A')`
- Productos disponibles: `filter(disponible=True)`

**Vista:** [`productos_filtrados`](individual5m7/productos/views.py)
**Template:** [`filtrados.html`](individual5m7/productos/templates/productos/filtrados.html)

---

### Ejercicio 3: Ejecutando Queries SQL desde Django
**URL:** `/productos/raw/`

Ejecuta una consulta SQL directa para obtener productos con precio < $50:

```python
Producto.objects.raw('SELECT * FROM productos_producto WHERE precio < 50')
```

**Vista:** [`productos_raw`](individual5m7/productos/views.py)
**Template:** [`raw.html`](individual5m7/productos/templates/productos/raw.html)

---

### Ejercicio 4: Mapeando Campos de Consultas al Modelo
**URL:** `/productos/raw-mapeo/`

Muestra cómo los campos del SQL se mapean a atributos del modelo:

```python
Producto.objects.raw(
    'SELECT id, nombre, precio, disponible FROM productos_producto WHERE precio BETWEEN 20 AND 80'
)
```

**Vista:** [`productos_raw_mapeo`](individual5m7/productos/views.py)
**Template:** [`raw_mapeo.html`](individual5m7/productos/templates/productos/raw_mapeo.html)

---

### Ejercicio 5: Realizando Búsquedas de Índice

El índice está definido en el modelo [`Producto`](individual5m7/productos/models.py):

```python
class Meta:
    indexes = [
        models.Index(fields=['nombre'], name='idx_nombre'),
    ]
```

Para verificar índices en MySQL:

```sql
SHOW INDEX FROM productos_producto;
```

**Beneficios:**
- ✅ Mejora la velocidad de búsquedas por nombre
- ✅ Optimiza filtros y ordenamiento
- ✅ Reduce el tiempo de consultas en tablas grandes

---

### Ejercicio 6: Exclusión de Campos del Modelo
**URL:** `/productos/sin-disponible/`

Usa `defer()` para excluir el campo `disponible` de la consulta inicial:

```python
Producto.objects.defer('disponible').all()
```

**Vista:** [`productos_sin_disponible`](individual5m7/productos/views.py)
**Template:** [`sin_disponible.html`](individual5m7/productos/templates/productos/sin_disponible.html)

---

### Ejercicio 7: Añadiendo Anotaciones en Consultas
**URL:** `/productos/con-impuesto/`

Calcula un campo adicional `precio_con_impuesto` (19% IVA):

```python
Producto.objects.annotate(
    precio_con_impuesto=ExpressionWrapper(
        F('precio') * Value(Decimal('1.19')),
        output_field=DecimalField(max_digits=10, decimal_places=2)
    )
)
```

**Vista:** [`productos_con_impuesto`](individual5m7/productos/views.py)
**Template:** [`con_impuesto.html`](individual5m7/productos/templates/productos/con_impuesto.html)

---

### Ejercicio 8: Pasando Parámetros a raw()
**URL:** `/productos/raw-parametros/?precio_min=30`

Demuestra el uso seguro de parámetros para prevenir SQL injection:

```python
Producto.objects.raw(
    'SELECT * FROM productos_producto WHERE precio > %s',
    [precio_minimo]
)
```

**Vista:** [`productos_raw_parametros`](individual5m7/productos/views.py)
**Template:** [`raw_parametros.html`](individual5m7/productos/templates/productos/raw_parametros.html)

---

### Ejercicio 9: Ejecutando SQL Personalizado Directamente
**URL:** `/productos/insertar-sql/`

Usa `connection.cursor()` para ejecutar INSERT directo:

```python
with connection.cursor() as cursor:
    cursor.execute(
        "INSERT INTO productos_producto (nombre, precio, disponible) VALUES (%s, %s, %s)",
        [nombre, precio, disponible]
    )
```

**Cuándo usar:**
- ✅ Operaciones masivas (bulk operations)
- ✅ Queries muy complejas
- ✅ Optimizaciones específicas de MySQL
- ❌ NO para operaciones CRUD simples

**Vista:** [`insertar_producto_sql`](individual5m7/productos/views.py)
**Template:** [`insertar_sql.html`](individual5m7/productos/templates/productos/insertar_sql.html)

---

### Ejercicio 10: Conexiones y Cursores
**URL:** `/productos/cursor/`

Demuestra el uso de cursores para recuperar datos manualmente:

```python
with connection.cursor() as cursor:
    cursor.execute("SELECT id, nombre, precio, disponible FROM productos_producto")
    columns = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        productos_data.append(dict(zip(columns, row)))
```

**Ventajas:**
- Control total sobre la consulta
- Eficiente para grandes volúmenes
- Características específicas de MySQL

**Desventajas:**
- No usa el ORM
- Menos portable
- No retorna instancias del modelo

**Vista:** [`listar_con_cursor`](individual5m7/productos/views.py)
**Template:** [`cursor.html`](individual5m7/productos/templates/productos/cursor.html)

---

### Ejercicio 11: Invocación a Procedimientos Almacenados
**URL:** `/productos/procedimiento/?precio_min=50`

Invoca el procedimiento almacenado `obtener_productos_por_precio`:

```python
with connection.cursor() as cursor:
    cursor.callproc('obtener_productos_por_precio', [precio_minimo])
    for row in cursor.fetchall():
        productos_data.append({
            'id': row[0],
            'nombre': row[1],
            'precio': row[2],
            'disponible': row[3]
        })
```

**Vista:** [`productos_procedimiento`](individual5m7/productos/views.py)
**Template:** [`procedimiento.html`](individual5m7/productos/templates/productos/procedimiento.html)

---

## 🎨 Interfaz de Usuario

Todas las vistas utilizan **Bootstrap 5.3.2** para un diseño responsivo y profesional.

### Navegación

La barra de navegación ([`base.html`](individual5m7/productos/templates/productos/base.html)) incluye enlaces a:

- Listar (Ejercicio 1)
- Filtrados (Ejercicio 2)
- Raw SQL (Ejercicio 3)
- Con Impuesto (Ejercicio 7)
- Cursor (Ejercicio 10)
- Procedimiento (Ejercicio 11)
- Admin Panel

### Características del Frontend

- ✅ Diseño responsivo (móvil y escritorio)
- ✅ Tablas con striped rows y hover effects
- ✅ Badges para estados (Disponible/No disponible)
- ✅ Alertas informativas con código de ejemplo
- ✅ Formularios estilizados
- ✅ Colores diferenciados por ejercicio

---

## 🔑 Panel de Administración

Accede al panel admin en: `http://127.0.0.1:8000/admin/`

**Funcionalidades:**
- ✅ Listar todos los productos
- ✅ Filtrar por disponibilidad
- ✅ Buscar por nombre
- ✅ Crear, editar y eliminar productos

Configurado en [`admin.py`](individual5m7/productos/admin.py):

```python
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('nombre',)
```

---

## 📝 Modelo de Datos

### Producto

Definido en [`models.py`](individual5m7/productos/models.py):

| Campo | Tipo | Características |
|-------|------|----------------|
| `id` | BigAutoField | Clave primaria (auto-generada) |
| `nombre` | CharField(100) | Nombre del producto |
| `precio` | DecimalField(5,2) | Precio con 2 decimales |
| `disponible` | BooleanField | Estado de disponibilidad (default: True) |

**Índices:**
- `idx_nombre` en el campo `nombre` para optimizar búsquedas

**Meta:**
```python
class Meta:
    db_table = 'productos_producto'
    indexes = [
        models.Index(fields=['nombre'], name='idx_nombre'),
    ]
```

---

## 🧪 Comandos Útiles

### Django

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell interactivo
python manage.py shell

# Ver SQL de migraciones
python manage.py sqlmigrate productos 0001

# Verificar problemas
python manage.py check
```

### MySQL

```bash
# Conectar a MySQL
mysql -u root -p

# Usar la base de datos
USE individual5m7_db;

# Ver tablas
SHOW TABLES;

# Ver estructura de tabla
DESCRIBE productos_producto;

# Ver índices
SHOW INDEX FROM productos_producto;

# Ver procedimientos
SHOW PROCEDURE STATUS WHERE Db = 'individual5m7_db';

# Ver código del procedimiento
SHOW CREATE PROCEDURE obtener_productos_por_precio;
```

---

## 📊 Conceptos Clave Aprendidos

### ORM vs SQL Directo

| Aspecto | ORM | SQL Directo |
|---------|-----|-------------|
| **Facilidad** | ✅ Alto nivel, pythónico | ⚠️ Requiere conocer SQL |
| **Portabilidad** | ✅ Entre diferentes DBMS | ❌ Específico de MySQL |
| **Rendimiento** | ⚠️ Puede ser menos eficiente | ✅ Control total |
| **Seguridad** | ✅ Protección automática | ⚠️ Requiere cuidado (SQL injection) |
| **Mantenibilidad** | ✅ Fácil de mantener | ⚠️ Más difícil |

### Cuándo usar cada técnica

**ORM (`objects.filter()`, `objects.all()`):**
- ✅ Operaciones CRUD estándar
- ✅ Filtros simples y medianos
- ✅ Relaciones entre modelos
- ✅ Desarrollo rápido

**raw():**
- ✅ Queries complejas que el ORM no soporta bien
- ✅ Aún necesitas objetos del modelo
- ✅ Optimizaciones específicas

**Cursores (`connection.cursor()`):**
- ✅ Operaciones masivas
- ✅ Queries extremadamente complejas
- ✅ Procedimientos almacenados
- ✅ No necesitas objetos del modelo

---

## 🔒 Seguridad

### Prevención de SQL Injection

❌ **NUNCA hagas esto:**
```python
# VULNERABLE
precio = request.GET.get('precio')
query = f"SELECT * FROM productos WHERE precio > {precio}"
```

✅ **SIEMPRE usa parámetros:**
```python
# SEGURO
precio = request.GET.get('precio')
productos = Producto.objects.raw(
    'SELECT * FROM productos_producto WHERE precio > %s',
    [precio]
)
```

---

## 🐛 Troubleshooting

### Error: ModuleNotFoundError: No module named 'productos'

**Solución:** Asegúrate de que la carpeta `productos` esté dentro de `individual5m7/`

### Error: Access denied for user 'root'@'localhost'

**Solución:** Verifica las credenciales en [`settings.py`](individual5m7/individual5m7/settings.py)

### Error: (2003) Can't connect to MySQL server

**Solución:** 
1. Verifica que MySQL esté corriendo
2. Comprueba el puerto (3306)
3. Revisa el firewall

### Error: PROCEDURE obtener_productos_por_precio does not exist

**Solución:** Ejecuta el script SQL para crear el procedimiento almacenado

---

## 📦 Dependencias

```txt
Django==5.2.7
mysqlclient==2.2.4
```

---

## 👨‍💻 Autor

Proyecto desarrollado como parte del **Módulo 7** del curso de **Python** en **Talento Digital**.

---

## 📄 Licencia

Este proyecto es de uso educativo.

---

## 🔄 Historial de Commits

```bash
git log --oneline
```

Commits sugeridos durante el desarrollo:

1. `Ejercicio 1: Modelo Producto creado`
2. `Ejercicios 2-8: Vistas con filtros, raw queries, anotaciones`
3. `Ejercicios 9-10: SQL directo con cursores`
4. `Ejercicio 11: Procedimientos almacenados`
5. `Configuración de URLs y admin`
6. `Templates Bootstrap completos`
7. `README actualizado con documentación completa`