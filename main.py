# -*- coding: utf-8 -*-
import os
import sys
import json
import shlex
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont
import pystray
import queue

# --- CONFIGURACIÓN ---
APPS_FILE = "apps.json"
ICON_FILE = "icon.png"

class AppLauncher:
    """
    Versión con flujo de trabajo simplificado y corrección definitiva para el botón Eliminar
    y la gestión de datos en la ventana de la GUI.
    """
    def __init__(self):
        self.tray_icon = None
        self.is_running = True
        self.running_processes = {}
        self.lock = threading.Lock()
        self.gui_queue = queue.Queue()

        self.root = tk.Tk()
        self.root.withdraw()
        self.gui_window = None

    # --- Lógica de la Aplicación ---

    def _load_apps(self):
        if not os.path.exists(APPS_FILE): return []
        try:
            with open(APPS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError): return []

    def _save_apps(self, apps):
        with open(APPS_FILE, 'w', encoding='utf-8') as f:
            json.dump(apps, f, indent=4, ensure_ascii=False)

    def _launch_app(self, app_config):
        app_name = app_config.get('name')
        try:
            command = [app_config['path']] + shlex.split(app_config.get('params', ''))
            process = subprocess.Popen(command)
            with self.lock:
                self.running_processes[app_name] = process
        except FileNotFoundError:
            self.queue_action('show_error', "Archivo no encontrado", f"Ruta no encontrada:\n{app_config['path']}")
        except Exception as e:
            self.queue_action('show_error', "Error al lanzar", f"Error al lanzar '{app_name}':\n{e}")

    # --- Comunicación Segura entre Hilos ---

    def queue_action(self, action_type, *args):
        self.gui_queue.put((action_type, args))

    def process_gui_queue(self):
        try:
            while True:
                action_type, args = self.gui_queue.get_nowait()
                if action_type == 'show_gui':
                    self._show_gui_handler()
                elif action_type == 'show_error':
                    messagebox.showerror(args[0], args[1])
                elif action_type == 'exit':
                    self._exit_handler()
        except queue.Empty:
            pass
        
        if self.is_running:
            self.root.after(100, self.process_gui_queue)

    # --- Hilo de pystray ---

    def _run_tray_icon(self):
        create_default_icon_if_needed()
        try:
            image = Image.open(ICON_FILE)
        except FileNotFoundError:
            self.queue_action('show_error', "Error Crítico", f"No se encontró {ICON_FILE}.")
            self.queue_action('exit')
            return

        menu = pystray.Menu(self._create_menu_items)
        self.tray_icon = pystray.Icon("LRA", image, "Lanzador Rápido", menu)
        self.tray_icon.left_click_action = lambda: self.queue_action('show_gui')
        self.tray_icon.run()

    def _create_menu_items(self):
        apps = self._load_apps()
        
        with self.lock:
            processes_to_check = list(self.running_processes.items())
            for name, process in processes_to_check:
                if process.poll() is not None:
                    del self.running_processes[name]
            running_names = self.running_processes.keys()

        if not apps:
            yield pystray.MenuItem("No hay apps registradas", None, enabled=False)
        else:
            for app in apps:
                is_running = app['name'] in running_names
                display_name = f"{app['name']} {'(Activa)' if is_running else ''}"
                
                def create_callback(conf):
                    def action(icon, item):
                        self._launch_app(conf)
                    return action

                yield pystray.MenuItem(display_name, create_callback(app))

        yield pystray.Menu.SEPARATOR
        yield pystray.MenuItem('Gestionar Aplicaciones', lambda: self.queue_action('show_gui'))
        yield pystray.MenuItem('Salir', lambda: self.queue_action('exit'))

    # --- Handlers de la GUI ---

    def _show_gui_handler(self):
        if self.gui_window and self.gui_window.winfo_exists():
            self.gui_window.deiconify()
        else:
            self._create_gui_window()
        self.gui_window.lift()
        self.gui_window.focus_force()

    def _exit_handler(self):
        self.is_running = False
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()

    def _create_gui_window(self):
        self.gui_window = tk.Toplevel(self.root)
        self.gui_window.title("Gestionar Aplicaciones")
        self.gui_window.geometry("700x450")
        self.gui_window.protocol("WM_DELETE_WINDOW", self.gui_window.withdraw)
        
        # Variable para mantener el estado de la selección de forma más fiable
        current_selection_index = None

        main_frame = ttk.Frame(self.gui_window, padding="10")
        main_frame.pack(fill="both", expand=True)

        add_button = ttk.Button(
            main_frame,
            text="Añadir Aplicación desde Archivo...",
            command=lambda: add_app_from_file()
        )
        add_button.pack(pady=(0, 10), fill="x")

        list_frame = ttk.LabelFrame(main_frame, text="Aplicaciones Registradas", padding="10")
        list_frame.pack(fill="both", expand=True, pady=5)
        
        listbox = tk.Listbox(list_frame, height=10)
        listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        form_frame = ttk.LabelFrame(main_frame, text="Editar Aplicación Seleccionada", padding="10")
        form_frame.pack(fill="x", pady=5)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(form_frame, width=50)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(form_frame, text="Parámetros:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        params_entry = ttk.Entry(form_frame)
        params_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady="10")

        # --- Lógica interna de la GUI (Corregida y Robusta) ---
        def refresh_listbox():
            nonlocal current_selection_index
            apps = self._load_apps()
            listbox.delete(0, tk.END)
            for app in apps:
                listbox.insert(tk.END, app['name'])
            clear_entries()
            current_selection_index = None # Resetear selección

        def clear_entries():
            nonlocal current_selection_index
            name_entry.delete(0, tk.END); params_entry.delete(0, tk.END)
            listbox.selection_clear(0, tk.END)
            current_selection_index = None # Resetear selección

        def on_app_select(event):
            nonlocal current_selection_index
            selected_indices = listbox.curselection()
            if not selected_indices:
                current_selection_index = None
                return
            
            current_selection_index = selected_indices[0]
            apps = self._load_apps()
            app = apps[current_selection_index]
            
            # Limpiar y rellenar los campos de edición
            name_entry.delete(0, tk.END)
            params_entry.delete(0, tk.END)
            name_entry.insert(0, app.get('name', ''))
            params_entry.insert(0, app.get('params', ''))

        listbox.bind("<<ListboxSelect>>", on_app_select)

        def add_app_from_file():
            filepath = filedialog.askopenfilename(
                title="Seleccionar ejecutable",
                filetypes=(("Ejecutables", "*.exe"), ("Todos los archivos", "*.*"))
            )
            if not filepath: return
            path = os.path.normpath(filepath)
            filename = os.path.basename(path)
            app_name = os.path.splitext(filename)[0]
            new_app = {"name": app_name, "path": path, "params": ""}
            apps = self._load_apps()
            apps.append(new_app)
            self._save_apps(apps)
            refresh_listbox()
            messagebox.showinfo("Éxito", f"'{app_name}' ha sido añadida.")

        def edit_app():
            nonlocal current_selection_index
            if current_selection_index is None: 
                messagebox.showwarning("Atención", "Selecciona una aplicación de la lista para editar.")
                return
            
            apps = self._load_apps()
            apps[current_selection_index]['name'] = name_entry.get().strip()
            apps[current_selection_index]['params'] = params_entry.get().strip()
            self._save_apps(apps)
            refresh_listbox()
            messagebox.showinfo("Éxito", "Cambios guardados.")

        def delete_app():
            nonlocal current_selection_index
            if current_selection_index is None: 
                messagebox.showwarning("Atención", "Selecciona una aplicación de la lista para eliminar.")
                return

            apps = self._load_apps()
            app_to_delete = apps[current_selection_index]
            
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar '{app_to_delete['name']}'?"):
                apps.pop(current_selection_index)
                self._save_apps(apps)
                refresh_listbox()
        
        edit_btn = ttk.Button(button_frame, text="Guardar Cambios", command=edit_app)
        edit_btn.pack(side="left", padx=5, expand=True, fill="x")
        del_btn = ttk.Button(button_frame, text="Eliminar Seleccionada", command=delete_app)
        del_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        refresh_listbox()

    def run(self):
        tray_thread = threading.Thread(target=self._run_tray_icon, daemon=True)
        tray_thread.start()
        self.process_gui_queue()
        print("\n*** ¡APLICACIÓN EN EJECUCIÓN! ***")
        self.root.mainloop()

def create_default_icon_if_needed():
    if not os.path.exists(ICON_FILE):
        print(f"-> Creando icono por defecto ({ICON_FILE})...")
        image = Image.new('RGB', (64, 64), color='dodgerblue')
        dc = ImageDraw.Draw(image)
        dc.rectangle([10, 10, 54, 54], fill='white')
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font = ImageFont.load_default()
        dc.text((18, 18), "LRA", fill="black", font=font)
        image.save(ICON_FILE)

if __name__ == "__main__":
    app = AppLauncher()
    app.run()
