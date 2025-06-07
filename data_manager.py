# data_manager.py
# Maneja la carga y guardado de datos desde archivos JSON.d

import json
import hashlib
from config import PRODUCTOS_JSON_PATH, USUARIOS_JSON_PATH
from auth_handler import _generar_hash_contrasena

# --- Estado del Usuario Actual (global a este módulo) ---
usuario_actual = {"nombre": None, "rol": None}
hora_inicio_sesion_actual = None

# --- Funciones de bajo nivel para manejar JSON ---
def _cargar_datos_json(ruta_archivo):
    """Carga datos desde un archivo JSON."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _guardar_datos_json(ruta_archivo, datos):
    """Guarda datos en un archivo JSON."""
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4)

# --- Funciones Públicas para Productos ---
# (Las funciones de productos no cambian)
def get_productos_data():
    return _cargar_datos_json(PRODUCTOS_JSON_PATH)

def get_producto_data(nombre_producto):
    productos = get_productos_data()
    return productos.get(nombre_producto)

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

# --- Funciones Públicas para Usuarios ---
def get_usuarios_registrados_data():
    return _cargar_datos_json(USUARIOS_JSON_PATH)

# --- NUEVAS FUNCIONES PARA GESTIÓN DE USUARIOS ---
def registrar_usuario(nombre_usuario, contrasena_plano):
    """Añade un nuevo usuario con su contraseña hasheada."""
    usuarios = get_usuarios_registrados_data()
    if nombre_usuario in usuarios:
        return False, "El nombre de usuario ya existe."
    
    nuevo_hash = _generar_hash_contrasena(contrasena_plano)
    usuarios[nombre_usuario] = {"contrasena_hash": nuevo_hash, "rol": "usuario"} # Por defecto, rol 'usuario'
    _guardar_datos_json(USUARIOS_JSON_PATH, usuarios)
    return True, "Usuario registrado con éxito."

def eliminar_usuario(nombre_usuario):
    """Elimina un usuario del sistema."""
    usuarios = get_usuarios_registrados_data()
    if nombre_usuario in usuarios:
        # Medida de seguridad: no permitir eliminar al único administrador.
        admins = [u for u, d in usuarios.items() if d.get("rol") == "administrador"]
        if usuarios[nombre_usuario].get("rol") == "administrador" and len(admins) <= 1:
            return False, "No se puede eliminar al único administrador."
        
        del usuarios[nombre_usuario]
        _guardar_datos_json(USUARIOS_JSON_PATH, usuarios)
        return True, "Usuario eliminado con éxito."
    return False, "El usuario no existe."