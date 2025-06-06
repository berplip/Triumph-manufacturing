# ui_components.py
# Módulo para la construcción y manejo de la interfaz gráfica (GUI).

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import datetime

# Importaciones de otros módulos del proyecto
import config
import data_manager
from auth_handler import autenticar_usuario
from excel_logger import registrar_accion_excel
from utils import abrir_enlace_web_util

# --- Variables de Módulo para Referencias a Widgets ---
app_principal_ref = None
entrada_modelo_busqueda_widget = None
lista_sugerencias_busqueda_widget = None
notebook_widget = None
tab_info_producto_widget = None
frame_info_producto_dinamico = None
lbl_total_stock_widget = None
campos_edicion_producto_actual = {}
style_aplicacion_global = None

# --- Funciones Auxiliares de UI ---
def _limpiar_frame_contenido_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    campos_edicion_producto_actual.clear()

def actualizar_sugerencias_ui(event=None):
    if entrada_modelo_busqueda_widget and lista_sugerencias_busqueda_widget:
        texto_busqueda = entrada_modelo_busqueda_widget.get().strip().lower()
        lista_sugerencias_busqueda_widget.delete(0, tk.END)
        productos_dict = data_manager.get_productos_data()
        if texto_busqueda:
            sugerencias = [p for p in productos_dict.keys() if p.lower().startswith(texto_busqueda)]
        else:
            sugerencias = sorted(productos_dict.keys())
        for s in sugerencias: lista_sugerencias_busqueda_widget.insert(tk.END, s)

def _calcular_y_actualizar_total_stock_ui():
    if lbl_total_stock_widget and data_manager.usuario_actual["rol"] == "administrador":
        total = sum(int(d.get("stock", 0)) for d in data_manager.get_productos_data().values())
        lbl_total_stock_widget.config(text=f"Stock Total Global: {total} unidades")

# --- Funciones CRUD de Productos (con interacción UI) ---
def _guardar_cambios_producto_ui_accion(nombre_producto_original):
    productos_dict_actuales = data_manager.get_productos_data()
    if nombre_producto_original not in productos_dict_actuales:
        messagebox.showerror("Error", f"Producto '{nombre_producto_original}' no encontrado.", parent=app_principal_ref)
        return
    try:
        datos_para_actualizar_crud = {}
        cambios_detectados_log_crud = []
        producto_actual_en_db = productos_dict_actuales[nombre_producto_original]

        for key, entry_widget_crud in campos_edicion_producto_actual.items():
            valor_actual_en_db = str(producto_actual_en_db.get(key, ''))
            valor_nuevo_del_widget = entry_widget_crud.get("1.0", tk.END).strip() if isinstance(entry_widget_crud, tk.Text) else entry_widget_crud.get().strip()
            
            if key == "stock":
                if not valor_nuevo_del_widget.isdigit():
                    messagebox.showerror("Error de Validación", "Stock debe ser número entero.", parent=app_principal_ref); return
                valor_nuevo_parsed = int(valor_nuevo_del_widget)
                if valor_nuevo_parsed != int(valor_actual_en_db if valor_actual_en_db.isdigit() else -1):
                    cambios_detectados_log_crud.append(f"{key}: '{valor_actual_en_db}' -> '{valor_nuevo_parsed}'")
                datos_para_actualizar_crud[key] = valor_nuevo_parsed
            else:
                if valor_nuevo_del_widget != valor_actual_en_db:
                    cambios_detectados_log_crud.append(f"{key}: '{valor_actual_en_db}' -> '{valor_nuevo_del_widget}'")
                datos_para_actualizar_crud[key] = valor_nuevo_del_widget
        
        if not cambios_detectados_log_crud:
            messagebox.showinfo("Sin Cambios", "No se detectaron cambios para guardar.", parent=app_principal_ref); return

        if data_manager.actualizar_producto_data(nombre_producto_original, datos_para_actualizar_crud):
            detalle_log = f"Producto: {nombre_producto_original}. Cambios: {'; '.join(cambios_detectados_log_crud)}"
            registrar_accion_excel("Edicion Producto (Guardado)", detalle_log)
            messagebox.showinfo("Éxito", f"Producto '{nombre_producto_original}' actualizado.", parent=app_principal_ref)
            _calcular_y_actualizar_total_stock_ui()
            mostrar_informacion_producto_seleccionado_ui() 
        else:
            messagebox.showerror("Error", "No se pudo actualizar el producto en el gestor de datos.", parent=app_principal_ref)

    except KeyError as ke: messagebox.showerror("Error de Campo", f"Falta campo: {ke}", parent=app_principal_ref)
    except Exception as e: messagebox.showerror("Error", f"No se guardaron cambios: {e}", parent=app_principal_ref)

def _eliminar_producto_ui_accion(nombre_producto):
    if nombre_producto in data_manager.get_productos_data():
        if messagebox.askyesno("Confirmar Eliminación", f"¿Eliminar '{nombre_producto}'?", parent=app_principal_ref):
            if data_manager.eliminar_producto_data(nombre_producto):
                registrar_accion_excel("Eliminacion Producto", f"Producto: {nombre_producto}")
                messagebox.showinfo("Eliminado", f"Producto '{nombre_producto}' eliminado.", parent=app_principal_ref)
                _limpiar_frame_contenido_widgets(frame_info_producto_dinamico)
                ttk.Label(frame_info_producto_dinamico, text="Producto eliminado. Seleccione otro.", style="Info.TLabel", justify=tk.CENTER).pack(expand=True, padx=20, pady=20)
                actualizar_sugerencias_ui()
                _calcular_y_actualizar_total_stock_ui()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto del gestor de datos.", parent=app_principal_ref)
    else: messagebox.showerror("Error", "No hay producto seleccionado.", parent=app_principal_ref)

def _abrir_ventana_registrar_producto_ui_accion():
    ventana_reg = tk.Toplevel(app_principal_ref)
    ventana_reg.title("Registrar Nuevo Producto")
    ventana_reg.geometry("500x600")
    ventana_reg.configure(background=config.COLOR_BACKGROUND)
    ventana_reg.grab_set()
    
    reg_style = ttk.Style(ventana_reg)
    reg_style.theme_use(style_aplicacion_global.theme_use())
    reg_style.configure("Reg.TFrame", background=config.COLOR_BACKGROUND)
    reg_style.configure("Reg.TLabel", background=config.COLOR_BACKGROUND, font=("Arial", 10))
    reg_style.configure("Reg.TEntry", font=("Arial", 10), padding=3)

    main_frame_reg = ttk.Frame(ventana_reg, style="Reg.TFrame", padding=15)
    main_frame_reg.pack(expand=True, fill="both")
    ttk.Label(main_frame_reg, text="Registrar Nuevo Producto", font=("Arial", 14, "bold"), background=config.COLOR_BACKGROUND, foreground=config.COLOR_HEADER_BG).pack(pady=(0,15))
    
    campos_reg_defs_ui = ["Nombre Producto:", "Serie:", "Manual (URL):", "Calibración (URL):", "Batería:", "Info Adicional:", "Imagen (ej: nombre.png):", "Stock Inicial:"]
    entries_reg_ui = {}
    for campo_text_ui in campos_reg_defs_ui:
        row_frame_ui = ttk.Frame(main_frame_reg, style="Reg.TFrame")
        row_frame_ui.pack(fill="x", pady=3)
        ttk.Label(row_frame_ui, text=campo_text_ui, style="Reg.TLabel", width=20).pack(side="left")
        key_reg_ui = campo_text_ui.split(":")[0].lower().replace(" (url)", "").replace(" (ej nombrepng)", "").replace(" ", "_")
        if campo_text_ui == "Info Adicional:": entry_ui = tk.Text(row_frame_ui, font=("Arial", 10), width=35, height=4, relief="solid", borderwidth=1, wrap="word")
        else: entry_ui = ttk.Entry(row_frame_ui, style="Reg.TEntry", width=35)
        entry_ui.pack(side="left", fill="x", expand=True)
        entries_reg_ui[key_reg_ui] = entry_ui
    
    def guardar_nuevo_prod_accion_interna():
        nuevo_nombre_prod = entries_reg_ui["nombre_producto"].get().strip()
        if not nuevo_nombre_prod: messagebox.showerror("Error", "Nombre del producto es obligatorio.", parent=ventana_reg); return
        if nuevo_nombre_prod in data_manager.get_productos_data(): messagebox.showerror("Error", f"Producto '{nuevo_nombre_prod}' ya existe.", parent=ventana_reg); return
        try:
            stock_str_reg_ui = entries_reg_ui["stock_inicial"].get()
            if not stock_str_reg_ui.isdigit() or int(stock_str_reg_ui) < 0: messagebox.showerror("Error", "Stock debe ser número >= 0.", parent=ventana_reg); return
            
            nuevo_producto_datos_reg = {
                "serie": entries_reg_ui["serie"].get(), "manual": entries_reg_ui["manual"].get(),
                "calibracion": entries_reg_ui["calibracion"].get(), "bateria": entries_reg_ui["bateria"].get(),
                "info": entries_reg_ui["info_adicional"].get("1.0", tk.END).strip(),
                "imagen": entries_reg_ui["imagen"].get(),
                "stock": int(stock_str_reg_ui)
            }
            
            if data_manager.registrar_producto_data(nuevo_nombre_prod, nuevo_producto_datos_reg):
                registrar_accion_excel("Registro Producto", f"Producto: {nuevo_nombre_prod}, Stock: {nuevo_producto_datos_reg['stock']}")
                messagebox.showinfo("Éxito", f"Producto '{nuevo_nombre_prod}' registrado.", parent=ventana_reg)
                actualizar_sugerencias_ui(); _calcular_y_actualizar_total_stock_ui(); ventana_reg.destroy()
            else: messagebox.showerror("Error", f"No se pudo registrar '{nuevo_nombre_prod}'.", parent=ventana_reg)
        except Exception as e: messagebox.showerror("Error al Guardar", str(e), parent=ventana_reg)

    ttk.Button(main_frame_reg, text="Guardar Producto", command=guardar_nuevo_prod_accion_interna, style="Accent.TButton").pack(pady=20)
    entries_reg_ui["nombre_producto"].focus()

# --- Lógica Principal de la UI de la Enciclopedia ---
def mostrar_informacion_producto_seleccionado_ui(event=None):
    global campos_edicion_producto_actual
    _limpiar_frame_contenido_widgets(frame_info_producto_dinamico) 
    
    if not lista_sugerencias_busqueda_widget: return
    indices = lista_sugerencias_busqueda_widget.curselection()
    if not indices:
        ttk.Label(frame_info_producto_dinamico, text="Seleccione un producto (doble clic) para ver su información.", style="Info.TLabel", justify=tk.CENTER).pack(expand=True, padx=20, pady=20)
        return
        
    nombre_sel = lista_sugerencias_busqueda_widget.get(indices[0])
    datos_prod = data_manager.get_producto_data(nombre_sel)

    registrar_accion_excel("Consulta Producto", f"Producto: {nombre_sel}")

    if not datos_prod: messagebox.showerror("Error", f"Datos no encontrados para {nombre_sel}.", parent=app_principal_ref); return
    if notebook_widget and tab_info_producto_widget: notebook_widget.select(tab_info_producto_widget)

    main_info_frame = ttk.Frame(frame_info_producto_dinamico, style="Content.TFrame")
    main_info_frame.pack(expand=True, fill="both", padx=10, pady=10)
    text_frame = ttk.Frame(main_info_frame, style="Content.TFrame")
    text_frame.pack(side="left", fill="both", expand=True, padx=(0,10))
    
    image_display_frame = ttk.Frame(main_info_frame, style="Content.TFrame", width=220, height=270)
    image_display_frame.pack(side="right", fill="none", expand=False, padx=(10,0), anchor="ne")
    image_display_frame.pack_propagate(False)

    img_filename = datos_prod.get('imagen', '')
    if img_filename:
        try:
            ruta_img = os.path.join(config.IMAGENES_PRODUCTOS_PATH, img_filename)
            if os.path.exists(ruta_img):
                img_original_pil = Image.open(ruta_img)
                img_original_pil.thumbnail((200, 250)) 
                img_tk_render_obj = ImageTk.PhotoImage(img_original_pil)
                lbl_img_widget = tk.Label(image_display_frame, image=img_tk_render_obj, bg=config.COLOR_BACKGROUND)
                lbl_img_widget.image = img_tk_render_obj
                lbl_img_widget.pack(pady=5, padx=5, anchor="center")
            else:
                error_msg = f"(Imagen '{img_filename}' no encontrada)"
                ttk.Label(image_display_frame, text=error_msg, style="ErrorImage.TLabel", wraplength=180).pack(pady=10, padx=5, anchor="n")
        except Exception as e:
            error_detalle = f"(Error al procesar imagen: {e})"
            ttk.Label(image_display_frame, text=error_detalle, style="ErrorImage.TLabel", wraplength=180).pack(pady=10, padx=5, anchor="n")
    else:
        ttk.Label(image_display_frame, text="(Sin imagen asignada)", style="Info.TLabel").pack(pady=10, padx=5, anchor="n")
    
    ttk.Label(text_frame, text=f"Producto: {nombre_sel}", style="Info.Header.TLabel").pack(pady=(0, 10), anchor="nw")
    
    campos_def = {"serie": "Número de serie:", "manual": "Manual:", "calibracion": "Calibración:", "bateria": "Batería:", "info": "Info Adicional:", "imagen": "Archivo Imagen:", "stock": "Stock:"}
    
    for key, label_txt in campos_def.items():
        if data_manager.usuario_actual["rol"] != 'administrador' and key in ['imagen', 'stock']:
            continue
            
        item_f = ttk.Frame(text_frame, style="Content.TFrame")
        item_f.pack(fill="x", pady=3, anchor="nw")
        ttk.Label(item_f, text=label_txt, style="Info.Bold.TLabel", width=18).pack(side="left", anchor="nw", padx=(0,5))
        
        val_dato = str(datos_prod.get(key, ''))

        if data_manager.usuario_actual["rol"] == "administrador":
            if key == "info": 
                entry_w = tk.Text(item_f, font=("Arial", 10), width=30, height=3, relief="solid", borderwidth=1, wrap="word")
                entry_w.insert("1.0", val_dato)
            else: 
                entry_w = ttk.Entry(item_f, style="Search.TEntry", width=30)
                entry_w.insert(0, val_dato)
            entry_w.pack(side="left", fill="x", expand=True)
            campos_edicion_producto_actual[key] = entry_w
        else:
            # --- MODIFICADO: Lógica para mostrar "Disponible" o "No disponible" ---
            texto_a_mostrar = ''
            if key in ["manual", "calibracion"]:
                texto_a_mostrar = "Disponible" if val_dato.strip() else "No disponible"
            else:
                texto_a_mostrar = val_dato.strip() if val_dato.strip() else "No disponible"

            if key == "info":
                lbl_val_w = ttk.Label(item_f, text=texto_a_mostrar, style="Info.TLabel", wraplength=text_frame.winfo_width() - 150 if text_frame.winfo_width() > 150 else 250)
                lbl_val_w.pack(side="left", anchor="nw")
            else:
                ttk.Label(item_f, text=texto_a_mostrar, style="Info.TLabel").pack(side="left", anchor="nw")
            # --- FIN DE LA MODIFICACIÓN ---

    btns_enlaces_f = ttk.Frame(text_frame, style="Content.TFrame")
    btns_enlaces_f.pack(fill="x", pady=(15,5), anchor="nw")
    
    manual_valor = datos_prod.get('manual', '').strip()
    if manual_valor:
        ttk.Button(btns_enlaces_f, text="Ver Manual", style="Accent.TButton", command=lambda m=manual_valor: abrir_enlace_web_util(m, app_principal_ref)).pack(side="left", padx=(0,10))
    
    calibracion_valor = datos_prod.get('calibracion', '').strip()
    if calibracion_valor:
        ttk.Button(btns_enlaces_f, text="Ver Calibración", style="Accent.TButton", command=lambda c=calibracion_valor: abrir_enlace_web_util(c, app_principal_ref)).pack(side="left", padx=(0,10))

    if data_manager.usuario_actual["rol"] == "administrador":
        admin_acts_f = ttk.Frame(text_frame, style="Content.TFrame")
        admin_acts_f.pack(fill="x", pady=(10,5), anchor="nw", after=btns_enlaces_f)
        ttk.Button(admin_acts_f, text="Guardar Cambios", style="Accent.TButton", command=lambda np=nombre_sel: _guardar_cambios_producto_ui_accion(np)).pack(side="left", padx=(0,10))
        ttk.Button(admin_acts_f, text="Eliminar Producto", style="Accent.TButton", command=lambda np=nombre_sel: _eliminar_producto_ui_accion(np)).pack(side="left")

# --- Funciones para Construir las Ventanas Principales ---
def _intentar_login_ui_logic(entry_usuario, entry_contrasena, ventana_login_ref, app_main_ref, callback_exito_login_ref):
    usuario_ingresado_login = entry_usuario.get()
    contrasena_ingresada_login = entry_contrasena.get()
    info_usuario_autenticado = autenticar_usuario(usuario_ingresado_login, contrasena_ingresada_login)
    
    if info_usuario_autenticado:
        data_manager.usuario_actual.update(info_usuario_autenticado)
        data_manager.hora_inicio_sesion_actual = datetime.datetime.now()
        registrar_accion_excel("Inicio Sesion", f"Usuario: {data_manager.usuario_actual['nombre']}, Rol: {data_manager.usuario_actual['rol']}")
        ventana_login_ref.destroy()
        app_main_ref.deiconify()
        callback_exito_login_ref(app_main_ref)
    else:
        messagebox.showerror("Error de Inicio de Sesión", "Usuario o contraseña incorrectos.", parent=ventana_login_ref)

def crear_ventana_login_ui(app_principal_arg, callback_exito_login_arg):
    global app_principal_ref 
    app_principal_ref = app_principal_arg
    app_principal_ref.withdraw()

    ventana_login_ui = tk.Toplevel(app_principal_ref)
    ventana_login_ui.title("Inicio de Sesión")
    ventana_login_ui.geometry("400x280")
    ventana_login_ui.resizable(False, False)
    ventana_login_ui.configure(background=config.COLOR_BACKGROUND)
    ventana_login_ui.grab_set()
    ventana_login_ui.protocol("WM_DELETE_WINDOW", lambda: on_app_close_ui())

    login_ui_style_local = ttk.Style(ventana_login_ui)
    try: login_ui_style_local.theme_use('clam') 
    except tk.TclError: login_ui_style_local.theme_use('default')
    login_ui_style_local.configure("Login.TFrame", background=config.COLOR_BACKGROUND)
    login_ui_style_local.configure("Login.Header.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_HEADER_BG, font=("Arial", 16, "bold"))
    login_ui_style_local.configure("Login.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_TEXT_GENERAL, font=("Arial", 11))
    login_ui_style_local.configure("Login.TEntry", font=("Arial", 11), padding=5)
    login_ui_style_local.configure("Login.TButton", font=("Arial", 11, "bold"), background=config.COLOR_ACCENT, foreground=config.COLOR_TEXT_ON_ACCENT, padding=(10,5))
    login_ui_style_local.map("Login.TButton", background=[('active', '#E88B0A')])
    
    login_main_frame = ttk.Frame(ventana_login_ui, style="Login.TFrame", padding=20)
    login_main_frame.pack(expand=True, fill="both")
    ttk.Label(login_main_frame, text="Acceso Enciclopedia", style="Login.Header.TLabel").pack(pady=(0, 20))
    ttk.Label(login_main_frame, text="Usuario:", style="Login.TLabel").pack(anchor="w", padx=10)
    entry_usuario_widget = ttk.Entry(login_main_frame, style="Login.TEntry", width=30)
    entry_usuario_widget.pack(pady=(0, 10), padx=10, fill="x")
    ttk.Label(login_main_frame, text="Contraseña:", style="Login.TLabel").pack(anchor="w", padx=10)
    entry_contrasena_widget = ttk.Entry(login_main_frame, style="Login.TEntry", show="*", width=30)
    entry_contrasena_widget.pack(pady=(0, 20), padx=10, fill="x")
    
    btn_ingresar_widget = ttk.Button(login_main_frame, text="Ingresar", style="Login.TButton", 
                              command=lambda: _intentar_login_ui_logic(entry_usuario_widget, entry_contrasena_widget, ventana_login_ui, app_principal_ref, callback_exito_login_arg))
    btn_ingresar_widget.pack(pady=10)
    
    ventana_login_ui.update_idletasks()
    x_pos_login = (ventana_login_ui.winfo_screenwidth() // 2) - (ventana_login_ui.winfo_width() // 2)
    y_pos_login = (ventana_login_ui.winfo_screenheight() // 2) - (ventana_login_ui.winfo_height() // 2)
    ventana_login_ui.geometry(f'+{x_pos_login}+{y_pos_login}')
    entry_usuario_widget.focus()

def inicializar_enciclopedia_ui(app_principal_arg):
    global app_principal_ref, entrada_modelo_busqueda_widget, lista_sugerencias_busqueda_widget, notebook_widget, tab_info_producto_widget, frame_info_producto_dinamico, lbl_total_stock_widget, style_aplicacion_global

    app_principal_ref = app_principal_arg 
    app_principal_ref.title(f"Balanzas Triunfo Enciclopedia - {data_manager.usuario_actual['nombre']} ({data_manager.usuario_actual['rol']})")
    app_principal_ref.protocol("WM_DELETE_WINDOW", on_app_close_ui)

    style_aplicacion_global = ttk.Style(app_principal_ref)
    try: style_aplicacion_global.theme_use('clam')
    except tk.TclError: style_aplicacion_global.theme_use('default')
    
    style_aplicacion_global.configure("Header.TFrame", background=config.COLOR_HEADER_BG)
    style_aplicacion_global.configure("Header.TLabel", background=config.COLOR_HEADER_BG, foreground=config.COLOR_HEADER_FG, font=("Arial", 20, "bold"), padding=(10,15))
    style_aplicacion_global.configure("TNotebook", background=config.COLOR_BACKGROUND, borderwidth=1)
    style_aplicacion_global.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[12, 6])
    style_aplicacion_global.map("TNotebook.Tab", background=[("selected", config.COLOR_TAB_ACTIVE_BG), ("!selected", config.COLOR_TAB_INACTIVE_BG)], foreground=[("selected", config.COLOR_TAB_ACTIVE_FG), ("!selected", config.COLOR_TAB_INACTIVE_FG)])
    style_aplicacion_global.configure("Content.TFrame", background=config.COLOR_BACKGROUND)
    style_aplicacion_global.configure("Search.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_TEXT_GENERAL, font=("Arial", 12, "bold"))
    style_aplicacion_global.configure("Search.TEntry", font=("Arial", 14), padding=(5,5))
    style_aplicacion_global.map("Search.TEntry", bordercolor=[('focus', config.COLOR_ACCENT)])
    style_aplicacion_global.configure("Info.Header.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_HEADER_BG, font=("Arial", 18, "bold"))
    style_aplicacion_global.configure("Info.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_TEXT_GENERAL, font=("Arial", 11))
    style_aplicacion_global.configure("Info.Bold.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_TEXT_GENERAL, font=("Arial", 11, "bold"))
    style_aplicacion_global.configure("Accent.TButton", font=("Arial", 11, "bold"), background=config.COLOR_ACCENT, foreground=config.COLOR_TEXT_ON_ACCENT, padding=(10,5), borderwidth=1)
    style_aplicacion_global.map("Accent.TButton", background=[('active', '#E88B0A'), ('pressed', '#D07D09')], relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
    style_aplicacion_global.configure("Admin.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_ACCENT, font=("Arial", 10, "bold"), padding=5)
    style_aplicacion_global.configure("ErrorImage.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_ERROR_TEXT, font=("Arial", 10, "italic"))

    frame_cabecera_main = ttk.Frame(app_principal_ref, style="Header.TFrame")
    frame_cabecera_main.pack(fill="x", side="top")
    ttk.Label(frame_cabecera_main, text="Balanzas Triunfo Enciclopedia", style="Header.TLabel").pack(pady=(5,10), side="left", padx=10)
    if data_manager.usuario_actual["rol"] == "administrador":
        btn_reg_prod = ttk.Button(frame_cabecera_main, text="Registrar Producto", style="Accent.TButton", command=_abrir_ventana_registrar_producto_ui_accion)
        btn_reg_prod.pack(side="right", padx=10, pady=10)
        lbl_total_stock_widget = ttk.Label(frame_cabecera_main, text="Stock Total Global: 0", style="Admin.TLabel")
        lbl_total_stock_widget.pack(side="right", padx=10, pady=10)
        _calcular_y_actualizar_total_stock_ui()

    notebook_main_frame = ttk.Frame(app_principal_ref, style="Content.TFrame", padding=(0,5,0,0))
    notebook_main_frame.pack(expand=True, fill='both')
    notebook_widget = ttk.Notebook(notebook_main_frame, style="TNotebook")
    
    tab_busqueda_main = ttk.Frame(notebook_widget, style="Content.TFrame", padding=20)
    notebook_widget.add(tab_busqueda_main, text='Buscar Producto')
    tab_info_producto_widget = ttk.Frame(notebook_widget, style="Content.TFrame", padding=0) 
    notebook_widget.add(tab_info_producto_widget, text='Información del Producto')
    notebook_widget.pack(expand=True, fill='both')

    ttk.Label(tab_busqueda_main, text="Ingrese el modelo de la balanza:", style="Search.TLabel").pack(pady=(0,10), anchor="w")
    entrada_modelo_busqueda_widget = ttk.Entry(tab_busqueda_main, style="Search.TEntry", width=45)
    entrada_modelo_busqueda_widget.pack(pady=(0,10), fill="x")
    entrada_modelo_busqueda_widget.bind("<KeyRelease>", actualizar_sugerencias_ui)
    
    frame_lista_sug = ttk.Frame(tab_busqueda_main, style="Content.TFrame")
    frame_lista_sug.pack(pady=10, fill="both", expand=True)
    lista_sugerencias_busqueda_widget = tk.Listbox(frame_lista_sug, font=("Arial", 12), width=38, height=10, bg=config.COLOR_LISTBOX_BG, fg=config.COLOR_LISTBOX_FG, selectbackground=config.COLOR_LISTBOX_SELECT_BG, selectforeground=config.COLOR_LISTBOX_SELECT_FG, borderwidth=1, relief="solid", exportselection=False)
    lista_sugerencias_busqueda_widget.pack(side="left", fill="both", expand=True)
    scrollbar_sug = ttk.Scrollbar(frame_lista_sug, orient="vertical", command=lista_sugerencias_busqueda_widget.yview)
    scrollbar_sug.pack(side="right", fill="y")
    lista_sugerencias_busqueda_widget.config(yscrollcommand=scrollbar_sug.set)
    lista_sugerencias_busqueda_widget.bind("<Double-Button-1>", mostrar_informacion_producto_seleccionado_ui)
    
    actualizar_sugerencias_ui()

    frame_info_producto_dinamico = ttk.Frame(tab_info_producto_widget, style="Content.TFrame")
    frame_info_producto_dinamico.pack(expand=True, fill='both')
    mostrar_informacion_producto_seleccionado_ui() 
    
    entrada_modelo_busqueda_widget.focus()

def on_app_close_ui():
    if data_manager.hora_inicio_sesion_actual:
        duracion = datetime.datetime.now() - data_manager.hora_inicio_sesion_actual
        duracion_minutos = duracion.total_seconds() / 60
        registrar_accion_excel("Cierre Aplicacion", f"Usuario: {data_manager.usuario_actual.get('nombre', 'N/A')}", duracion_min=duracion_minutos)
    else:
        registrar_accion_excel("Cierre Aplicacion", "Sin inicio de sesion previo (cerrado desde login).")
    
    if app_principal_ref: 
        app_principal_ref.destroy()