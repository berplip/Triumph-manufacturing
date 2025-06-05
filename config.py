# config.py
# Este archivo contiene las constantes de configuración para la aplicación.

import os

# --- Paleta de Colores (sin cambios) ---
COLOR_HEADER_BG = "#0A234D"
COLOR_HEADER_FG = "white"
COLOR_ACCENT = "#F39C12"
COLOR_BACKGROUND = "white"
COLOR_TEXT_GENERAL = "#333333"
COLOR_TEXT_ON_ACCENT = "white"
COLOR_LISTBOX_BG = "white"
COLOR_LISTBOX_FG = COLOR_TEXT_GENERAL
COLOR_LISTBOX_SELECT_BG = COLOR_ACCENT
COLOR_LISTBOX_SELECT_FG = COLOR_TEXT_ON_ACCENT
COLOR_TAB_INACTIVE_BG = "#E0E0E0"
COLOR_TAB_ACTIVE_BG = COLOR_HEADER_BG
COLOR_TAB_ACTIVE_FG = COLOR_HEADER_FG
COLOR_TAB_INACTIVE_FG = COLOR_TEXT_GENERAL
COLOR_ERROR_TEXT = "#D8000C" # Rojo para texto de error

# --- Rutas y Nombres de Archivo ---
# BASE_DIR será el directorio donde se encuentra este archivo config.py
# Asumimos que config.py está en la raíz del proyecto.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directorio para las imágenes de los productos
# AHORA APUNTA A UNA CARPETA 'imagenes_productos' DIRECTAMENTE EN LA RAÍZ DEL PROYECTO
IMAGENES_PRODUCTOS_DIR_NAME = "imagenes_productos"
IMAGENES_PRODUCTOS_PATH = os.path.join(BASE_DIR, IMAGENES_PRODUCTOS_DIR_NAME)

# Nombre del archivo de log de Excel
EXCEL_LOG_FILENAME = "registro_actividad_balanzas.xlsx"
LOGS_DIR_NAME = "logs"
LOGS_PATH = os.path.join(BASE_DIR, LOGS_DIR_NAME)
EXCEL_LOG_FILE_FULL_PATH = os.path.join(LOGS_PATH, EXCEL_LOG_FILENAME)

# Crear la carpeta de imágenes si no existe
if not os.path.exists(IMAGENES_PRODUCTOS_PATH):
    os.makedirs(IMAGENES_PRODUCTOS_PATH, exist_ok=True)

# La carpeta de logs también se crea en excel_logger.py, pero podemos asegurarla aquí también.
if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH, exist_ok=True)
