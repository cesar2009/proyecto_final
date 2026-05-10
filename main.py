import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox

# Leer excel
df = pd.read_excel("Pokemon.xlsx")

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("1000x700")
app.title("Analizador Pokémon - TU NOMBRE")

titulo = ctk.CTkLabel(
    app,
    text="Analizador de Datos Pokémon",
    font=("Arial", 28)
)
titulo.pack(pady=20)

# filtro por tipo
tipo_var = ctk.StringVar(value=df["Type 1"].unique()[0])

menu = ctk.CTkOptionMenu(
    app,
    values=list(df["Type 1"].unique()),
    variable=tipo_var
)
menu.pack(pady=10)


def filtrar():
    return df[df["Type 1"] == tipo_var.get()]


# gráfica 1
def grafica_barras():
    data = filtrar()

    data.groupby("Generation")["Attack"].mean().plot(kind="bar")
    plt.title("Promedio de Ataque por Generación")
    plt.ylabel("Ataque")
    plt.show()


# gráfica 2
def grafica_dispersion():
    data = filtrar()

    plt.scatter(data["HP"], data["Speed"])
    plt.xlabel("HP")
    plt.ylabel("Speed")
    plt.title("HP vs Speed")
    plt.show()


# exportar excel
def exportar():
    data = filtrar()
    data.to_excel("ReportePokemon.xlsx")

    messagebox.showinfo(
        "Éxito",
        "Reporte exportado correctamente"
    )


# acerca de
def acerca():
    messagebox.showinfo(
        "Acerca de",
        """
Analizador de datos Pokémon

Programador: TU NOMBRE

Librerías:
- pandas
- matplotlib
- openpyxl
- customtkinter
        """
    )


# salir
def salir():
    if messagebox.askyesno("Confirmar", "¿Salir del programa?"):
        app.quit()


ctk.CTkButton(
    app,
    text="Generar gráfica de barras",
    command=grafica_barras
).pack(pady=10)

ctk.CTkButton(
    app,
    text="Generar gráfica dispersión",
    command=grafica_dispersion
).pack(pady=10)

ctk.CTkButton(
    app,
    text="Exportar reporte Excel",
    command=exportar
).pack(pady=10)

ctk.CTkButton(
    app,
    text="Acerca de",
    command=acerca
).pack(pady=10)

ctk.CTkButton(
    app,
    text="Salir",
    command=salir
).pack(pady=10)

app.mainloop()