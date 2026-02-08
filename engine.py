# MOD-001: ENCABEZADO [INICIO]
"""
*****************************************
PROYECTO: Desktop Box
ARCHIVO: engine.py
VERSIÓN: 05.00
FECHA: 26/01/2026 10:38 (UTC-5)
*****************************************
"""
# MOD-001: FIN

# MOD-002: IMPORTACIONES [INICIO]
import tkinter as tk
from tkinter import colorchooser, simpledialog
import json, os, sys
# MOD-002: FIN

# MOD-003: CONFIGURACIÓN DE RUTAS [INICIO]
# SOLUCIÓN TÉCNICA PARA RUTAS EN EXECUTABLES (.exe)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

nombre_caja = sys.argv[1].lower() if len(sys.argv) > 1 else "organizador"
CONFIG_FILE = os.path.join(BASE_DIR, f"config_{nombre_caja}.json")
# MOD-003: FIN

# MOD-004: CLASE PRINCIPAL [INICIO]
class OrganizadorMarcoPro:
    def __init__(self, root):
        self.root = root
        self.min_w, self.min_h = 150, 100
        self.datos = {"x": 100, "y": 100, "w": 400, "h": 300, "color": "#5a027d", "titulo": nombre_caja.upper()}
        self.cargar_config()

        self.root.title(self.datos['titulo']) 
        self.root.overrideredirect(True) 
        self.root.geometry(f"{self.datos['w']}x{self.datos['h']}+{self.datos['x']}+{self.datos['y']}")
        
        self.trans_color = '#abcdef' 
        self.root.wm_attributes("-transparentcolor", self.trans_color)
        self.root.configure(bg=self.trans_color)

        self.crear_interfaz()
        self.vincular_eventos()
        self.crear_menu()
# MOD-004: FIN

# MOD-005: INTERFAZ VISUAL [INICIO]
    def crear_interfaz(self):
        # Marco principal
        self.marco = tk.Frame(self.root, bg=self.datos['color'])
        self.marco.pack(expand=True, fill="both")
        
        # Tirador SUPERIOR (Más delgado: bajamos de 5 a 3)
        self.resizer_sup = tk.Frame(self.marco, bg=self.datos['color'], cursor="sb_v_double_arrow", height=3)
        self.resizer_sup.pack(side="top", fill="x")

        # Etiqueta de título (Reducimos pady de 2 a 0 para adelgazar la columna)
        # Probamos con tamaño 10 o 9 para que se vea más minimalista
        self.label = tk.Label(self.marco, text=self.datos['titulo'], fg="white", 
                              bg=self.datos['color'], font=("Segoe UI", 10, "bold"), cursor="fleur")
        self.label.pack(side="top", fill="x", pady=0)

        # Área interior TRANSPARENTE
        self.interior = tk.Frame(self.marco, bg=self.trans_color)
        self.interior.pack(expand=True, fill="both", padx=8, pady=(0, 8)) 

        # Tiradores de esquina inferiores
        self.resizer_der = tk.Frame(self.marco, bg=self.datos['color'], cursor="size_nw_se", width=15, height=15)
        self.resizer_der.place(relx=1.0, rely=1.0, anchor="se")

        self.resizer_izq = tk.Frame(self.marco, bg=self.datos['color'], cursor="size_ne_sw", width=15, height=15)
        self.resizer_izq.place(relx=0.0, rely=1.0, anchor="sw")
# MOD-005: FIN

# MOD-006: VINCULACIÓN DE EVENTOS V4 [INICIO]
    def vincular_eventos(self):
        # Eventos de movimiento y Menú Contextual (Clic derecho restaurado)
        for widget in [self.marco, self.label]:
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)
            widget.bind("<Button-3>", self.show_menu)

        # Eventos para Tirador Superior
        self.resizer_sup.bind("<ButtonPress-1>", self.start_resize_sup)
        self.resizer_sup.bind("<B1-Motion>", self.do_resize_sup)

        # Eventos para Tiradores Inferiores (Esquinas)
        self.resizer_der.bind("<ButtonPress-1>", self.start_resize_der)
        self.resizer_der.bind("<B1-Motion>", self.do_resize_der)
        self.resizer_izq.bind("<ButtonPress-1>", self.start_resize_izq)
        self.resizer_izq.bind("<B1-Motion>", self.do_resize_izq)
# MOD-006: FIN

# MOD-007: MENÚ CONTEXTUAL V2 [INICIO]
    def crear_menu(self):
        # Restauración del modal con 3 opciones
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Cambiar Nombre", command=self.cambiar_nombre)
        self.menu.add_command(label="Cambiar Color", command=self.cambiar_color)
        self.menu.add_separator()
        self.menu.add_command(label="Cerrar esta caja", command=self.root.destroy)

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)
# MOD-007: FIN

# MOD-008: LÓGICA DE MOVIMIENTO [INICIO]
    def start_move(self, event): 
        self.x, self.y = event.x, event.y
    
    def do_move(self, event):
        nx, ny = self.root.winfo_x() + (event.x - self.x), self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{nx}+{ny}")
        self.datos["x"], self.datos["y"] = nx, ny
        self.guardar_config()
# MOD-008: FIN

# MOD-009: REDIMENSIONAR DERECHA Y SUPERIOR V2 [INICIO]
    def start_resize_der(self, event):
        self.start_w, self.start_h = self.root.winfo_width(), self.root.winfo_height()
        self.mouse_x, self.mouse_y = event.x_root, event.y_root

    def do_resize_der(self, event):
        nuevo_w = max(self.min_w, self.start_w + (event.x_root - self.mouse_x))
        nuevo_h = max(self.min_h, self.start_h + (event.y_root - self.mouse_y))
        self.root.geometry(f"{nuevo_w}x{nuevo_h}")
        self.datos["w"], self.datos["h"] = nuevo_w, nuevo_h
        self.guardar_config()

    def start_resize_sup(self, event):
        self.start_h = self.root.winfo_height()
        self.start_y = self.root.winfo_y()
        self.mouse_y = event.y_root

    def do_resize_sup(self, event):
        dy = event.y_root - self.mouse_y
        nuevo_h = self.start_h - dy
        if nuevo_h > self.min_h:
            nueva_y = self.start_y + dy
            self.root.geometry(f"{self.root.winfo_width()}x{nuevo_h}+{self.root.winfo_x()}+{nueva_y}")
            self.datos["h"], self.datos["y"] = nuevo_h, nueva_y
            self.guardar_config()
# MOD-009: FIN

# MOD-010: REDIMENSIONAR IZQUIERDA V3 [INICIO]
    def start_resize_izq(self, event):
        self.start_w, self.start_h = self.root.winfo_width(), self.root.winfo_height()
        self.start_x = self.root.winfo_x()
        self.mouse_x, self.mouse_y = event.x_root, event.y_root

    def do_resize_izq(self, event):
        dx = event.x_root - self.mouse_x
        nuevo_w = self.start_w - dx
        if nuevo_w > self.min_w:
            nueva_x = self.start_x + dx
            nuevo_h = max(self.min_h, self.start_h + (event.y_root - self.mouse_y))
            self.root.geometry(f"{nuevo_w}x{nuevo_h}+{nueva_x}+{self.root.winfo_y()}")
            self.datos["w"], self.datos["h"] = nuevo_w, nuevo_h
            self.datos["x"] = nueva_x
            self.guardar_config()
# MOD-010: FIN

# MOD-011: CAMBIAR NOMBRE [INICIO]
    def cambiar_nombre(self):
        global CONFIG_FILE
        nuevo_nombre = simpledialog.askstring("Renombrar", "Nuevo nombre para esta caja:", parent=self.root)
        if nuevo_nombre:
            nuevo_limpio = nuevo_nombre.lower().strip().replace(" ", "_")
            nueva_ruta = os.path.join(BASE_DIR, f"config_{nuevo_limpio}.json")
            self.datos['titulo'] = nuevo_nombre.upper()
            self.label.config(text=self.datos['titulo'])
            if os.path.exists(CONFIG_FILE) and CONFIG_FILE != nueva_ruta:
                os.remove(CONFIG_FILE)
            CONFIG_FILE = nueva_ruta
            self.guardar_config()
# MOD-011: FIN

# MOD-012: CAMBIAR COLOR V2 [INICIO]
    def cambiar_color(self):
        color = colorchooser.askcolor(title="Elegir Color", parent=self.root)[1]
        if color:
            self.datos['color'] = color
            # Actualizamos todos los elementos visuales del borde
            widgets_color = [self.marco, self.label, self.resizer_sup, self.resizer_der, self.resizer_izq]
            for w in widgets_color:
                w.configure(bg=color)
            self.guardar_config()
# MOD-012: FIN

# MOD-013: GESTIÓN DE CONFIGURACIÓN [INICIO]
    def guardar_config(self):
        try:
            with open(CONFIG_FILE, "w") as f: 
                json.dump(self.datos, f, indent=4)
        except Exception: 
            pass

    def cargar_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    contenido = f.read()
                    if contenido.strip():
                        self.datos.update(json.loads(contenido))
            except Exception: 
                pass
        else:
            self.guardar_config()
# MOD-013: FIN

# MOD-014: CÓDIGO DE CIERRE [INICIO]
if __name__ == "__main__":
    root = tk.Tk()
    app = OrganizadorMarcoPro(root)
    root.mainloop()
# MOD-014: FIN

# MOD-099: NOTAS [INICIO]
"""
DESCRIPCIÓN:
Motor principal de Desktop Box.
Crea cajas flotantes personalizables en el escritorio.

FUNCIONALIDADES:
- Ventanas sin borde con transparencia
- Movimiento y redimensionamiento (ambos lados)
- Personalización de nombre y color
- Persistencia de configuración en JSON

DEPENDENCIAS:
- tkinter (interfaz gráfica)
- json (almacenamiento de configuración)
- sys, os (manejo de rutas y argumentos)

COMPATIBILIDAD:
- Funciona como .py y compilado a .exe
- Compatible con gestor.pyw v01.00

ESTADO:
Funcional y estable
"""
# MOD-099: FIN
