# config.py

# Este archivo contiene las constantes de configuración para la aplicación. w

import os

# --- Paleta de Colores ---
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
COLOR_ERROR_TEXT = "#D8000C"

# --- Rutas y Nombres de Archivo ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Directorio raíz del proyecto

# NUEVO: Directorio para recursos como logos e iconos
ASSETS_DIR_NAME = "assets"
ASSETS_PATH = os.path.join(BASE_DIR, ASSETS_DIR_NAME)

# Directorio para las imágenes de los productos
IMAGENES_PRODUCTOS_DIR_NAME = "imagenes_productos"
IMAGENES_PRODUCTOS_PATH = os.path.join(BASE_DIR, IMAGENES_PRODUCTOS_DIR_NAME)

# Directorio para los manuales de los productos (PDFs locales)
MANUALES_PRODUCTOS_DIR_NAME = "manuales_productos"
MANUALES_PRODUCTOS_PATH = os.path.join(BASE_DIR, MANUALES_PRODUCTOS_DIR_NAME)

# Archivo de log de Excel
EXCEL_LOG_FILENAME = "registro_actividad_balanzas.xlsx"
LOGS_DIR_NAME = "logs"
LOGS_PATH = os.path.join(BASE_DIR, LOGS_DIR_NAME)
EXCEL_LOG_FILE_FULL_PATH = os.path.join(LOGS_PATH, EXCEL_LOG_FILENAME)

# Crear las carpetas necesarias si no existen
paths_to_create = [
    ASSETS_PATH, # Asegurar que se cree la carpeta de assets
    IMAGENES_PRODUCTOS_PATH,
    MANUALES_PRODUCTOS_PATH,
    LOGS_PATH
]
for path in paths_to_create:
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
            print(f"INFO (config.py): Directorio creado: {path}")
        except OSError as e:
            print(f"ADVERTENCIA (config.py): No se pudo crear el directorio '{path}': {e}")