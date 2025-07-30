import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import app_handler as handler

class GuiManager(tk.Toplevel):
    
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestionar Aplicaciones")
        self.geometry("700x500")
        
       
        self.apps = handler.load_apps()

       
        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        self._setup_widgets()
        self._refresh_listbox()

    def _setup_widgets(self):
        """Crea y posiciona todos los widgets en la ventana."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

     
        list_frame = ttk.LabelFrame(main_frame, text="Aplicaciones Registradas", padding="10")
        list_frame.pack(fill="both", expand=True, pady=5)

        self.app_listbox = tk.Listbox(list_frame, height=10)
        self.app_listbox.pack(side="left", fill="both", expand=True)
        self.app_listbox.bind("<<ListboxSelect>>", self._on_app_select)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.app_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.app_listbox.config(yscrollcommand=scrollbar.set)

        # --- Frame del Formulario de Edición ---
        form_frame = ttk.LabelFrame(main_frame, text="Detalles de la Aplicación", padding="10")
        form_frame.pack(fill="x", pady=5)


        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame, width=50)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Ruta:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.path_entry = ttk.Entry(form_frame)
        self.path_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        browse_button = ttk.Button(form_frame, text="...", width=3, command=self._browse_file)
        browse_button.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(form_frame, text="Parámetros:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.params_entry = ttk.Entry(form_frame)
        self.params_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady="10")

        self.add_button = ttk.Button(button_frame, text="Añadir Nueva", command=self._add_app)
        self.add_button.pack(side="left", padx=5, expand=True, fill="x")
        
        self.edit_button = ttk.Button(button_frame, text="Guardar Cambios", command=self._edit_app)
        self.edit_button.pack(side="left", padx=5, expand=True, fill="x")

        self.delete_button = ttk.Button(button_frame, text="Eliminar Seleccionada", command=self._delete_app)
        self.delete_button.pack(side="left", padx=5, expand=True, fill="x")

    def _refresh_listbox(self):
        """Limpia y vuelve a poblar el listbox con los datos actuales."""
        self.app_listbox.delete(0, tk.END)
        for app in self.apps:
            self.app_listbox.insert(tk.END, app['name'])
        self._clear_entries()

    def _clear_entries(self):
        """Limpia los campos de texto del formulario."""
        self.name_entry.delete(0, tk.END)
        self.path_entry.delete(0, tk.END)
        self.params_entry.delete(0, tk.END)
        self.app_listbox.selection_clear(0, tk.END)

    def _on_app_select(self, event):
       
        selected_indices = self.app_listbox.curselection()
        if not selected_indices:
            return
        
        selected_index = selected_indices[0]
        app = self.apps[selected_index]
        
        self._clear_entries()
        self.name_entry.insert(0, app.get('name', ''))
        self.path_entry.insert(0, app.get('path', ''))
        self.params_entry.insert(0, app.get('params', ''))

    def _browse_file(self):
       
        filepath = filedialog.askopenfilename(
            title="Seleccionar ejecutable",
            filetypes=(("Ejecutables", "*.exe"), ("Todos los archivos", "*.*"))
        )
        if filepath:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, filepath)

    def _add_app(self):
       
        name = self.name_entry.get().strip()
        path = self.path_entry.get().strip()

        if not name or not path:
            messagebox.showerror("Error", "El nombre y la ruta son obligatorios.")
            return

        new_app = {
            "name": name,
            "path": path,
            "params": self.params_entry.get().strip()
        }
        self.apps.append(new_app)
        handler.save_apps(self.apps)
        self._refresh_listbox()
        messagebox.showinfo("Éxito", f"'{name}' ha sido añadida.")

    def _edit_app(self):
        """Guarda los cambios de la aplicación seleccionada."""
        selected_indices = self.app_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Atención", "Por favor, selecciona una aplicación para editar.")
            return
        
        selected_index = selected_indices[0]
        name = self.name_entry.get().strip()
        path = self.path_entry.get().strip()

        if not name or not path:
            messagebox.showerror("Error", "El nombre y la ruta son obligatorios.")
            return

        self.apps[selected_index] = {
            "name": name,
            "path": path,
            "params": self.params_entry.get().strip()
        }
        handler.save_apps(self.apps)
        self._refresh_listbox()
        self.app_listbox.selection_set(selected_index) # Mantener la selección
        messagebox.showinfo("Éxito", f"'{name}' ha sido actualizada.")

    def _delete_app(self):
        """Elimina la aplicación seleccionada."""
        selected_indices = self.app_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Atención", "Por favor, selecciona una aplicación para eliminar.")
            return
        
        selected_index = selected_indices[0]
        app_name = self.apps[selected_index]['name']

        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar '{app_name}'?"):
            del self.apps[selected_index]
            handler.save_apps(self.apps)
            self._refresh_listbox()
            messagebox.showinfo("Éxito", f"'{app_name}' ha sido eliminada.")
