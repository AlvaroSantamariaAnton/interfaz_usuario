import re
from tkinter import *
from tkinter import messagebox
from app import database
from datetime import datetime
from app.utils import centrar_ventana

# Clase que define la ventana de registro de nuevos usuarios
class Registro:
    def __init__(self, root, login_callback, modo_admin=False):
        self.root = root
        self.root.title("Registro de usuario")
        centrar_ventana(self.root, 500, 350)
        self.login_callback = login_callback
        self.modo_admin = modo_admin

        frame = Frame(root)
        frame.pack(pady=20)

        # Campo: nombre de usuario (obligatorio)
        Label(frame, text="Usuario *:", font=("Arial", 12)).grid(row=0, column=0, pady=5, padx=10, sticky=E)
        self.entry_user = Entry(frame, font=("Arial", 12))
        self.entry_user.grid(row=0, column=1)

        # Campo: contraseña (obligatoria)
        Label(frame, text="Contraseña *:", font=("Arial", 12)).grid(row=1, column=0, pady=5, padx=10, sticky=E)
        self.entry_pass = Entry(frame, font=("Arial", 12), show="*")
        self.entry_pass.grid(row=1, column=1)

        # Botón para mostrar u ocultar la contraseña
        self.ver_pass = False
        self.toggle_btn = Button(frame, text="👁", command=self.toggle_password)
        self.toggle_btn.grid(row=1, column=2, padx=5)

        # Campo: fecha de nacimiento (obligatoria)
        Label(frame, text="Fecha nacimiento (DD-MM-YYYY) *:", font=("Arial", 12)).grid(row=2, column=0, pady=5, padx=10, sticky=E)
        self.entry_fecha = Entry(frame, font=("Arial", 12))
        self.entry_fecha.grid(row=2, column=1)

        # Campo: nombre (opcional)
        Label(frame, text="Nombre:", font=("Arial", 12)).grid(row=3, column=0, pady=5, padx=10, sticky=E)
        self.entry_nombre = Entry(frame, font=("Arial", 12))
        self.entry_nombre.grid(row=3, column=1)

        # Campo: apellidos (opcional)
        Label(frame, text="Apellidos:", font=("Arial", 12)).grid(row=4, column=0, pady=5, padx=10, sticky=E)
        self.entry_apellidos = Entry(frame, font=("Arial", 12))
        self.entry_apellidos.grid(row=4, column=1)

        # Campo: sexo (obligatorio)
        Label(frame, text="Sexo *:", font=("Arial", 12)).grid(row=5, column=0, pady=5, padx=10, sticky=E)
        self.sexo_var = StringVar()
        self.sexo_var.set("")   # valor vacío por defecto (obliga a elegir)
        OptionMenu(frame, self.sexo_var, "Hombre", "Mujer").grid(row=5, column=1)

        # Botón para registrar
        Button(root, text="Registrarse", font=("Arial", 12), command=self.registrar_usuario).pack(pady=20)

        # Texto que indica qué campos son obligatorios
        Label(root, text="(*) Campos obligatorios", font=("Arial", 10), fg="gray").pack()

    # Alterna la visibilidad del campo de contraseña
    def toggle_password(self):
        self.ver_pass = not self.ver_pass
        self.entry_pass.config(show="" if self.ver_pass else "*")

    # Lógica que se ejecuta al pulsar "Registrarse"
    def registrar_usuario(self):
        # Se obtienen los datos desde los campos del formulario
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        fecha_str = self.entry_fecha.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        sexo = self.sexo_var.get().strip()

        # Validación de campos obligatorios
        if not username or not password or not fecha_str or not sexo:
            messagebox.showwarning("Campos obligatorios", "Debes completar todos los campos marcados con *.")
            return

        # Validación del nombre de usuario (solo letras, números y guión bajo)
        if not validar_usuario(username):
            messagebox.showerror("Usuario inválido", "El nombre de usuario solo puede contener letras, números y guiones bajos.")
            return

        # Validación y cálculo de edad desde la fecha introducida
        try:
            fecha_nacimiento = datetime.strptime(fecha_str, "%d-%m-%Y")
            edad = calcular_edad(fecha_nacimiento)
            if edad < 0:
                messagebox.showerror("Fecha inválida", "La fecha de nacimiento no puede estar en el futuro.")
                return
        except ValueError:
            messagebox.showerror("Formato inválido", "Usa el formato DD-MM-YYYY para la fecha.")
            return

        # Registrar usuario en base de datos
        if database.registrar_usuario(username, password, edad, bloqueado=0):
            # Si el registro fue exitoso, guardar también los datos personales opcionales
            database.actualizar_datos_usuario(username, nombre, apellidos, sexo)
            messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
            self.root.destroy()

            # Si no es modo admin, iniciar sesión automáticamente
            if not self.modo_admin and self.login_callback:
                self.login_callback(username, password)
        else:
            messagebox.showerror("Error", "El usuario ya existe.")

# Función auxiliar para calcular edad exacta a partir de la fecha de nacimiento
def calcular_edad(fecha_nac):
    hoy = datetime.today()
    edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
    return edad

# Función auxiliar para validar el nombre de usuario
# Solo se permiten letras, números y guiones bajos
def validar_usuario(username):
    return bool(re.match(r'^[a-zA-Z0-9_]+$', username))
