# MOD-001: ENCABEZADO [INICIO]
"""
*****************************************
PROYECTO: Desktop Box
ARCHIVO: gestor.pyw
VERSIÓN: 07.00
FECHA: 25/01/2026 08:07 (UTC-5)
*****************************************
"""
# MOD-001: FIN

# MOD-002: IMPORTACIONES [INICIO]
import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess, os, sys
import json
# MOD-002: FIN

# MOD-003: CLASE PRINCIPAL V3 [INICIO]
class GestorDesktopBox:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Box")
        self.root.geometry("350x520") 
        
        self.bloqueo_apertura = False 
        
        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.engine_py = os.path.join(self.base_path, "engine.py")
        self.engine_exe = os.path.join(self.base_path, "engine.exe")
        
        # MOD-013: Variable para el switch (Se inicializa verificando si ya existe el acceso directo)
        self.inicio_auto_var = tk.BooleanVar(value=self.verificar_inicio_automatico())
        
        self.cajas_vistas = [] 
        
        self.crear_interfaz()
        self.actualizar_lista()
        self.verificar_cambios_loop()
# MOD-003: FIN

# MOD-004: INTERFAZ VISUAL V2 [INICIO]
    def crear_interfaz(self):
        tk.Label(self.root, text="DESKTOP BOX", font=("Segoe UI", 12, "bold")).pack(pady=5)
        
        # Switch de Inicio Automático
        tk.Checkbutton(self.root, text="Iniciar cajas con Windows", 
                       variable=self.inicio_auto_var,
                       command=self.alternar_inicio_automatico,
                       font=("Segoe UI", 9)).pack(pady=5)

        self.lista_frame = tk.Frame(self.root)
        self.lista_frame.pack(expand=True, fill="both", padx=20)
        
        tk.Button(self.root, text="+ Crear Nueva Caja", command=self.crear_nueva, 
                  bg="#28a745", fg="white", font=("Segoe UI", 10, "bold"), pady=5).pack(fill="x", padx=30, pady=5)

        tk.Button(self.root, text="👁 Abrir Todas las Cajas", command=self.abrir_todas, 
                  bg="#17a2b8", fg="white", font=("Segoe UI", 10, "bold"), pady=5).pack(fill="x", padx=30, pady=5)
        
        tk.Button(self.root, text="Cerrar Todas las Cajas", command=self.matar_procesos, 
                  bg="#dc3545", fg="white", font=("Segoe UI", 9)).pack(fill="x", padx=30, pady=10)
# MOD-004: FIN

# MOD-005: OBTENER LISTA DE CAJAS [INICIO]
    def obtener_cajas(self):
        try:
            return sorted([f.replace("config_", "").replace(".json", "") 
                    for f in os.listdir(self.base_path) if f.startswith("config_") and f.endswith(".json")])
        except:
            return []
# MOD-005: FIN

# MOD-006: ACTUALIZAR LISTA [INICIO]
    def actualizar_lista(self):
        nuevas_cajas = self.obtener_cajas()
        if nuevas_cajas == self.cajas_vistas: 
            return 
        
        self.cajas_vistas = nuevas_cajas
        
        # Limpiar lista actual
        for widget in self.lista_frame.winfo_children(): 
            widget.destroy()
        
        # Mostrar mensaje si no hay cajas
        if not nuevas_cajas:
            tk.Label(self.lista_frame, text="No hay cajas creadas.", fg="gray").pack(pady=20)
            return
        
        # Crear elemento para cada caja
        for nombre in nuevas_cajas:
            f = tk.Frame(self.lista_frame, pady=5)
            f.pack(fill="x")
            
            tk.Label(f, text=nombre.upper(), font=("Segoe UI", 10)).pack(side="left")
            
            tk.Button(f, text=" X ", bg="#dc3545", fg="white", font=("Segoe UI", 8, "bold"),
                      command=lambda n=nombre: self.eliminar_caja(n)).pack(side="right", padx=(5, 0))
            
            tk.Button(f, text="Abrir", bg="#007bff", fg="white", 
                      command=lambda n=nombre: self.abrir_caja(n)).pack(side="right")
# MOD-006: FIN

# MOD-007: VERIFICACIÓN AUTOMÁTICA [INICIO]
    def verificar_cambios_loop(self):
        self.actualizar_lista()
        self.root.after(1000, self.verificar_cambios_loop)
# MOD-007: FIN

# MOD-008: ABRIR CAJA V3 [INICIO]
    def abrir_caja(self, nombre):
        # Si el sistema está bloqueado, ignoramos el clic rápido
        if self.bloqueo_apertura:
            return
            
        self.bloqueo_apertura = True
        
        # Lógica de limpieza individual
        titulo_objetivo = nombre.upper()
        os.system(f'taskkill /f /fi "WINDOWTITLE eq {titulo_objetivo}" 2>nul')
        
        # Lógica de apertura híbrida (EXE o PY)
        if os.path.exists(self.engine_exe):
            subprocess.Popen([self.engine_exe, nombre], creationflags=0x08000000)
        elif os.path.exists(self.engine_py):
            subprocess.Popen([sys.executable, self.engine_py, nombre], creationflags=0x08000000)
        else:
            messagebox.showerror("Error de Motor", f"No se encontró engine.exe ni engine.py en:\n{self.base_path}")
            
        # Liberamos el bloqueo después de un breve tiempo de seguridad
        self.root.after(500, self._desbloquear_apertura)

    def _desbloquear_apertura(self):
        self.bloqueo_apertura = False
# MOD-008: FIN

# MOD-009: ABRIR TODAS LAS CAJAS V3 [INICIO]
    def abrir_todas(self):
        # Si ya hay una apertura en curso, cancelamos
        if self.bloqueo_apertura:
            return
            
        self.bloqueo_apertura = True
        
        # Primero matamos todos los procesos existentes
        self.matar_procesos()
        
        # Ejecutamos la apertura masiva con un delay y luego desbloqueamos
        self.root.after(300, self._ejecutar_apertura_masiva)
        self.root.after(800, self._desbloquear_apertura)

    def _ejecutar_apertura_masiva(self):
        for nombre in self.obtener_cajas():
            if os.path.exists(self.engine_exe):
                subprocess.Popen([self.engine_exe, nombre], creationflags=0x08000000)
            elif os.path.exists(self.engine_py):
                subprocess.Popen([sys.executable, self.engine_py, nombre], creationflags=0x08000000)
# MOD-009: FIN

# MOD-010: ELIMINAR CAJA [INICIO]
    def eliminar_caja(self, nombre):
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre.upper()}'?"):
            # Cerrar proceso si está abierto
            os.system(f'taskkill /f /fi "WINDOWTITLE eq {nombre.upper()}" 2>nul')
            
            # Eliminar archivo de configuración
            config_path = os.path.join(self.base_path, f"config_{nombre}.json")
            if os.path.exists(config_path): 
                os.remove(config_path)
            
            self.actualizar_lista()
# MOD-010: FIN

# MOD-011: CREAR NUEVA CAJA [INICIO]
    def crear_nueva(self):
        nombre = simpledialog.askstring("Nueva Caja", "Nombre de la caja:", parent=self.root)
        if nombre:
            n_limpio = nombre.lower().strip().replace(" ", "_")
            config_path = os.path.join(self.base_path, f"config_{n_limpio}.json")
            
            # Creación segura del JSON
            if not os.path.exists(config_path):
                datos = {"x": 100, "y": 100, "w": 400, "h": 300, "color": "#5a027d", "titulo": nombre.upper()}
                try:
                    with open(config_path, "w") as f:
                        json.dump(datos, f, indent=4)
                except Exception as e:
                    messagebox.showerror("Error de Escritura", f"No se pudo crear el archivo JSON:\n{e}")
                    return

            self.actualizar_lista()
            self.abrir_caja(n_limpio)
# MOD-011: FIN

# MOD-012: CERRAR TODOS LOS PROCESOS V2 [INICIO]
    def matar_procesos(self):
        # Se asegura de cerrar tanto el ejecutable como los scripts de Python
        os.system('taskkill /f /im engine.exe 2>nul')
        os.system('taskkill /f /fi "WINDOWTITLE ne Desktop Box" /im python.exe 2>nul')
        os.system('taskkill /f /fi "WINDOWTITLE ne Desktop Box" /im pythonw.exe 2>nul')
        # El delay para actualizar la lista es fundamental para la estabilidad
        self.root.after(500, self.actualizar_lista)
# MOD-012: FIN

# MOD-013: LÓGICA DE INICIO AUTOMÁTICO V3 [INICIO]
    def verificar_inicio_automatico(self):
        """Revisa si existe el archivo de arranque en la carpeta Startup."""
        ruta_startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        path_auto = os.path.join(ruta_startup, "DBoxAutoStart.bat")
        return os.path.exists(path_auto)

    def alternar_inicio_automatico(self):
        """Crea o elimina el script de arranque según el estado del switch."""
        ruta_startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        path_auto = os.path.join(ruta_startup, "DBoxAutoStart.bat")
        
        if self.inicio_auto_var.get():
            try:
                # El .bat ejecuta dbox.exe con el argumento --autostart
                ejecutable = os.path.join(self.base_path, "dbox.exe")
                with open(path_auto, "w") as f:
                    f.write(f'start "" "{ejecutable}" --autostart')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo configurar el inicio: {e}")
        else:
            if os.path.exists(path_auto):
                os.remove(path_auto)

    def manejar_autostart(self):
        """Si el programa se abre con el parámetro --autostart, abre las cajas en silencio."""
        if "--autostart" in sys.argv:
            # Esperamos 2 segundos para que el escritorio cargue por completo 
            # y mandamos a abrir todas las cajas sin mostrar el gestor
            self.root.after(2000, self.abrir_todas)

    def _desbloquear_apertura(self): # Asegúrate de que esta función exista para el MOD-008
        self.bloqueo_apertura = False
# MOD-013: FIN

# MOD-014: CÓDIGO DE CIERRE V2 [INICIO]
if __name__ == "__main__":
    root = tk.Tk()
    app = GestorDesktopBox(root)
    
    # NUEVO: Si es autostart, ocultamos la ventana del gestor para que no estorbe
    if "--autostart" in sys.argv:
        root.withdraw() # Oculta la ventana principal del gestor 
    
    app.manejar_autostart() 
    root.mainloop()
# MOD-014: FIN

# MOD-099: NOTAS [INICIO]
"""
DESCRIPCIÓN:
Gestor principal de Desktop Box.
Interfaz de administración para crear, abrir y eliminar cajas.

FUNCIONALIDADES:
- Listado dinámico de cajas existentes
- Crear nuevas cajas con configuración inicial
- Abrir cajas individuales o todas simultáneamente
- Eliminar cajas (archivo y proceso)
- Cerrar todos los procesos de cajas abiertas
- Detección automática de cambios cada segundo

INTEGRACIÓN:
- Lanza engine.py o engine.exe según disponibilidad
- Gestiona archivos config_nombre.json
- Compatible con compilación a .exe

DEPENDENCIAS:
- tkinter (interfaz gráfica)
- subprocess (lanzamiento de procesos)
- json (gestión de configuración)
- sys, os (rutas y sistema)

COMPATIBILIDAD:
- Funciona como .pyw y compilado a .exe
- Compatible con engine.py v01.00

ESTADO:
Funcional y estable
"""
# MOD-099: FIN
