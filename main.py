from tkinter import Tk
from app.login import Login
from app.utils import centrar_ventana


# ----------------------------------------------
# Punto de entrada principal del programa
# ----------------------------------------------
if __name__ == "__main__":
    # Se crea la ventana principal de la aplicación con Tkinter
    root = Tk()

    # Se centra la ventana en pantalla con dimensiones específicas
    centrar_ventana(root, 420, 400)
    
    # Se instancia la clase Login, pasando la ventana como argumento
    app = Login(root)
    
    # Se inicia el bucle principal de Tkinter (para mantener la ventana abierta)
    root.mainloop()
