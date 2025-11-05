from tkinter import *
from tkinter import messagebox
from app import database
from datetime import datetime

class Registro:
    def __init__(self, root, login_callback):
        self.root = root
        self.root.title("Registro de usuario")
        self.root.geometry("400x350")
        self.login_callback = login_callback

        frame = Frame(root)
        frame.pack(pady=20)

        Label(frame, text="Usuario:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky=E)
        self.entry_user = Entry(frame, font=("Arial", 12))
        self.entry_user.grid(row=0, column=1)

        Label(frame, text="Contraseña:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky=E)
        self.entry_pass = Entry(frame, font=("Arial", 12), show="*")
        self.entry_pass.grid(row=1, column=1)

        self.ver_pass = False
        self.toggle_btn = Button(frame, text="👁", command=self.toggle_password)
        self.toggle_btn.grid(row=1, column=2, padx=5)

        Label(frame, text="Fecha nacimiento (DD-MM-YYYY):", font=("Arial", 12)).grid(row=2, column=0, pady=10, padx=10, sticky=E)
        self.entry_fecha = Entry(frame, font=("Arial", 12))
        self.entry_fecha.grid(row=2, column=1)

        Button(root, text="Registrarse", font=("Arial", 12), command=self.registrar_usuario).pack(pady=20)

    def toggle_password(self):
        self.ver_pass = not self.ver_pass
        self.entry_pass.config(show="" if self.ver_pass else "*")

    def registrar_usuario(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        fecha_str = self.entry_fecha.get().strip()

        if not username or not password or not fecha_str:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos obligatorios.")
            return

        try:
            fecha_nacimiento = datetime.strptime(fecha_str, "%d-%m-%Y")
            edad = int((datetime.today() - fecha_nacimiento).days / 365.25)
        except ValueError:
            messagebox.showerror("Formato incorrecto", "La fecha debe tener el formato DD-MM-YYYY.")
            return

        if edad < 0:
            messagebox.showerror("Edad inválida", "La fecha introducida no es válida.")
            return

        creado = database.registrar_usuario(username, password, edad)
        if creado:
            messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente. Iniciando sesión...")
            self.root.destroy()
            self.login_callback(username, password)
        else:
            messagebox.showerror("Error", "El usuario ya existe.")
