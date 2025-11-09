# Módulo con utilidades reutilizables en toda la aplicación

def centrar_ventana(ventana, ancho, alto):
    """
    Centra una ventana de Tkinter en la pantalla.
    """

    ventana.update_idletasks()  # Asegura que los datos de geometría están actualizados

    # Obtenemos las dimensiones de la pantalla del usuario
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Calculamos la posición centrada
    x = (screen_width // 2) - (ancho // 2)
    y = (screen_height // 2) - (alto // 2)

    # Aplicamos la geometría centrada a la ventana
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
