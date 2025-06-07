# data_manager.pylol
# Maneja la carga y guardado de datos desde archivos JSON (versión simplificada).

import json
from config import PRODUCTOS_JSON_PATH, USUARIOS_JSON_PATH

# --- Estado del Usuario Actual ---
usuario_actual = {"nombre": None, "rol": None}
hora_inicio_sesion_actual = None

# --- Funciones de bajo nivel para JSON ---
def _cargar_datos_json(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _guardar_datos_json(ruta_archivo, datos):
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4)

# --- Funciones para Productos (sin cambios) ---
def get_productos_data(): return _cargar_datos_json(PRODUCTOS_JSON_PATH)
def get_producto_data(nombre_producto): return get_productos_data().get(nombre_producto)
def actualizar_producto_data(nombre_producto, datos_actualizados):
    productos = get_productos_data()
    if nombre_producto in productos:
        productos[nombre_producto].update(datos_actualizados)
        _guardar_datos_json(PRODUCTOS_JSON_PATH, productos)
        return True
    return False
def eliminar_producto_data(nombre_producto):
    productos = get_productos_data()
    if nombre_producto in productos:
        del productos[nombre_producto]
        _guardar_datos_json(PRODUCTOS_JSON_PATH, productos)
        return True
    return False
def registrar_producto_data(nombre_producto, datos_producto):
    productos = get_productos_data()
    if nombre_producto not in productos:
        productos[nombre_producto] = datos_producto
        _guardar_datos_json(PRODUCTOS_JSON_PATH, productos)
        return True
    return False

# --- Funciones para Usuarios ---
def get_usuarios_registrados_data():
    return _cargar_datos_json(USUARIOS_JSON_PATH)

def guardar_o_actualizar_usuario(nombre_usuario, datos_usuario):
    """Guarda un nuevo usuario o actualiza los datos de uno existente."""
    usuarios = get_usuarios_registrados_data()
    # Protección: No se puede cambiar el rol del superadmin
    if nombre_usuario == "superadmin" and datos_usuario.get("rol") != "superadmin":
        return False, "No se puede cambiar el rol del Super Administrador."
    
    usuarios[nombre_usuario] = datos_usuario
    _guardar_datos_json(USUARIOS_JSON_PATH, usuarios)
    return True, f"Usuario '{nombre_usuario}' guardado con éxito."

def eliminar_usuario(nombre_usuario):
    """Elimina un usuario del sistema."""
    usuarios = get_usuarios_registrados_data()
    if nombre_usuario in usuarios:
        # Protección: No se puede eliminar al superadmin
        if nombre_usuario == "superadmin":
            return False, "No se puede eliminar al Super Administrador."
        
        del usuarios[nombre_usuario]
        _guardar_datos_json(USUARIOS_JSON_PATH, usuarios)
        return True, "Usuario eliminado con éxito."
    return False, "El usuario no existe."