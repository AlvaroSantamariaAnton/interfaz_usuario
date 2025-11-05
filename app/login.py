from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from app import database
from app.register import Registro
from app import excep

class Login:
    def __init__(self, window_login):
        self.window = window_login
        self.window.title("Ventana de acceso")
        self.window.geometry("420x400")
        self.window.resizable(0, 0)

        database.crear_tabla()

        frame_enc = Frame(window_login)
        frame_enc.pack()

        img_login = Image.open("img/login.png")
        img_render = ImageTk.PhotoImage(img_login.resize((30, 30)))
        label_img = Label(frame_enc, image=img_render)
        label_img.image = img_render
        label_img.grid(row=0, column=0, sticky='s', padx=10, pady=30)

        Label(frame_enc, text="INICIAR SESIÓN", fg="black", font=("Comic Sans", 15), pady=10).grid(row=0, column=1)

        frame_form = LabelFrame(window_login, text="Datos", font=("Comic Sans", 11))
        frame_form.pack()

        Label(frame_form, text="Usuario: ", font=("Comic Sans", 13)).grid(row=0, column=0, padx=10, pady=(30, 15))
        self.user = Entry(frame_form, width=25, font=("Comic Sans", 13))
        self.user.grid(row=0, column=1, padx=10, pady=(30, 15))

        Label(frame_form, text="Contraseña: ", font=("Comic Sans", 13)).grid(row=1, column=0, padx=10, pady=(15, 30))
        self.passw = Entry(frame_form, width=25, font=("Comic Sans", 13), show="*")
        self.passw.grid(row=1, column=1, padx=10, pady=(15, 30))

        self.show_password = False
        self.toggle_btn = Button(frame_form, text="👁", command=self.toggle_password)
        self.toggle_btn.grid(row=1, column=2, padx=(0, 10), pady=(15, 30))

        frame_btn = Frame(window_login)
        frame_btn.pack()

        Button(frame_btn, text="Acceder", command=self.loginuser, height=2, width=12, bg="black", fg="#ffffff", font=("Comic Sans", 13)).grid(row=0, column=0, padx=10, pady=10)
        Button(frame_btn, text="Registrarse", command=self.abrir_registro, height=2, width=12, bg="gray", fg="#ffffff", font=("Comic Sans", 13)).grid(row=0, column=1, padx=10, pady=10)

    def toggle_password(self):
        self.show_password = not self.show_password
        self.passw.config(show="" if self.show_password else "*")

    def loginuser(self, username=None, password=None):
        user = username if username else self.user.get().strip()
        pw = password if password else self.passw.get().strip()

        datos = database.verificar_usuario(user, pw)
        if datos:
            nombre, edad, bloqueado = datos
            try:
                if edad < 18:
                    raise excep.MenorEdadError("Acceso denegado: el usuario es menor de edad.")
                if bloqueado:
                    raise excep.UsuarioBloqueadoError("Acceso denegado: el usuario está bloqueado.")
                messagebox.showinfo("BIENVENIDO", f"Bienvenido {nombre}")
                self.usuario_logado = user
                self.abrir_programa()
            except (excep.MenorEdadError, excep.UsuarioBloqueadoError) as e:
                messagebox.showwarning("Acceso restringido", str(e))
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def abrir_programa(self):
        self.window.destroy()
        self.panel_window = Tk()
        self.panel_window.title("Panel de Usuario")
        self.panel_window.geometry("500x400")

        frame = Frame(self.panel_window)
        frame.pack(pady=40)

        Label(frame, text="Bienvenido a tu panel privado", font=("Arial", 18)).pack(pady=10)

        Button(frame, text="Mi perfil", font=("Arial", 12), width=20, command=self.ver_perfil).pack(pady=5)
        Button(frame, text="Ajustes", font=("Arial", 12), width=20, command=self.abrir_ajustes).pack(pady=5)
        Button(frame, text="Cerrar sesión", font=("Arial", 12), width=20, fg="red", command=self.panel_window.destroy).pack(pady=20)

        self.panel_window.mainloop()

    def abrir_registro(self):
        reg_window = Toplevel(self.window)
        Registro(reg_window, self.loginuser)

    def ver_perfil(self):
        datos = database.obtener_datos_usuario(self.usuario_logado)
        if not datos:
            messagebox.showerror("Error", "No se pudieron cargar los datos del perfil.")
            return

        nombre, apellidos, sexo, username, password, edad = datos

        perfil_window = Toplevel(self.panel_window)
        perfil_window.title("Mi perfil")
        perfil_window.geometry("400x400")

        frame = Frame(perfil_window)
        frame.pack(pady=20)

        Label(frame, text="Mi perfil", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        Label(frame, text="Nombre:", font=("Arial", 12)).grid(row=1, column=0, sticky=W, padx=10)
        Label(frame, text=nombre or "(sin datos)", font=("Arial", 12)).grid(row=1, column=1, sticky=W)

        Label(frame, text="Apellidos:", font=("Arial", 12)).grid(row=2, column=0, sticky=W, padx=10)
        Label(frame, text=apellidos or "(sin datos)", font=("Arial", 12)).grid(row=2, column=1, sticky=W)

        Label(frame, text="Sexo:", font=("Arial", 12)).grid(row=3, column=0, sticky=W, padx=10)
        Label(frame, text=sexo or "(sin datos)", font=("Arial", 12)).grid(row=3, column=1, sticky=W)

        Label(frame, text="Usuario:", font=("Arial", 12)).grid(row=4, column=0, sticky=W, padx=10)
        Label(frame, text=username, font=("Arial", 12)).grid(row=4, column=1, sticky=W)

        Label(frame, text="Edad:", font=("Arial", 12)).grid(row=5, column=0, sticky=W, padx=10)
        Label(frame, text=str(edad), font=("Arial", 12)).grid(row=5, column=1, sticky=W)

        Button(perfil_window, text="Cerrar", command=perfil_window.destroy).pack(pady=20)

    def abrir_ajustes(self):
        datos = database.obtener_datos_usuario(self.usuario_logado)
        if not datos:
            messagebox.showerror("Error", "No se pudieron cargar los datos.")
            return

        nombre, apellidos, sexo, username, _, _ = datos

        ajustes_window = Toplevel(self.panel_window)
        ajustes_window.title("Ajustes del perfil")
        ajustes_window.geometry("400x400")

        frame = Frame(ajustes_window)
        frame.pack(pady=20)

        Label(frame, text="Editar perfil", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        Label(frame, text="Nombre:", font=("Arial", 12)).grid(row=1, column=0, sticky=W, padx=10)
        entry_nombre = Entry(frame, font=("Arial", 12))
        entry_nombre.insert(0, nombre or "")
        entry_nombre.grid(row=1, column=1, columnspan=2, pady=5)

        Label(frame, text="Apellidos:", font=("Arial", 12)).grid(row=2, column=0, sticky=W, padx=10)
        entry_apellidos = Entry(frame, font=("Arial", 12))
        entry_apellidos.insert(0, apellidos or "")
        entry_apellidos.grid(row=2, column=1, columnspan=2, pady=5)

        Label(frame, text="Sexo:", font=("Arial", 12)).grid(row=3, column=0, sticky=W, padx=10)
        sexo_var = StringVar()
        sexo_var.set(sexo if sexo in ("Hombre", "Mujer") else "")
        sexo_menu = OptionMenu(frame, sexo_var, "Hombre", "Mujer")
        sexo_menu.grid(row=3, column=1, columnspan=2, pady=5)

        Label(frame, text="Nueva contraseña:", font=("Arial", 12)).grid(row=4, column=0, sticky=W, padx=10)
        entry_pass = Entry(frame, font=("Arial", 12), show="*")
        entry_pass.grid(row=4, column=1, pady=5)

        show_pw = False
        def toggle_pw():
            nonlocal show_pw
            show_pw = not show_pw
            entry_pass.config(show="" if show_pw else "*")

        Button(frame, text="👁", command=toggle_pw).grid(row=4, column=2, padx=5)

        def aplicar_cambios():
            nuevo_nombre = entry_nombre.get().strip()
            nuevos_apellidos = entry_apellidos.get().strip()
            nuevo_sexo = sexo_var.get()
            nueva_pass = entry_pass.get().strip() or None

            database.actualizar_datos_usuario(username, nuevo_nombre, nuevos_apellidos, nuevo_sexo, nueva_pass)
            messagebox.showinfo("Cambios aplicados", "Tu perfil ha sido actualizado.")
            ajustes_window.destroy()

        Button(ajustes_window, text="Aplicar cambios", command=aplicar_cambios, bg="green", fg="white").pack(pady=10)
        Button(ajustes_window, text="Cancelar", command=ajustes_window.destroy).pack()
