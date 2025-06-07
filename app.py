# app.py
# Versión optimizada y orientada a objetos de la Enciclopedia Balanzas Triunfo.

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import datetime
import webbrowser
import pathlib

# Importaciones de otros módulos del proyecto
import config
import data_manager
from auth_handler import autenticar_usuario, _generar_hash_contrasena
from excel_logger import inicializar_excel_log, registrar_accion_excel

class App(tk.Tk):
    # (El __init__ y las funciones de configuración de la ventana y estilos no cambian)
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.campos_edicion_producto_actual = {}
        self.style = ttk.Style(self)
        self._configurar_estilos_globales()
        inicializar_excel_log()
        self._configurar_ventana_principal()
        self.crear_ventana_login()

    def _configurar_ventana_principal(self):
        self.title("Balanzas Triunfo Enciclopedia")
        self.geometry("900x700")
        self.configure(background=config.COLOR_BACKGROUND)
        self.minsize(800, 600)
        self.protocol("WM_DELETE_WINDOW", self._on_app_close)
        try:
            icon_path = os.path.join(config.IMAGENES_PRODUCTOS_PATH, "icono.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"No se pudo cargar el icono principal: {e}")

    def _configurar_estilos_globales(self):
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            self.style.theme_use('default')
        self.style.configure("Header.TFrame", background=config.COLOR_HEADER_BG)
        self.style.configure("Header.TLabel", background=config.COLOR_HEADER_BG, foreground=config.COLOR_HEADER_FG, font=("Arial", 20, "bold"), padding=(10, 15))
        self.style.configure("TNotebook", background=config.COLOR_BACKGROUND, borderwidth=1)
        self.style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[12, 6])
        self.style.map("TNotebook.Tab", background=[("selected", config.COLOR_TAB_ACTIVE_BG), ("!selected", config.COLOR_TAB_INACTIVE_BG)], foreground=[("selected", config.COLOR_TAB_ACTIVE_FG), ("!selected", config.COLOR_TAB_INACTIVE_FG)])
        self.style.configure("Content.TFrame", background=config.COLOR_BACKGROUND)
        self.style.configure("Search.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_TEXT_GENERAL, font=("Arial", 12, "bold"))
        self.style.configure("Search.TEntry", font=("Arial", 14), padding=(5,5))
        self.style.map("Search.TEntry", bordercolor=[('focus', config.COLOR_ACCENT)])
        self.style.configure("Info.Header.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_HEADER_BG, font=("Arial", 18, "bold"))
        self.style.configure("Info.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_TEXT_GENERAL, font=("Arial", 11))
        self.style.configure("Info.Bold.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_TEXT_GENERAL, font=("Arial", 11, "bold"))
        self.style.configure("Accent.TButton", font=("Arial", 11, "bold"), background=config.COLOR_ACCENT, foreground=config.COLOR_TEXT_ON_ACCENT, padding=(10,5), borderwidth=1)
        self.style.map("Accent.TButton", background=[('active', '#E88B0A'), ('pressed', '#D07D09')], relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        self.style.configure("Admin.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_ACCENT, font=("Arial", 10, "bold"), padding=5)
        self.style.configure("ErrorImage.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_ERROR_TEXT, font=("Arial", 10, "italic"))

    def crear_ventana_login(self):
        self.ventana_login = tk.Toplevel(self)
        self.ventana_login.title("Inicio de Sesión")
        self.ventana_login.geometry("400x280")
        self.ventana_login.resizable(False, False)
        self.ventana_login.configure(background=config.COLOR_BACKGROUND)
        self.ventana_login.grab_set()
        self.ventana_login.protocol("WM_DELETE_WINDOW", self._on_app_close)
        try:
            icon_path = os.path.join(config.IMAGENES_PRODUCTOS_PATH, "icono.ico")
            if os.path.exists(icon_path):
                self.ventana_login.iconbitmap(icon_path)
        except Exception as e:
            print(f"No se pudo cargar el icono para la ventana de login: {e}")
        style = ttk.Style(self.ventana_login)
        style.theme_use(self.style.theme_use())
        style.configure("Login.TFrame", background=config.COLOR_BACKGROUND)
        style.configure("Login.Header.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_HEADER_BG, font=("Arial", 16, "bold"))
        style.configure("Login.TLabel", background=config.COLOR_BACKGROUND, foreground=config.COLOR_TEXT_GENERAL, font=("Arial", 11))
        style.configure("Login.TEntry", font=("Arial", 11), padding=5)
        style.configure("Login.TButton", font=("Arial", 11, "bold"), background=config.COLOR_ACCENT, foreground=config.COLOR_TEXT_ON_ACCENT, padding=(10, 5))
        style.map("Login.TButton", background=[('active', '#E88B0A')])
        frame = ttk.Frame(self.ventana_login, style="Login.TFrame", padding=20)
        frame.pack(expand=True, fill="both")
        ttk.Label(frame, text="Acceso Enciclopedia", style="Login.Header.TLabel").pack(pady=(0, 20))
        ttk.Label(frame, text="Usuario:", style="Login.TLabel").pack(anchor="w", padx=10)
        entry_usuario = ttk.Entry(frame, style="Login.TEntry", width=30)
        entry_usuario.pack(pady=(0, 10), padx=10, fill="x")
        ttk.Label(frame, text="Contraseña:", style="Login.TLabel").pack(anchor="w", padx=10)
        entry_contrasena = ttk.Entry(frame, style="Login.TEntry", show="*", width=30)
        entry_contrasena.pack(pady=(0, 20), padx=10, fill="x")
        ttk.Button(frame, text="Ingresar", style="Login.TButton", command=lambda: self._intentar_login(entry_usuario, entry_contrasena)).pack(pady=10)
        self.ventana_login.update_idletasks()
        x = (self.ventana_login.winfo_screenwidth() // 2) - (self.ventana_login.winfo_width() // 2)
        y = (self.ventana_login.winfo_screenheight() // 2) - (self.ventana_login.winfo_height() // 2)
        self.ventana_login.geometry(f'+{x}+{y}')
        entry_usuario.focus()

    def _intentar_login(self, entry_usuario, entry_contrasena):
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        info_usuario = autenticar_usuario(usuario, contrasena)
        if info_usuario:
            data_manager.usuario_actual.update(info_usuario)
            data_manager.hora_inicio_sesion_actual = datetime.datetime.now()
            registrar_accion_excel("Inicio Sesion", f"Usuario: {data_manager.usuario_actual['nombre']}, Rol: {data_manager.usuario_actual['rol']}")
            self.ventana_login.destroy()
            self.deiconify()
            self.inicializar_enciclopedia()
        else:
            messagebox.showerror("Error de Inicio de Sesión", "Usuario o contraseña incorrectos.", parent=self.ventana_login)

    def inicializar_enciclopedia(self):
        """Construye la interfaz principal de la enciclopedia después del login."""
        self.title(f"Balanzas Triunfo Enciclopedia - {data_manager.usuario_actual['nombre']} ({data_manager.usuario_actual['rol']})")

        frame_cabecera = ttk.Frame(self, style="Header.TFrame")
        frame_cabecera.pack(fill="x", side="top")
        
        try:
            logo_path = os.path.join(config.IMAGENES_PRODUCTOS_PATH, "logo.png")
            if os.path.exists(logo_path):
                logo_pil = Image.open(logo_path)
                logo_pil.thumbnail((50, 50))
                self.logo_tk = ImageTk.PhotoImage(logo_pil)
                lbl_logo = ttk.Label(frame_cabecera, image=self.logo_tk, style="Header.TLabel")
                lbl_logo.pack(side="left", padx=(10, 5), pady=5)
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        ttk.Label(frame_cabecera, text="Balanzas Triunfo Enciclopedia", style="Header.TLabel").pack(pady=(5, 10), side="left", padx=10)
        
        # --- MODIFICADO: Contenedor para botones de admin ---
        admin_buttons_frame = ttk.Frame(frame_cabecera, style="Header.TFrame")
        admin_buttons_frame.pack(side="right", padx=10, pady=10)

        if data_manager.usuario_actual["rol"] == "administrador":
            # --- NUEVO: Botón para gestionar usuarios ---
            btn_gest_usr = ttk.Button(admin_buttons_frame, text="Gestionar Usuarios", style="Accent.TButton", command=self._abrir_ventana_gestion_usuarios)
            btn_gest_usr.pack(side="right", padx=(10, 0))
            
            btn_reg_prod = ttk.Button(admin_buttons_frame, text="Registrar Producto", style="Accent.TButton", command=self._abrir_ventana_registrar_producto)
            btn_reg_prod.pack(side="right", padx=(10, 0))
            
            self.lbl_total_stock = ttk.Label(frame_cabecera, text="Stock Total Global: 0", style="Admin.TLabel")
            self.lbl_total_stock.pack(side="right", padx=10)
            self._calcular_y_actualizar_total_stock()

        notebook_frame = ttk.Frame(self, style="Content.TFrame", padding=(0, 5, 0, 0))
        notebook_frame.pack(expand=True, fill='both')
        self.notebook = ttk.Notebook(notebook_frame, style="TNotebook")
        
        tab_busqueda = ttk.Frame(self.notebook, style="Content.TFrame", padding=20)
        self.tab_info_producto = ttk.Frame(self.notebook, style="Content.TFrame", padding=0)
        
        self.notebook.add(tab_busqueda, text='Buscar Producto')
        self.notebook.add(self.tab_info_producto, text='Información del Producto')
        self.notebook.pack(expand=True, fill='both')

        ttk.Label(tab_busqueda, text="Ingrese el modelo de la balanza:", style="Search.TLabel").pack(pady=(0, 10), anchor="w")
        self.entrada_modelo_busqueda = ttk.Entry(tab_busqueda, style="Search.TEntry", width=45)
        self.entrada_modelo_busqueda.pack(pady=(0, 10), fill="x")
        self.entrada_modelo_busqueda.bind("<KeyRelease>", self._actualizar_sugerencias)
        
        frame_lista = ttk.Frame(tab_busqueda, style="Content.TFrame")
        frame_lista.pack(pady=10, fill="both", expand=True)
        self.lista_sugerencias = tk.Listbox(frame_lista, font=("Arial", 12), width=38, height=10, bg=config.COLOR_LISTBOX_BG, fg=config.COLOR_LISTBOX_FG, selectbackground=config.COLOR_LISTBOX_SELECT_BG, selectforeground=config.COLOR_LISTBOX_SELECT_FG, borderwidth=1, relief="solid", exportselection=False)
        self.lista_sugerencias.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.lista_sugerencias.yview)
        scrollbar.pack(side="right", fill="y")
        self.lista_sugerencias.config(yscrollcommand=scrollbar.set)
        self.lista_sugerencias.bind("<Double-Button-1>", self._mostrar_informacion_producto)
        
        self._actualizar_sugerencias()

        self.frame_info_producto_dinamico = ttk.Frame(self.tab_info_producto, style="Content.TFrame")
        self.frame_info_producto_dinamico.pack(expand=True, fill='both')
        self._mostrar_informacion_producto()
        
        self.entrada_modelo_busqueda.focus()

    # --- NUEVA SECCIÓN: MÉTODOS PARA GESTIÓN DE USUARIOS ---

    def _abrir_ventana_gestion_usuarios(self):
        """Crea y muestra la ventana para gestionar usuarios."""
        win_gest = tk.Toplevel(self)
        win_gest.title("Gestión de Usuarios")
        win_gest.geometry("400x400")
        win_gest.resizable(False, False)
        win_gest.grab_set()

        main_frame = ttk.Frame(win_gest, padding=15)
        main_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_frame, text="Usuarios Registrados", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill="both", expand=True)
        
        user_listbox = tk.Listbox(list_frame, font=("Arial", 11))
        user_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=user_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        user_listbox.config(yscrollcommand=scrollbar.set)
        
        def refrescar_lista():
            user_listbox.delete(0, tk.END)
            usuarios = data_manager.get_usuarios_registrados_data()
            for u, d in usuarios.items():
                user_listbox.insert(tk.END, f"{u} ({d.get('rol', 'N/A')})")
        
        refrescar_lista()
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(btn_frame, text="Añadir Usuario", style="Accent.TButton", command=lambda: self._dialogo_anadir_usuario(win_gest, refrescar_lista)).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Eliminar Seleccionado", style="Accent.TButton", command=lambda: self._accion_eliminar_usuario(user_listbox, win_gest, refrescar_lista)).pack(side="left", expand=True, padx=5)

    def _dialogo_anadir_usuario(self, parent_window, callback_refresh):
        """Muestra un diálogo para añadir un nuevo usuario."""
        diag = tk.Toplevel(parent_window)
        diag.title("Añadir Nuevo Usuario")
        diag.geometry("350x200")
        diag.grab_set()

        frame = ttk.Frame(diag, padding=15)
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="Nombre de usuario:").pack(anchor="w")
        entry_user = ttk.Entry(frame)
        entry_user.pack(fill="x", pady=(0, 10))
        
        ttk.Label(frame, text="Contraseña:").pack(anchor="w")
        entry_pass = ttk.Entry(frame, show="*")
        entry_pass.pack(fill="x")
        
        def guardar_usuario():
            username = entry_user.get().strip()
            password = entry_pass.get().strip()
            if not username or not password:
                messagebox.showerror("Error", "Ambos campos son obligatorios.", parent=diag)
                return
            
            exito, mensaje = data_manager.registrar_usuario(username, password)
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=parent_window)
                registrar_accion_excel("Registro Usuario", f"Usuario añadido: {username}")
                callback_refresh()
                diag.destroy()
            else:
                messagebox.showerror("Error", mensaje, parent=diag)

        ttk.Button(frame, text="Guardar", style="Accent.TButton", command=guardar_usuario).pack(pady=20)
        entry_user.focus()

    def _accion_eliminar_usuario(self, listbox, parent_window, callback_refresh):
        """Lógica para eliminar el usuario seleccionado en la listbox."""
        indices = listbox.curselection()
        if not indices:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un usuario de la lista para eliminar.", parent=parent_window)
            return
            
        # Extraer solo el nombre de usuario de la cadena "nombre (rol)"
        usuario_a_eliminar = listbox.get(indices[0]).split(" ")[0]
        
        if usuario_a_eliminar == data_manager.usuario_actual.get("nombre"):
            messagebox.showerror("Error", "No puedes eliminarte a ti mismo.", parent=parent_window)
            return

        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar al usuario '{usuario_a_eliminar}'?", parent=parent_window):
            exito, mensaje = data_manager.eliminar_usuario(usuario_a_eliminar)
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=parent_window)
                registrar_accion_excel("Eliminación Usuario", f"Usuario eliminado: {usuario_a_eliminar}")
                callback_refresh()
            else:
                messagebox.showerror("Error", mensaje, parent=parent_window)

    # --- Métodos de la clase que reemplazan funciones antiguas ---
    # (El código interno es casi idéntico, solo que ahora son métodos)

    def _abrir_enlace(self, recurso):
        """Abre un recurso, que puede ser una URL web o un archivo PDF local."""
        registrar_accion_excel("Intento Abrir Recurso", f"Recurso: {recurso}")
        
        if not recurso or not recurso.strip():
            messagebox.showinfo("Recurso no Disponible", "No hay un enlace o archivo válido.", parent=self)
            return
        
        recurso = recurso.strip()
        if recurso.startswith(('http://', 'https://')):
            try:
                webbrowser.open(recurso, new=2)
            except Exception as e:
                messagebox.showerror("Error al Abrir Enlace", f"No se pudo abrir el enlace: {recurso}\nError: {e}", parent=self)
        else:
            ruta_completa = os.path.join(config.MANUALES_PRODUCTOS_PATH, recurso)
            if os.path.exists(ruta_completa):
                try:
                    uri = pathlib.Path(ruta_completa).as_uri()
                    webbrowser.open(uri)
                except Exception as e:
                    messagebox.showerror("Error al Abrir Archivo", f"No se pudo abrir el archivo: {recurso}\nError: {e}", parent=self)
            else:
                messagebox.showwarning("Archivo no Encontrado", f"El archivo '{recurso}' no fue encontrado.", parent=self)

    def _actualizar_sugerencias(self, event=None):
        texto_busqueda = self.entrada_modelo_busqueda.get().strip().lower()
        self.lista_sugerencias.delete(0, tk.END)
        productos = data_manager.get_productos_data()
        
        if texto_busqueda:
            sugerencias = [p for p in productos.keys() if p.lower().startswith(texto_busqueda)]
        else:
            sugerencias = sorted(productos.keys())
        
        for s in sugerencias:
            self.lista_sugerencias.insert(tk.END, s)

    def _mostrar_informacion_producto(self, event=None):
        for widget in self.frame_info_producto_dinamico.winfo_children():
            widget.destroy()
        self.campos_edicion_producto_actual.clear()
        indices = self.lista_sugerencias.curselection()
        if not indices:
            ttk.Label(self.frame_info_producto_dinamico, text="Seleccione un producto para ver su información.", style="Info.TLabel", justify=tk.CENTER).pack(expand=True, padx=20, pady=20)
            return
        nombre_sel = self.lista_sugerencias.get(indices[0])
        datos_prod = data_manager.get_producto_data(nombre_sel)
        if not datos_prod:
            messagebox.showerror("Error", f"No se encontraron datos para {nombre_sel}", parent=self)
            return
        registrar_accion_excel("Consulta Producto", f"Producto: {nombre_sel}")
        self.notebook.select(self.tab_info_producto)
        main_frame = ttk.Frame(self.frame_info_producto_dinamico, style="Content.TFrame")
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        text_frame = ttk.Frame(main_frame, style="Content.TFrame")
        text_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        image_frame = ttk.Frame(main_frame, style="Content.TFrame", width=220, height=270)
        image_frame.pack(side="right", fill="none", expand=False, padx=(10, 0), anchor="ne")
        image_frame.pack_propagate(False)
        img_filename = datos_prod.get('imagen', '')
        if img_filename:
            try:
                ruta_img = os.path.join(config.IMAGENES_PRODUCTOS_PATH, img_filename)
                if os.path.exists(ruta_img):
                    img_pil = Image.open(ruta_img)
                    img_pil.thumbnail((200, 250))
                    self.img_tk = ImageTk.PhotoImage(img_pil)
                    lbl_img = tk.Label(image_frame, image=self.img_tk, bg=config.COLOR_BACKGROUND)
                    lbl_img.pack(pady=5, padx=5, anchor="center")
                else:
                    ttk.Label(image_frame, text=f"(Imagen '{img_filename}' no encontrada)", style="ErrorImage.TLabel", wraplength=180).pack(pady=10, padx=5)
            except Exception as e:
                ttk.Label(image_frame, text=f"(Error al procesar imagen: {e})", style="ErrorImage.TLabel", wraplength=180).pack(pady=10, padx=5)
        else:
            ttk.Label(image_frame, text="(Sin imagen asignada)", style="Info.TLabel").pack(pady=10, padx=5)
        ttk.Label(text_frame, text=f"Producto: {nombre_sel}", style="Info.Header.TLabel").pack(pady=(0, 10), anchor="nw")
        campos_def = {"serie": "Número de serie:", "manual": "Manual:", "calibracion": "Calibración:", "bateria": "Batería:", "info": "Info Adicional:", "imagen": "Archivo Imagen:", "stock": "Stock:"}
        for key, label_txt in campos_def.items():
            if data_manager.usuario_actual["rol"] != 'administrador' and key in ['imagen', 'stock']:
                continue
            item_f = ttk.Frame(text_frame, style="Content.TFrame")
            item_f.pack(fill="x", pady=3, anchor="nw")
            ttk.Label(item_f, text=label_txt, style="Info.Bold.TLabel", width=18).pack(side="left", anchor="nw", padx=(0, 5))
            val_dato = str(datos_prod.get(key, ''))
            if data_manager.usuario_actual["rol"] == "administrador":
                if key == "info":
                    entry_w = tk.Text(item_f, font=("Arial", 10), width=30, height=3, relief="solid", borderwidth=1, wrap="word")
                    entry_w.insert("1.0", val_dato)
                else:
                    entry_w = ttk.Entry(item_f, style="Search.TEntry", width=30)
                    entry_w.insert(0, val_dato)
                entry_w.pack(side="left", fill="x", expand=True)
                self.campos_edicion_producto_actual[key] = entry_w
            else:
                texto_a_mostrar = ''
                if key in ["manual", "calibracion"]:
                    texto_a_mostrar = "Disponible" if val_dato.strip() else "No disponible"
                else:
                    texto_a_mostrar = val_dato.strip() if val_dato.strip() else "(No especificado)"
                if key == "info":
                    lbl_val = ttk.Label(item_f, text=texto_a_mostrar, style="Info.TLabel", wraplength=450)
                    lbl_val.pack(side="left", anchor="nw")
                else:
                    ttk.Label(item_f, text=texto_a_mostrar, style="Info.TLabel").pack(side="left", anchor="nw")
        btns_frame = ttk.Frame(text_frame, style="Content.TFrame")
        btns_frame.pack(fill="x", pady=(15, 5), anchor="nw")
        if datos_prod.get('manual', '').strip():
            ttk.Button(btns_frame, text="Ver Manual", style="Accent.TButton", command=lambda m=datos_prod.get('manual'): self._abrir_enlace(m)).pack(side="left", padx=(0, 10))
        if datos_prod.get('calibracion', '').strip():
            ttk.Button(btns_frame, text="Ver Calibración", style="Accent.TButton", command=lambda c=datos_prod.get('calibracion'): self._abrir_enlace(c)).pack(side="left", padx=(0, 10))
        if data_manager.usuario_actual["rol"] == "administrador":
            admin_btns_frame = ttk.Frame(text_frame, style="Content.TFrame")
            admin_btns_frame.pack(fill="x", pady=(10, 5), anchor="nw", after=btns_frame)
            ttk.Button(admin_btns_frame, text="Guardar Cambios", style="Accent.TButton", command=lambda: self._guardar_cambios_producto(nombre_sel)).pack(side="left", padx=(0, 10))
            ttk.Button(admin_btns_frame, text="Eliminar Producto", style="Accent.TButton", command=lambda: self._eliminar_producto(nombre_sel)).pack(side="left")

    def _calcular_y_actualizar_total_stock(self):
        if hasattr(self, 'lbl_total_stock') and data_manager.usuario_actual["rol"] == "administrador":
            total = sum(int(p.get("stock", 0)) for p in data_manager.get_productos_data().values())
            self.lbl_total_stock.config(text=f"Stock Total Global: {total} unidades")

    def _on_app_close(self):
        if data_manager.hora_inicio_sesion_actual:
            duracion = datetime.datetime.now() - data_manager.hora_inicio_sesion_actual
            minutos = duracion.total_seconds() / 60
            registrar_accion_excel("Cierre Aplicacion", f"Usuario: {data_manager.usuario_actual.get('nombre', 'N/A')}", duracion_min=minutos)
        else:
            registrar_accion_excel("Cierre Aplicacion", "Cerrado desde login.")
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()