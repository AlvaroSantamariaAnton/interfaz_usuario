# Módulo con utilidades reutilizables en toda la aplicación

def centrar_ventana(ventana, ancho, alto):
    """
    Centra una ventana de Tkinter en la pantalla.

    Parámetros:
        ventana: la instancia de Tk() o Toplevel()
        ancho (int): ancho deseado de la ventana
        alto (int): alto deseado de la ventana
    """

    ventana.update_idletasks()
    # Obtenemos las dimensiones de la pantalla del usuario
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Calculamos la posición centrada
    x = (screen_width // 2) - (ancho // 2)
    y = (screen_height // 2) - (alto // 2)

    # Aplicamos la geometría centrada a la ventana
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
