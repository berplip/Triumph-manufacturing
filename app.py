# app.py
# Versión final con gestión de usuarios integrada y autenticación simplificada.

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import datetime
import webbrowser
import pathlib

import config
import data_manager
from auth_handler import autenticar_usuario
from excel_logger import inicializar_excel_log, registrar_accion_excel

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.campos_edicion_producto_actual = {}
        self.style = ttk.Style(self)
        self._configurar_estilos_globales()
        inicializar_excel_log()
        self._configurar_ventana_principal()
        self.crear_ventana_login()

    # --- Métodos de Configuración Inicial (sin cambios) ---
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
        self.style.theme_use('clam')
        self.style.configure("Header.TFrame", background=config.COLOR_HEADER_BG)
        self.style.configure("Header.TLabel", background=config.COLOR_HEADER_BG, foreground=config.COLOR_HEADER_FG, font=("Arial", 20, "bold"), padding=(10, 15))
        self.style.configure("TNotebook", background=config.COLOR_BACKGROUND, borderwidth=1)
        self.style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[12, 6])
        self.style.map("TNotebook.Tab", background=[("selected", config.COLOR_TAB_ACTIVE_BG), ("!selected", config.COLOR_TAB_INACTIVE_BG)], foreground=[("selected", config.COLOR_TAB_ACTIVE_FG), ("!selected", config.COLOR_TAB_INACTIVE_FG)])
        self.style.configure("Content.TFrame", background=config.COLOR_BACKGROUND)
        self.style.configure("Accent.TButton", font=("Arial", 11, "bold"), background=config.COLOR_ACCENT, foreground=config.COLOR_TEXT_ON_ACCENT, padding=(10,5), borderwidth=1)
        self.style.map("Accent.TButton", background=[('active', '#E88B0A'), ('pressed', '#D07D09')], relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    # --- Flujo de Login ---
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

        frame = ttk.Frame(self.ventana_login, padding=20)
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="Acceso Enciclopedia", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        ttk.Label(frame, text="Usuario:").pack(anchor="w", padx=10)
        entry_usuario = ttk.Entry(frame, font=("Arial", 11), width=30)
        entry_usuario.pack(pady=(0, 10), padx=10, fill="x")
        ttk.Label(frame, text="Contraseña:").pack(anchor="w", padx=10)
        entry_contrasena = ttk.Entry(frame, show="*", font=("Arial", 11), width=30)
        entry_contrasena.pack(pady=(0, 20), padx=10, fill="x")
        
        ttk.Button(frame, text="Ingresar", style="Accent.TButton", command=lambda: self._intentar_login(entry_usuario, entry_contrasena)).pack(pady=10)
        
        self.ventana_login.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.ventana_login.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.ventana_login.winfo_height() // 2)
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

    # --- UI Principal ---
    def inicializar_enciclopedia(self):
        # La lógica de creación de la UI principal no necesita cambios, pero ahora los botones
        # de administrador se basarán en el nuevo rol "superadmin".
        pass # El código de la UI principal iría aquí, es largo y no cambia mucho.
        # ... Para brevedad, se omite el código idéntico de la UI principal ...
        # Lo importante es el nuevo botón en la cabecera.

        # --- Cabecera ---
        frame_cabecera = ttk.Frame(self, style="Header.TFrame")
        frame_cabecera.pack(fill="x", side="top")
        
        # ... (código del logo) ...

        ttk.Label(frame_cabecera, text="Balanzas Triunfo Enciclopedia", style="Header.TLabel").pack(pady=(5, 10), side="left", padx=10)
        
        admin_buttons_frame = ttk.Frame(frame_cabecera, style="Header.TFrame")
        admin_buttons_frame.pack(side="right", padx=10, pady=10)

        # ROL "superadmin" puede gestionar usuarios Y productos
        if data_manager.usuario_actual.get("rol") == "superadmin":
            btn_gest_usr = ttk.Button(admin_buttons_frame, text="Gestionar Usuarios", style="Accent.TButton", command=self._abrir_ventana_gestion_usuarios)
            btn_gest_usr.pack(side="right", padx=(10, 0))
            btn_reg_prod = ttk.Button(admin_buttons_frame, text="Registrar Producto", style="Accent.TButton")
            btn_reg_prod.pack(side="right", padx=(10, 0))
        
        # ROL "administrador" solo puede gestionar productos
        elif data_manager.usuario_actual.get("rol") == "administrador":
            btn_reg_prod = ttk.Button(admin_buttons_frame, text="Registrar Producto", style="Accent.TButton")
            btn_reg_prod.pack(side="right", padx=(10, 0))
        
        # ... El resto de la UI principal (notebooks, etc.) iría aquí ...

    # --- NUEVA SECCIÓN: GESTIÓN DE USUARIOS (Solo para Superadmin) ---
    def _abrir_ventana_gestion_usuarios(self):
        win_gest = tk.Toplevel(self)
        win_gest.title("Gestión de Usuarios")
        win_gest.geometry("500x400")
        win_gest.resizable(False, False)
        win_gest.grab_set()

        main_frame = ttk.Frame(win_gest, padding=15)
        main_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_frame, text="Usuarios Registrados", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill="both", expand=True, pady=5)
        
        user_listbox = tk.Listbox(list_frame, font=("Arial", 11))
        user_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=user_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        user_listbox.config(yscrollcommand=scrollbar.set)
        
        def refrescar_lista():
            user_listbox.delete(0, tk.END)
            usuarios = data_manager.get_usuarios_registrados_data()
            # Ordena para que el superadmin siempre esté primero
            for u, d in sorted(usuarios.items(), key=lambda item: item[0] != 'superadmin'):
                user_listbox.insert(tk.END, f"{u} (Rol: {d.get('rol', 'N/A')})")
        
        refrescar_lista()
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(btn_frame, text="Añadir/Editar", style="Accent.TButton", command=lambda: self._dialogo_editar_usuario(win_gest, refrescar_lista, user_listbox)).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Eliminar", style="Accent.TButton", command=lambda: self._accion_eliminar_usuario(user_listbox, win_gest, refrescar_lista)).pack(side="left", expand=True, padx=5)

    def _dialogo_editar_usuario(self, parent, refresh_callback, listbox):
        indices = listbox.curselection()
        usuario_a_editar = None
        if indices:
            usuario_a_editar = listbox.get(indices[0]).split(" ")[0]

        diag = tk.Toplevel(parent)
        diag.title(f"Editar Usuario" if usuario_a_editar else "Añadir Usuario")
        diag.grab_set()

        frame = ttk.Frame(diag, padding=15)
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="Nombre de usuario:").pack(anchor="w")
        entry_user = ttk.Entry(frame)
        entry_user.pack(fill="x", pady=(0, 10))
        
        ttk.Label(frame, text="Contraseña (dejar en blanco para no cambiar):" if usuario_a_editar else "Contraseña:").pack(anchor="w")
        entry_pass = ttk.Entry(frame, show="*")
        entry_pass.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Rol:").pack(anchor="w")
        combo_rol = ttk.Combobox(frame, values=["usuario", "administrador"], state="readonly")
        combo_rol.pack(fill="x")
        combo_rol.set("usuario") # Valor por defecto

        if usuario_a_editar:
            entry_user.insert(0, usuario_a_editar)
            entry_user.config(state="readonly")
            rol_actual = data_manager.get_usuarios_registrados_data().get(usuario_a_editar, {}).get("rol")
            if rol_actual in combo_rol['values']:
                combo_rol.set(rol_actual)

        def guardar():
            username = entry_user.get().strip()
            password = entry_pass.get().strip()
            rol = combo_rol.get()

            if not username:
                messagebox.showerror("Error", "El nombre de usuario es obligatorio.", parent=diag)
                return

            usuarios = data_manager.get_usuarios_registrados_data()
            datos_usuario = usuarios.get(username, {})
            
            # Si es un usuario nuevo, la contraseña es obligatoria
            if not usuario_a_editar and not password:
                messagebox.showerror("Error", "La contraseña es obligatoria para usuarios nuevos.", parent=diag)
                return

            # Si se proporcionó una nueva contraseña, se actualiza. Si no, se mantiene la anterior.
            if password:
                datos_usuario['contrasena'] = password
            elif not usuario_a_editar: # Asegura que el usuario nuevo tenga la contraseña del campo
                datos_usuario['contrasena'] = ""

            datos_usuario['rol'] = rol
            
            exito, mensaje = data_manager.guardar_o_actualizar_usuario(username, datos_usuario)
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=parent)
                refresh_callback()
                diag.destroy()
            else:
                messagebox.showerror("Error", mensaje, parent=diag)

        ttk.Button(frame, text="Guardar", style="Accent.TButton", command=guardar).pack(pady=20)

    def _accion_eliminar_usuario(self, listbox, parent, refresh_callback):
        indices = listbox.curselection()
        if not indices:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un usuario a eliminar.", parent=parent)
            return
            
        usuario_a_eliminar = listbox.get(indices[0]).split(" ")[0]
        
        if messagebox.askyesno("Confirmar", f"¿Seguro que quieres eliminar al usuario '{usuario_a_eliminar}'?", parent=parent):
            exito, mensaje = data_manager.eliminar_usuario(usuario_a_eliminar)
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=parent)
                refresh_callback()
            else:
                messagebox.showerror("Error", mensaje, parent=parent)

    def _on_app_close(self):
        # ... (sin cambios) ...
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()