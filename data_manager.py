# data_manager.py
# Maneja los datos de la aplicación: productos, usuarios y estado de sesión.
# En esta versión, los datos están definidos directamente en este archivo.

import hashlib
# YA NO SE IMPORTA NADA DE CONFIG.PY RELACIONADO CON JSON

# --- Almacenamiento de Usuarios (directamente en el código) ---
# Contraseñas hasheadas: "pass123" para usuario1, "adminpass" para admin.
_usuarios_registrados = {
    "usuario1": {"contrasena_hash": hashlib.sha256("pass123".encode()).hexdigest(), "rol": "usuario"},
    "admin": {"contrasena_hash": hashlib.sha256("adminpass".encode()).hexdigest(), "rol": "administrador"}
    # Puedes agregar más usuarios aquí si es necesario, generando sus hashes
}

# --- Estado del Usuario Actual (global a este módulo) ---
usuario_actual = {"nombre": None, "rol": None}
hora_inicio_sesion_actual = None

# --- Diccionario de productos (directamente en el código) ---
# "manual": nombre del archivo PDF local (ej. "LP7516_manual.pdf") que debe estar en la carpeta definida en config.MANUALES_PRODUCTOS_PATH
# "calibracion": URL para el video.
# "imagen": nombre del archivo de imagen (ej. "LP7516.png") que debe estar en config.IMAGENES_PRODUCTOS_PATH
_productos = {
    "LP7516": {
        "serie": "666",
        "manual": "LP7516_manual.pdf",
        "calibracion": "https://www.youtube.com/watch?v=WJbHmguujdc&ab_channel=ONECOIN",
        "bateria": "4V4AH/20HR",
        "info": "Conector de 5 pines y RS232.",
        "imagen": "LP7516sec01.png",
        "stock": 10
    },
    "TCS-IND.": {
        "serie": "67890ABC",
        "manual": "TCS-IND_manual.pdf", # Ejemplo, podría estar vacío si no hay manual
        "calibracion": "https://www.youtube.com/watch?v=example_cal_video",
        "bateria": "Níquel",
        "info": "Indicador industrial versátil.",
        "imagen": "TCS-IND.png",
        "stock": 5
    },
    "XK ": {
        "serie": "123 ",
        "manual": "", # Sin manual local
        "calibracion": "", # Sin URL de calibración
        "bateria": "6V4AH",
        "info": "Indicador básico y económico.",
        "imagen": "XK.png",
        "stock": 25
    },
    "TRASPALETA": {
        "serie": "XYZ789",
        "manual": "TRASPALETA_manual.pdf",
        "calibracion": "",
        "bateria": "Batería recargable específica.",
        "info": "Balanza integrada en transpaleta manual.",
        "imagen": "TRASPALETA.png",
        "stock": 3
    }
    # Agrega más productos aquí directamente si es necesario
}

# --- Funciones Públicas para Acceder y Modificar Datos ---
def get_productos_data():
    """Retorna una copia del diccionario de productos."""
    return _productos.copy()

def get_producto_data(nombre_producto):
    """Retorna los datos de un producto específico (como una copia), o None."""
    producto = _productos.get(nombre_producto)
    return producto.copy() if producto else None

def get_usuarios_registrados_data():
    """Retorna una copia del diccionario de usuarios."""
    return _usuarios_registrados.copy()

def actualizar_producto_data(nombre_producto, datos_actualizados):
    """Actualiza un producto existente en el diccionario en memoria."""
    if nombre_producto in _productos:
        _productos[nombre_producto].update(datos_actualizados)
        print(f"INFO (data_manager): Producto '{nombre_producto}' actualizado en memoria.")
        return True
    print(f"ERROR (data_manager): Intento de actualizar producto no existente '{nombre_producto}'.")
    return False

def eliminar_producto_data(nombre_producto):
    """Elimina un producto del diccionario en memoria."""
    if nombre_producto in _productos:
        del _productos[nombre_producto]
        print(f"INFO (data_manager): Producto '{nombre_producto}' eliminado de memoria.")
        return True
    print(f"ERROR (data_manager): Intento de eliminar producto no existente '{nombre_producto}'.")
    return False

def registrar_producto_data(nombre_producto, datos_producto):
    """Registra un nuevo producto en el diccionario en memoria."""
    if nombre_producto not in _productos:
        _productos[nombre_producto] = datos_producto
        print(f"INFO (data_manager): Producto '{nombre_producto}' registrado en memoria.")
        return True
    print(f"ERROR (data_manager): Intento de registrar producto ya existente '{nombre_producto}'.")
    return False

# Las funciones inicializar_datos_productos e inicializar_datos_usuarios NO existen
# en esta versión porque los datos se definen directamente arriba y no se cargan desde JSON.
