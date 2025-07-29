Lanzador Rápido de Aplicaciones (LRA)
Lanzador Rápido de Aplicaciones (LRA) es una utilidad de escritorio ligera y discreta para Windows, diseñada para mejorar tu productividad. Te permite registrar y lanzar tus programas favoritos con un solo clic desde la bandeja del sistema, manteniendo tu escritorio limpio y organizado.

✨ Características Principales
Ejecución desde la Bandeja del Sistema: La aplicación vive en tu bandeja del sistema (cerca del reloj), sin ocupar espacio en la barra de tareas.

Gestión Intuitiva:

Clic Izquierdo: Abre la ventana para gestionar tus aplicaciones.

Clic Derecho: Despliega un menú para lanzar tus programas al instante.

Añadir Aplicaciones con un Clic: Olvídate de rellenar formularios. Simplemente selecciona un archivo .exe y la aplicación se añadirá automáticamente a tu lista.

Monitoreo de Estado: Visualiza fácilmente qué aplicaciones lanzadas desde el LRA siguen en ejecución gracias al indicador (Activa).

Edición Avanzada: Permite editar el nombre de las aplicaciones y añadir parámetros de lanzamiento personalizados para usuarios avanzados.

Ligero y Eficiente: Consume una cantidad mínima de recursos del sistema.

Persistente: Todas tus aplicaciones registradas se guardan automáticamente, listas para la próxima vez que inicies el programa.

📋 Requisitos
Python 3.8 o superior.

🚀 Instalación y Configuración
Sigue estos pasos para poner en marcha la aplicación en tu sistema.

1. Descargar el Proyecto
Primero, descarga los archivos del proyecto. Puedes clonar el repositorio si tienes Git, o simplemente descargar el código como un archivo ZIP.

2. Abrir una Terminal
Abre una terminal o línea de comandos (CMD, PowerShell, etc.) y navega hasta la carpeta donde descargaste el proyecto.

# Ejemplo:
cd C:\Users\TuUsuario\Desktop\Proyecto-Lanzador-Python

3. Crear y Activar un Entorno Virtual
Es una buena práctica usar un entorno virtual para aislar las dependencias del proyecto.

# 1. Crear el entorno virtual (se creará una carpeta llamada "venv")
python -m venv venv

# 2. Activar el entorno virtual
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
# source venv/bin/activate

Verás (venv) al principio de la línea de la terminal, lo que indica que el entorno está activo.

4. Instalar las Dependencias
Con el entorno virtual activo, instala las librerías necesarias con el siguiente comando:

pip install pystray pillow

¡Y listo! La aplicación ya está configurada y lista para ser ejecutada.

💡 Cómo Usar la Aplicación
1. Ejecutar el Programa
Asegúrate de que tu entorno virtual esté activo y ejecuta el siguiente comando en la terminal:

python main.py

Verás un mensaje de confirmación en la terminal y un nuevo ícono azul aparecerá en tu bandeja del sistema.

2. Añadir tu Primera Aplicación
Haz clic izquierdo en el ícono azul en la bandeja del sistema para abrir la ventana de "Gestionar Aplicaciones".

Haz clic en el botón "Añadir Aplicación desde Archivo...".

Se abrirá un explorador de archivos. Busca y selecciona el archivo ejecutable (.exe) de la aplicación que deseas añadir (por ejemplo, C:\Program Files\VLC\vlc.exe).

¡Listo! La aplicación se añadirá automáticamente a la lista con su nombre.

3. Lanzar Aplicaciones
Haz clic derecho en el ícono de la bandeja del sistema.

Aparecerá un menú con todas tus aplicaciones registradas.

Haz clic en el nombre de la aplicación que deseas abrir.

4. Editar o Eliminar Aplicaciones
Abre la ventana de gestión con un clic izquierdo.

Selecciona la aplicación que deseas modificar de la lista.

Para Editar: Cambia el nombre o añade parámetros en los campos de texto y haz clic en "Guardar Cambios".

Para Eliminar: Con la aplicación seleccionada, haz clic en "Eliminar Seleccionada" y confirma tu decisión.

📁 Estructura de Archivos
main.py: El corazón de la aplicación. Contiene todo el código fuente.

apps.json: Un archivo de texto donde se guardan tus aplicaciones registradas. Se crea y actualiza automáticamente.

icon.png: El ícono que se muestra en la bandeja del sistema. Si no existe, se crea uno por defecto al iniciar la aplicación.

README.md: Este archivo.

📄 Licencia
Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
