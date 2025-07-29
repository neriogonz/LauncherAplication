import json
import subprocess
import shlex
import os
import tkinter as tk
from tkinter import messagebox

# Constante para el nombre del archivo de base de datos
APPS_FILE = "apps.json"

# Diccionario para mantener un registro de los procesos en ejecución
running_processes = {}

def show_error_popup(title, message):
   
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana raíz principal
    messagebox.showerror(title, message)
    root.destroy()

def load_apps():
    
    if not os.path.exists(APPS_FILE):
        return []
    try:
        with open(APPS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_apps(apps):
  
    with open(APPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(apps, f, indent=4, ensure_ascii=False)

def launch_app(app_config):
    
    global running_processes
    app_name = app_config.get('name')

    if app_name in running_processes and running_processes[app_name].poll() is None:
        print(f"La aplicación '{app_name}' ya está en ejecución.")
        return

    try:
        command = [app_config['path']] + shlex.split(app_config.get('params', ''))
        print(f"Ejecutando: {' '.join(command)}")
        
        process = subprocess.Popen(command)
        running_processes[app_name] = process

    except FileNotFoundError:
        error_message = (f"Error: No se pudo encontrar el archivo.\n\n"
                         f"Asegúrate de que la ruta es correcta en tu gestor de aplicaciones:\n\n"
                         f"'{app_config['path']}'")
        print(error_message)
        show_error_popup("Archivo no encontrado", error_message)

    except Exception as e:
        error_message = f"Ocurrió un error al intentar lanzar '{app_name}':\n\n{e}"
        print(error_message)
        show_error_popup("Error al lanzar", error_message)

def check_process_status(app_name):
    
    if app_name in running_processes:
        process = running_processes[app_name]
        if process.poll() is None:
            return True
        else:
            del running_processes[app_name]
            return False
    return False
