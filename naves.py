import tkinter as tk
import random

# Configuración inicial de la ventana
root = tk.Tk()
root.title("Juego de Navecita")
root.resizable(False, False)

# Dimensiones del área de juego
canvas_width = 600
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Clase para la nave del jugador
class Nave:
    def __init__(self, canvas):
        self.canvas = canvas
        self.nave = canvas.create_rectangle(280, 350, 320, 370, fill="white")
        self.velocidad_x = 0

    def mover(self, event):
        if event.keysym == "Left":
            self.velocidad_x = -5
        elif event.keysym == "Right":
            self.velocidad_x = 5
        elif event.keysym == "space":
            balas.append(Bala(canvas, self.canvas.coords(self.nave)[0] + 20, 350))

    def detener(self, event):
        self.velocidad_x = 0

    def actualizar(self):
        coords = self.canvas.coords(self.nave)
        if coords[0] + self.velocidad_x >= 0 and coords[2] + self.velocidad_x <= canvas_width:
            self.canvas.move(self.nave, self.velocidad_x, 0)

# Clase para las balas
class Bala:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.bala = canvas.create_rectangle(x - 2, y, x + 2, y - 10, fill="yellow")
        self.velocidad_y = -5

    def actualizar(self):
        self.canvas.move(self.bala, 0, self.velocidad_y)
        return self.canvas.coords(self.bala)

# Clase para los enemigos
class Enemigo:
    def __init__(self, canvas):
        self.canvas = canvas
        x = random.randint(0, canvas_width - 30)
        self.enemigo = canvas.create_rectangle(x, 0, x + 30, 30, fill="red")
        self.velocidad_y = 2

    def actualizar(self):
        self.canvas.move(self.enemigo, 0, self.velocidad_y)
        return self.canvas.coords(self.enemigo)

# Función para actualizar el juego
def actualizar_juego():
    # Mover la nave
    nave.actualizar()

    # Actualizar balas y enemigos
    for bala in balas[:]:
        if bala.actualizar()[1] <= 0:
            canvas.delete(bala.bala)
            balas.remove(bala)

    for enemigo in enemigos[:]:
        if enemigo.actualizar()[1] >= canvas_height:
            canvas.delete(enemigo.enemigo)
            enemigos.remove(enemigo)

    # Detectar colisiones
    for enemigo in enemigos[:]:
        enemigo_coords = canvas.coords(enemigo.enemigo)
        for bala in balas[:]:
            bala_coords = canvas.coords(bala.bala)
            if (enemigo_coords[0] < bala_coords[0] < enemigo_coords[2] and
                enemigo_coords[1] < bala_coords[1] < enemigo_coords[3]):
                canvas.delete(enemigo.enemigo)
                canvas.delete(bala.bala)
                enemigos.remove(enemigo)
                balas.remove(bala)
                break

        # Verificar colisión de enemigo con la nave
        nave_coords = canvas.coords(nave.nave)
        if (enemigo_coords[0] < nave_coords[2] and enemigo_coords[2] > nave_coords[0] and
            enemigo_coords[1] < nave_coords[3] and enemigo_coords[3] > nave_coords[1]):
            canvas.create_text(canvas_width/2, canvas_height/2, text="GAME OVER", fill="white", font=("Arial", 24))
            return

    # Generar enemigos aleatoriamente
    if random.randint(1, 100) > 97:
        enemigos.append(Enemigo(canvas))

    # Volver a ejecutar la actualización del juego
    root.after(30, actualizar_juego)

# Crear la nave
nave = Nave(canvas)

# Listas para balas y enemigos
balas = []
enemigos = []

# Controlar el movimiento de la nave
root.bind("<KeyPress>", nave.mover)
root.bind("<KeyRelease>", nave.detener)

# Iniciar el juego
actualizar_juego()

# Ejecutar el bucle principal de la ventana
root.mainloop()
