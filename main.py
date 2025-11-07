from tkinter import Tk
from app.login import Login
from app.utils import centrar_ventana

# Punto de entrada del programa
if __name__ == "__main__":
    # Crear una instancia de la ventana principal de Tkinter
    root = Tk()

    # Centrar la ventana en la pantalla
    centrar_ventana(root, 420, 400)
    
    # Inicializar la interfaz de login, pasándole la ventana principal
    app = Login(root)
    
    # Iniciar el bucle principal de la aplicación (mantiene la ventana abierta)
    root.mainloop()
