import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class RegistroTareas:
    def __init__(self, master):
        self.master = master
        self.master.title("Registro de Tareas")
        
        self.tarea_var = tk.StringVar()
        tk.Label(master, text="Tarea:").grid(row=0, column=0)
        tk.Entry(master, textvariable=self.tarea_var).grid(row=0, column=1)
        
        self.cargar_datos()
        
        self.inicio_var = None
        self.pausa_var = None
        
        
        tk.Button(master, text="Iniciar", command=self.iniciar_tarea).grid(row=1, column=0)
        tk.Button(master, text="Pausar", command=self.pausar_tarea).grid(row=1, column=1)
        tk.Button(master, text="Reanudar", command=self.reanudar_tarea).grid(row=1, column=2)
        tk.Button(master, text="Finalizar", command=self.finalizar_tarea).grid(row=1, column=3)
        tk.Button(master, text="Guardar", command=self.guardar_excel).grid(row=1, column=4)
        
        self.estado_label = tk.Label(master, text="Estado: No iniciado")
        self.estado_label.grid(row=2, column=0, columnspan=5)
        
        
        self.crear_interfaz_estadisticas()
        
    def cargar_datos(self):
        try:
            self.data = pd.read_excel("registro_tareas.xlsx").to_dict(orient="records")
        except FileNotFoundError:
            self.data = []

    def guardar_datos(self):
        df = pd.DataFrame(self.data)
        df.to_excel("registro_tareas.xlsx", index=False)

    def iniciar_tarea(self):
        self.inicio_var = datetime.now()
        self.pausa_var = None
        self.tiempo_pausado = []
        self.estado_label.config(text="Estado: Iniciado")

    def pausar_tarea(self):
        if self.inicio_var:
            self.pausa_var = datetime.now()
            self.estado_label.config(text="Estado: En pausa")
        else:
            messagebox.showwarning("Advertencia", "No hay ninguna tarea en curso.")

    def reanudar_tarea(self):
        if self.pausa_var:
            pausa_duracion = datetime.now() - self.pausa_var
            self.tiempo_pausado.append(pausa_duracion)
            self.pausa_var = None
            self.estado_label.config(text="Estado: Reanudado")
        else:
            messagebox.showwarning("Advertencia", "La tarea no está en pausa.")

    def finalizar_tarea(self):
        if self.inicio_var:
            fin = datetime.now()
            duracion_total = fin - self.inicio_var
            for pausa in self.tiempo_pausado:
                duracion_total -= pausa
            self.data.append([self.tarea_var.get(), self.inicio_var, fin, duracion_total])
            self.inicio_var = None
            self.estado_label.config(text="Estado: Finalizado")
        else:
            messagebox.showwarning("Advertencia", "No hay ninguna tarea en curso.")

    def guardar_excel(self):
        ruta = "registro_tareas.xlsx"
    
        if self.data:
            df = pd.DataFrame(self.data, columns=["Tarea", "Hora de Inicio", "Hora de Finalización", "Duración"])
              # Convertir la columna 'Duración' a timedelta
            df["Duración"] = pd.to_timedelta(df["Duración"])

            df["Duración"] = df["Duración"].dt.total_seconds() / 60  # Convertir a minutos

            plt.figure()
            sns.barplot(x='Tarea', y='Duración', data=df)
            plt.xticks(rotation=90)
            plt.title('Tiempo Dedicado a Cada Tarea')
            plt.ylabel('Duración (minutos)')
            plt.xlabel('Tarea')
            plt.show()
        else:
            messagebox.showwarning("Advertencia", "No hay datos para mostrar")
                            
    def mostrar_estadisticas(self):
        if self.data:
            df = pd.DataFrame(self.data, columns=["Tarea", "Hora de Inicio", "Hora de Finalización", "Duración"])

            tiempo_total = df["Duración"].sum()
            tiempo_medio = df["Duración"].mean()
            
            estadisticas = f"Tiempo Total Trabajado: {tiempo_total}\nTiempo Medio por Tarea: {tiempo_medio}"
            messagebox.showinfo("Estadísticas", estadisticas)
        else:
            messagebox.showwarning("Advertencia", "No hay datos para mostrar")

    def mostrar_grafico(self):
        if self.data:
            df = pd.DataFrame(self.data, columns=["Tarea", "Hora de Inicio", "Hora de Finalización", "Duración"])
            # Convertir la columna 'Duración' a timedelta
            df["Duración"] = pd.to_timedelta(df["Duración"])

            df["Duración"] = df["Duración"].dt.total_seconds() / 60  # Convertir a minutos

            plt.figure()
            sns.barplot(x='Tarea', y='Duración', data=df)
            plt.xticks(rotation=90)
            plt.title('Tiempo Dedicado a Cada Tarea')
            plt.ylabel('Duración (minutos)')
            plt.xlabel('Tarea')
            plt.show()
        else:
            messagebox.showwarning("Advertencia", "No hay datos para mostrar")

    def crear_interfaz_estadisticas(self):
        tk.Button(self.master, text="Mostrar Estadísticas", command=self.mostrar_estadisticas).grid(row=3, column=0, columnspan=2)
        tk.Button(self.master, text="Mostrar Gráfico", command=self.mostrar_grafico).grid(row=3, column=2, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroTareas(root)
    root.mainloop()
