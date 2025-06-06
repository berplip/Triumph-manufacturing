# main_app.py
# Punto de entrada principal de la aplicación Balanzas Triunfo Enciclopedia.

import tkinter as tk
# Importa configuraciones y módulos necesarios
from config import COLOR_BACKGROUND
from excel_logger import inicializar_excel_log
from ui_components import crear_ventana_login_ui, inicializar_enciclopedia_ui

if __name__ == "__main__":
    # 1. Inicializar el logger de Excel al arrancar la aplicaciónw
    # Esto asegura que el archivo y la carpeta de logs existan.
    inicializar_excel_log()

    # 2. Crear la ventana principal (raíz) de la aplicación Tkinter
    root_app = tk.Tk()
    root_app.geometry("900x700") # Tamaño inicial, ajustado para más contenido
    root_app.configure(background=COLOR_BACKGROUND)
    root_app.minsize(800, 600) # Tamaño mínimo permitido para la ventana
    root_app.iconbitmap("logo.ico")

    # 3. Iniciar con la ventana de login.
    # Se pasa 'root_app' y la función 'inicializar_enciclopedia_ui' como callback.
    # 'inicializar_enciclopedia_ui' se ejecutará si el login es exitoso.
    crear_ventana_login_ui(root_app, inicializar_enciclopedia_ui)

    # 4. Iniciar el bucle principal de Tkinter para que la aplicación corra y maneje eventos. w
    root_app.mainloop()
