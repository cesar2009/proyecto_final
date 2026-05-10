import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

# Configuración inicial
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PokemonApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analizador Pokémon - Cesar Ketchup")
        self.geometry("1200x750")
        self.minsize(1000, 600)

        # Escondemos la ventana principal mientras carga
        self.withdraw()

        # Variables de datos y estado
        self.df = None
        self.tipos_unicos = []
        self.tipo_var = ctk.StringVar()

        # Iniciar pantalla de carga
        self.mostrar_splash()

    # --- 1. PANTALLA DE CARGA ---
    def mostrar_splash(self):
        # Usar CTkToplevel evita el error de los comandos "after" de Tkinter
        self.splash = ctk.CTkToplevel(self)
        self.splash.overrideredirect(True)  # Sin bordes
        self.splash.geometry("500x300+700+350")
        self.splash.configure(fg_color="#1f1f1f")
        self.splash.attributes("-topmost", True)  # Siempre al frente

        frame_splash = ctk.CTkFrame(self.splash, fg_color="transparent")
        frame_splash.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame_splash, text="🎮", font=("Arial", 50)).pack(pady=(20, 0))
        ctk.CTkLabel(frame_splash, text="Analizador Pokémon", font=("Arial", 26, "bold"), text_color="#1e90ff").pack(
            pady=10)
        ctk.CTkLabel(frame_splash, text="Cargando base de datos...", font=("Arial", 14), text_color="gray").pack(pady=5)

        self.barra_progreso = ctk.CTkProgressBar(frame_splash, width=300, progress_color="#1e90ff")
        self.barra_progreso.pack(pady=20)
        self.barra_progreso.set(0)

        # Iniciar la simulación de carga por pasos
        self.progreso = 0
        self.after(50, self.cargar_datos_paso)

    def cargar_datos_paso(self):
        if self.progreso < 100:
            self.progreso += 5
            self.barra_progreso.set(self.progreso / 100)

            # Cuando llega a 30%, carga el Excel
            if self.progreso == 30:
                self.cargar_datos()

            self.after(50, self.cargar_datos_paso)
        else:
            # Al terminar, cierra el splash y muestra la app principal
            self.splash.destroy()
            self.deiconify()  # Muestra la ventana principal
            self.construir_interfaz()
            self.actualizar_kpis()
            self.mostrar_grafica_inicio()

    def cargar_datos(self):
        try:
            self.df = pd.read_excel("Pokemon.xlsx")
            self.tipos_unicos = sorted(self.df["Type 1"].dropna().unique().tolist())
            if self.tipos_unicos:
                self.tipo_var.set(self.tipos_unicos[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se encontró el archivo Pokemon.xlsx\n{e}")
            self.destroy()

    # --- 2. CONSTRUCCIÓN DE LA INTERFAZ ---
    def construir_interfaz(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=15, fg_color="#2b2b2b")
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 0), pady=20)
        sidebar_frame.grid_propagate(False)

        ctk.CTkLabel(sidebar_frame, text="Pokémon Analytics", font=("Arial", 20, "bold"), text_color="#1e90ff").pack(
            pady=(30, 5))
        ctk.CTkLabel(sidebar_frame, text="By Cesar Ketchup", font=("Arial", 12), text_color="gray").pack(pady=(0, 30))

        ctk.CTkLabel(sidebar_frame, text="Filtrar por Tipo 1:", font=("Arial", 14, "bold"), anchor="w").pack(padx=20,
                                                                                                             fill="x")
        menu = ctk.CTkOptionMenu(sidebar_frame, values=self.tipos_unicos, variable=self.tipo_var,
                                 command=lambda e: self.actualizar_kpis())
        menu.pack(padx=20, pady=(5, 30), fill="x")

        btn_style = {"fg_color": "transparent", "border_width": 1, "border_color": "#555", "hover_color": "#3a3a3a",
                     "anchor": "w", "font": ("Arial", 14)}

        ctk.CTkButton(sidebar_frame, text="📊  Ataque por Generación", command=self.grafica_barras, **btn_style).pack(
            padx=20, pady=5, fill="x")
        ctk.CTkButton(sidebar_frame, text="💨  HP vs Velocidad", command=self.grafica_dispersion, **btn_style).pack(
            padx=20, pady=5, fill="x")
        ctk.CTkButton(sidebar_frame, text="📥  Exportar a Excel", command=self.exportar, fg_color="green",
                      hover_color="darkgreen", font=("Arial", 14)).pack(padx=20, pady=(30, 5), fill="x")

        ctk.CTkLabel(sidebar_frame, text="").pack(expand=True)  # Espaciador

        ctk.CTkButton(sidebar_frame, text="ℹ️  Acerca de", command=self.acerca, fg_color="transparent",
                      hover_color="#3a3a3a", text_color="gray").pack(padx=20, pady=5, fill="x")
        ctk.CTkButton(sidebar_frame, text="❌  Salir", command=self.salir, fg_color="darkred", hover_color="red",
                      font=("Arial", 14)).pack(padx=20, pady=(5, 30), fill="x")

        # --- MAIN PANEL ---
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # KPIs
        kpi_frame = ctk.CTkFrame(main_frame, height=100, fg_color="transparent")
        kpi_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        kpi1 = ctk.CTkFrame(kpi_frame, fg_color="#2b2b2b", corner_radius=10)
        kpi1.pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkLabel(kpi1, text="Total Pokémon", text_color="gray").pack(pady=(10, 0))
        self.lbl_total = ctk.CTkLabel(kpi1, text="0", font=("Arial", 24, "bold"), text_color="#1e90ff")
        self.lbl_total.pack(pady=(0, 10))

        kpi2 = ctk.CTkFrame(kpi_frame, fg_color="#2b2b2b", corner_radius=10)
        kpi2.pack(side="left", expand=True, fill="x", padx=10)
        ctk.CTkLabel(kpi2, text="Ataque Promedio", text_color="gray").pack(pady=(10, 0))
        self.lbl_avg_atk = ctk.CTkLabel(kpi2, text="0", font=("Arial", 24, "bold"), text_color="#ff6347")
        self.lbl_avg_atk.pack(pady=(0, 10))

        kpi3 = ctk.CTkFrame(kpi_frame, fg_color="#2b2b2b", corner_radius=10)
        kpi3.pack(side="left", expand=True, fill="x", padx=(10, 0))
        ctk.CTkLabel(kpi3, text="HP Promedio", text_color="gray").pack(pady=(10, 0))
        self.lbl_avg_hp = ctk.CTkLabel(kpi3, text="0", font=("Arial", 24, "bold"), text_color="#32cd32")
        self.lbl_avg_hp.pack(pady=(0, 10))

        # Frame para la gráfica
        canvas_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b", corner_radius=10)
        canvas_frame.grid(row=1, column=0, sticky="nsew")

        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.fig.patch.set_facecolor('#2b2b2b')
        self.ax.set_facecolor('#2b2b2b')

        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    # --- 3. FUNCIONES LÓGICAS ---
    def filtrar(self):
        return self.df[self.df["Type 1"] == self.tipo_var.get()]

    def actualizar_kpis(self):
        data = self.filtrar()
        self.lbl_total.configure(text=str(len(data)))
        self.lbl_avg_atk.configure(text=f"{data['Attack'].mean():.1f}")
        self.lbl_avg_hp.configure(text=f"{data['HP'].mean():.1f}")

    def mostrar_grafica_inicio(self):
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Selecciona una gráfica\npara comenzar",
                     ha='center', va='center', fontsize=20, color='gray')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def grafica_barras(self):
        data = self.filtrar()
        self.ax.clear()

        data_grouped = data.groupby("Generation")["Attack"].mean()
        # astype(str) arregla el problema de que Matplotlib omita generaciones en el eje X
        bars = self.ax.bar(data_grouped.index.astype(str), data_grouped.values, color='#1e90ff', edgecolor='white',
                           linewidth=0.5)

        self.ax.set_title(f"Promedio de Ataque por Generación (Tipo: {self.tipo_var.get()})", color='white',
                          fontsize=14)
        self.ax.set_ylabel("Ataque", color='white', fontsize=12)
        self.ax.set_xlabel("Generación", color='white', fontsize=12)
        self.ax.tick_params(colors='white')

        for bar in bars:
            yval = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.1f}', ha='center', va='bottom',
                         color='white', fontsize=9)

        self.fig.tight_layout()
        self.canvas.draw()

    def grafica_dispersion(self):
        data = self.filtrar()
        self.ax.clear()

        scatter = self.ax.scatter(data["HP"], data["Speed"], c=data["Attack"], cmap='plasma', alpha=0.7,
                                  edgecolors='white', linewidth=0.5)

        self.ax.set_title(f"HP vs Speed (Tipo: {self.tipo_var.get()})", color='white', fontsize=14)
        self.ax.set_xlabel("HP", color='white', fontsize=12)
        self.ax.set_ylabel("Speed", color='white', fontsize=12)
        self.ax.tick_params(colors='white')

        # Evita que la barra de colores se duplique si presionas el botón varias veces
        if len(self.fig.axes) > 1:
            self.fig.axes[1].remove()

        cbar = self.fig.colorbar(scatter, ax=self.ax)
        cbar.set_label('Ataque', color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

        self.fig.tight_layout()
        self.canvas.draw()

    def exportar(self):
        data = self.filtrar()
        archivo = f"Reporte_{self.tipo_var.get()}.xlsx"
        data.to_excel(archivo, index=False)
        messagebox.showinfo("Éxito", f"Reporte exportado como: {archivo}")

    def acerca(self):
        messagebox.showinfo(
            "Acerca de",
            "Analizador de datos Pokémon\n\n"
            "Programador: Cesar Alcocer\n\n"
            "Librerías:\n"
            "- pandas\n"
            "- matplotlib\n"
            "- openpyxl\n"
            "- customtkinter"
        )

    def salir(self):
        if messagebox.askyesno("Confirmar", "¿Salir del programa?"):
            plt.close('all')  # Limpia la memoria de matplotlib
            self.destroy()  # Cierra la app de forma segura


# --- 4. EJECUCIÓN ---
if __name__ == "__main__":
    app = PokemonApp()
    app.mainloop()