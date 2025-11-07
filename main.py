from tkinter import Tk
from app.login import Login
from app.utils import centrar_ventana

if __name__ == "__main__":
    root = Tk()
    centrar_ventana(root, 420, 400)
    app = Login(root)
    root.mainloop()
