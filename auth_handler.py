# auth_handler.py
# Lógica para la autenticación de usuarios.

import hashlib
from data_manager import get_usuarios_registrados_data # Importa datos de usuarios

def _generar_hash_contrasena(contrasena_texto_plano):
    """Función interna para generar hash (solo para referencia si se añaden usuarios programáticamente)."""
    return hashlib.sha256(contrasena_texto_plano.encode()).hexdigest()

def _verificar_contrasena_hash(contrasena_guardada_hash, contrasena_ingresada):
    """Verifica una contraseña ingresada contra un hash guardado."""
    contrasena_ingresada_hash = hashlib.sha256(contrasena_ingresada.encode()).hexdigest()
    return contrasena_guardada_hash == contrasena_ingresada_hash

def autenticar_usuario(nombre_usuario_ingresado, contrasena_ingresada):
    """
    Autentica un usuario.
    Retorna un diccionario con {'nombre': nombre, 'rol': rol} si es exitoso, sino None.
    """
    usuarios = get_usuarios_registrados_data()
    if nombre_usuario_ingresado in usuarios:
        datos_usuario_guardados = usuarios[nombre_usuario_ingresado]
        if _verificar_contrasena_hash(datos_usuario_guardados["contrasena_hash"], contrasena_ingresada):
            return {"nombre": nombre_usuario_ingresado, "rol": datos_usuario_guardados["rol"]}
    return None
