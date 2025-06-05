# data_manager.py
# Maneja los datos de la aplicación: productos, usuarios y estado de sesión.

import hashlib

# --- Almacenamiento de Usuarios ---
# Contraseñas hasheadas. Ejemplos: "pass123" y "adminpass"
_usuarios_registrados = {
    "usuario1": {"contrasena_hash": hashlib.sha256("pass123".encode()).hexdigest(), "rol": "usuario"},
    "admin": {"contrasena_hash": hashlib.sha256("adminpass".encode()).hexdigest(), "rol": "administrador"}
}

# --- Estado del Usuario Actual (global a este módulo) ---
usuario_actual = {"nombre": None, "rol": None}
hora_inicio_sesion_actual = None

# --- Diccionario de productos (global a este módulo) ---

# La clave "imagen" es el nombre del archivo (ej. "LP7516.png")

# que debe estar en la carpeta config.IMAGENES_PRODUCTOS_PATH
_productos = {
    "LP7516": {
        "serie": "666",
        "manual": "https://ipesa.pt/image/catalog/pdf/d4d0947362b0b836310638d2ade34873-698900275-00%20Manual%20Visor%20LP7516.pdf",
        "calibracion": "https://www.youtube.com/watch?v=WJbHmguujdc&ab_channel=ONECOIN",
        "bateria": "4V4AH/20HR",
        "info": "Conector de 5 pines y RS232.",
        "imagen": "LP7516sec01.png",
        "stock": 10
    },
    "TCS-IND.": {
        "serie": "67890ABC",
        "manual": "",
        "calibracion": "https://www.youtube.com/watch?v=example_cal_video",
        "bateria": "Níquel",
        "info": "Indicador industrial versátil.",
        "imagen": "TCS-IND.png",
        "stock": 5
    },
    "XK ": {
        "serie": "123 ",
        "manual": "https://www.example.com/xk_manual.pdf",
        "calibracion": "",
        "bateria": "6V4AH",
        "info": "Indicador básico y económico.",
        "imagen": "XK.png",
        "stock": 25
    },
    "TRASPALETA": {
        "serie": "XYZ789",
        "manual": "",
        "calibracion": "",
        "bateria": "Batería recargable específica.",
        "info": "Balanza integrada en transpaleta manual.",
        "imagen": "TRASPALETA.png",
        "stock": 3
    }
}

# --- Funciones Públicas para Acceder y Modificar Datos ---
def get_productos_data():
    """Retorna una copia del diccionario de productos para evitar modificación externa directa."""
    return _productos.copy() # Retorna una copia superficial

def get_producto_data(nombre_producto):
    """Retorna los datos de un producto específico, o None si no existe."""
    return _productos.get(nombre_producto)

def get_usuarios_registrados_data():
    """Retorna una copia del diccionario de usuarios."""
    return _usuarios_registrados.copy()

def actualizar_producto_data(nombre_producto, datos_actualizados):
    """Actualiza un producto existente. Retorna True si fue exitoso, False si no."""
    if nombre_producto in _productos:
        _productos[nombre_producto].update(datos_actualizados)
        return True
    return False

def eliminar_producto_data(nombre_producto):
    """Elimina un producto. Retorna True si fue exitoso, False si no."""
    if nombre_producto in _productos:
        del _productos[nombre_producto]
        return True
    return False

def registrar_producto_data(nombre_producto, datos_producto):
    """Registra un nuevo producto. Retorna True si fue exitoso, False si ya existía."""
    if nombre_producto not in _productos:
        _productos[nombre_producto] = datos_producto
        return True
    return False