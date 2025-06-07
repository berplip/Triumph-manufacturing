# auth_handler.py
# Lógica de autenticación simplificada (sin hashes).

import data_manager

def autenticar_usuario(nombre_usuario_ingresado, contrasena_ingresada):
    """
    Autentica a un usuario comparando la contraseña en texto plano.
    Retorna un diccionario con los datos del usuario si es exitoso, sino None.
    """
    usuarios = data_manager.get_usuarios_registrados_data()
    if nombre_usuario_ingresado in usuarios:
        datos_usuario_guardados = usuarios[nombre_usuario_ingresado]
        
        # Comparación directa de contraseñas
        if datos_usuario_guardados.get("contrasena") == contrasena_ingresada:
            return {"nombre": nombre_usuario_ingresado, "rol": datos_usuario_guardados.get("rol")}
            
    return None