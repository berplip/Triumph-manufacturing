# utils.py
# Funciones de utilidad general para la aplicación.

import webbrowser
from tkinter import messagebox
from excel_logger import registrar_accion_excel # Importar para registrar la acción

def abrir_enlace_web_util(url, app_parent_for_messagebox=None):
    """
    Abre una URL en el navegador predeterminado.
    Registra la acción.
    app_parent_for_messagebox es la ventana raíz para los messageboxes.
    """
    registrar_accion_excel("Intento Abrir Enlace Web", f"URL: {url}")
    if url and url.strip() and url.startswith(('http://', 'https://')):
        try:
            webbrowser.open(url, new=2)
        except Exception as e:
            messagebox.showerror("Error al Abrir Enlace", f"No se pudo abrir el enlace: {url}\nError: {e}", parent=app_parent_for_messagebox)
    else:
        messagebox.showinfo("Enlace no Disponible", "No hay un enlace válido para este recurso.", parent=app_parent_for_messagebox)

# Podrías añadir más utilidades aquí, por ejemplo, para formatear fechas, validar entradas, etc.