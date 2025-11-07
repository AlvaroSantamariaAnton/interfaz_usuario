from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from app import database
from app.register import Registro
from app import excep
from app.utils import centrar_ventana

# Clase principal que gestiona el inicio de sesión y navegación de usuario/admin
class Login:
    def __init__(self, window_login):
        self.window = window_login
        self.window.title("Ventana de acceso")
        centrar_ventana(self.window, 420, 400)
        self.window.resizable(0, 0)

        # Asegurar que las tablas de la base de datos existen
        database.crear_tabla()
        database.crear_tabla_mensajes()

        frame_enc = Frame(window_login)
        frame_enc.pack()

        # Carga y muestra una imagen (icono de login)
        img_login = Image.open("img/login.png")
        img_render = ImageTk.PhotoImage(img_login.resize((30, 30)))
        label_img = Label(frame_enc, image=img_render)
        label_img.image = img_render
        label_img.grid(row=0, column=0, sticky='s', padx=10, pady=30)

        Label(frame_enc, text="INICIAR SESIÓN", fg="black", font=("Arial", 15), pady=10).grid(row=0, column=1)

        # Frame donde estarán los campos de entrada del formulario
        frame_form = LabelFrame(window_login, text="Datos", font=("Arial", 11))
        frame_form.pack()

        # Campo de entrada para el nombre de usuario
        Label(frame_form, text="Usuario: ", font=("Arial", 13)).grid(row=0, column=0, padx=10, pady=(30, 15))
        self.user = Entry(frame_form, width=25, font=("Arial", 13))
        self.user.grid(row=0, column=1, padx=10, pady=(30, 15))

        # Campo de entrada para la contraseña (oculta por defecto)
        Label(frame_form, text="Contraseña: ", font=("Arial", 13)).grid(row=1, column=0, padx=10, pady=(15, 30))
        self.passw = Entry(frame_form, width=25, font=("Arial", 13), show="*")
        self.passw.grid(row=1, column=1, padx=10, pady=(15, 30))

        # Botón para mostrar/ocultar contraseña
        self.show_password = False
        self.toggle_btn = Button(frame_form, text="👁", command=self.toggle_password)
        self.toggle_btn.grid(row=1, column=2, padx=(0, 10), pady=(15, 30))

        # Botones para acceder o registrarse
        frame_btn = Frame(window_login)
        frame_btn.pack()

        Button(frame_btn, text="Acceder", command=self.loginuser, height=2, width=12, bg="black", fg="#ffffff", font=("Arial", 13)).grid(row=0, column=0, padx=10, pady=10)
        Button(frame_btn, text="Registrarse", command=self.abrir_registro, height=2, width=12, bg="gray", fg="#ffffff", font=("Arial", 13)).grid(row=0, column=1, padx=10, pady=10)

    # Método para alternar la visibilidad del campo de contraseña
    def toggle_password(self):
        self.show_password = not self.show_password
        self.passw.config(show="" if self.show_password else "*")

    # Método principal para iniciar sesión
    # Permite autologin si se le pasan username y password como argumentos
    def loginuser(self, username=None, password=None):
        # Si se pasaron credenciales, usarlas; si no, leer del formulario
        user = username if username else self.user.get().strip()
        pw = password if password else self.passw.get().strip()

        # Verifica en la base de datos si el usuario existe y es válido
        datos = database.verificar_usuario(user, pw)
        if datos:
            username_bd, edad, bloqueado = datos
            try:
                # Si el usuario es "admin", abrir el panel de administración
                if username_bd == "admin":
                    self.window.destroy()
                    self.abrir_panel_admin()
                    return

                # Comprobar si el usuario es menor de edad
                if edad < 18:
                    raise excep.MenorEdadError("Acceso denegado: el usuario es menor de edad.")
                
                # Comprobar si el usuario está bloqueado
                if bloqueado:
                    raise excep.UsuarioBloqueadoError("Acceso denegado: el usuario está bloqueado.")
                
                # Usuario válido: guardar sesión e ir al panel de usuario
                self.usuario_logado = user
                self.abrir_programa()

            except (excep.MenorEdadError, excep.UsuarioBloqueadoError) as e:
                messagebox.showwarning("Acceso restringido", str(e))
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    # Abre el panel principal para usuarios normales
    def abrir_programa(self):
        self.window.destroy()   # Cierra la ventana de login
        
        self.panel_window = Tk()
        self.panel_window.title("Panel de Usuario")

        # Centra la ventana del panel de usuario
        centrar_ventana(self.panel_window, 400, 350)

        frame = Frame(self.panel_window)
        frame.pack(pady=40)

        # Mensaje de bienvenida y botones de navegación
        Label(frame, text="Bienvenido a tu panel privado", font=("Arial", 18)).pack(pady=10)

        Button(frame, text="Mi perfil", font=("Arial", 12), width=20, command=self.ver_perfil).pack(pady=5)
        Button(frame, text="Mensajes", font=("Arial", 12), width=20, command=self.abrir_mensajes).pack(pady=5)
        Button(frame, text="Ajustes", font=("Arial", 12), width=20, command=self.abrir_ajustes).pack(pady=5)
        Button(frame, text="Cerrar sesión", font=("Arial", 12), width=20, fg="red", command=self.panel_window.destroy).pack(pady=20)

        self.panel_window.mainloop()

    # Abre el panel para el usuario administrador
    def abrir_panel_admin(self):
            self.admin_window = Tk()
            self.admin_window.title("Panel Administrador")

            # Centrar ventana de administración
            centrar_ventana(self.admin_window, 400, 300)

            # Título y botones del panel de administrador
            Label(self.admin_window, text="Panel de Administración", font=("Arial", 16)).pack(pady=20)

            Button(self.admin_window, text="Gestionar Usuarios", font=("Arial", 12), width=25, command=self.gestionar_usuarios).pack(pady=10)
            Button(self.admin_window, text="Añadir Usuario", font=("Arial", 12), width=25, command=self.abrir_registro_admin).pack(pady=10)
            Button(self.admin_window, text="Cerrar sesión", font=("Arial", 12), width=25, fg="red", command=self.admin_window.destroy).pack(pady=20)

            self.admin_window.mainloop()

    # Abre la ventana de registro para un nuevo usuario (desde login)
    def abrir_registro(self):
        # Creamos una nueva ventana secundaria
        reg_window = Toplevel(self.window)
        # Mostramos el formulario de registro
        Registro(reg_window, self.loginuser)    # Le pasamos la función de login para hacer login automático tras registrarse

    # Abre la ventana de registro desde el panel de administración
    def abrir_registro_admin(self):
            reg_window = Toplevel(self.admin_window)
            # En este caso no hay login automático tras registrar, y se indica que es modo admin
            Registro(reg_window, login_callback=None, modo_admin=True)

    # Muestra una lista de todos los usuarios para gestión por el administrador
    def gestionar_usuarios(self):
            # Carga todos los usuarios desde la base de datos
            usuarios = database.obtener_todos_los_usuarios()

            # Crea una nueva ventana para gestionar usuarios
            gestion_win = Toplevel(self.admin_window)
            gestion_win.title("Gestionar Usuarios")
            centrar_ventana(gestion_win, 600, 600)

            Label(gestion_win, text="Usuarios Registrados", font=("Arial", 14)).pack(pady=10)

            frame = Frame(gestion_win)
            frame.pack(pady=10)

            # Recorremos los usuarios y creamos una fila para cada uno
            for i, (username, bloqueado) in enumerate(usuarios):
                # Muestra el nombre del usuario
                Label(frame, text=username, font=("Arial", 11), width=15, anchor="w").grid(row=i, column=0, padx=5, pady=5)

                # Muestra el estado de bloqueo actual
                estado = StringVar(value="Bloqueado" if bloqueado else "Activo")
                estado_label = Label(frame, textvariable=estado, width=10)
                estado_label.grid(row=i, column=1)

                # Función para alternar el estado de bloqueo del usuario
                def make_toggle(u=username, e=estado):
                    def toggle():
                        nuevo_estado = 0 if e.get() == "Bloqueado" else 1
                        database.actualizar_estado_bloqueo(u, nuevo_estado)
                        e.set("Bloqueado" if nuevo_estado else "Activo")
                    return toggle

                Button(frame, text="Bloquear/Desbloquear", command=make_toggle()).grid(row=i, column=2)

                # Función para eliminar un usuario, con confirmación
                def make_eliminar(u=username):
                    def eliminar():
                        if messagebox.askyesno("Eliminar", f"¿Eliminar usuario '{u}'?"):
                            database.eliminar_usuario(u)
                            gestion_win.destroy()
                            self.gestionar_usuarios()   # Recargar la lista actualizada
                    return eliminar

                Button(frame, text="Eliminar", fg="red", command=make_eliminar()).grid(row=i, column=3, padx=5)

    # Muestra la ventana con los datos del perfil del usuario logueado            
    def ver_perfil(self):
        # Consulta los datos desde la base de datos
        datos = database.obtener_datos_usuario(self.usuario_logado)
        if not datos:
            messagebox.showerror("Error", "No se pudieron cargar los datos del perfil.")
            return

        nombre, apellidos, sexo, username, password, edad = datos

        # Nueva ventana para mostrar el perfil
        perfil_window = Toplevel(self.panel_window)
        perfil_window.title("Mi perfil")
        centrar_ventana(perfil_window, 350, 300)

        frame = Frame(perfil_window)
        frame.pack(pady=20)

        Label(frame, text="Mi perfil", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Mostrar cada campo del perfil en filas
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

    # Abre la ventana de ajustes para modificar datos del perfil
    def abrir_ajustes(self):
        # Obtiene los datos actuales del usuario
        datos = database.obtener_datos_usuario(self.usuario_logado)
        if not datos:
            messagebox.showerror("Error", "No se pudieron cargar los datos.")
            return

        nombre, apellidos, sexo, username, _, _ = datos

        ajustes_window = Toplevel(self.panel_window)
        ajustes_window.title("Ajustes del perfil")
        centrar_ventana(ajustes_window, 400, 350)

        frame = Frame(ajustes_window)
        frame.pack(pady=20)

        Label(frame, text="Editar perfil", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        # Campos para editar los datos del perfil
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
        # Función para mostrar/ocultar la nueva contraseña
        def toggle_pw():
            nonlocal show_pw
            show_pw = not show_pw
            entry_pass.config(show="" if show_pw else "*")

        Button(frame, text="👁", command=toggle_pw).grid(row=4, column=2, padx=5)

        # Función para aplicar los cambios realizados
        def aplicar_cambios():
            nuevo_nombre = entry_nombre.get().strip()
            nuevos_apellidos = entry_apellidos.get().strip()
            nuevo_sexo = sexo_var.get()
            nueva_pass = entry_pass.get().strip() or None

            # Actualiza los datos en la base de datos
            database.actualizar_datos_usuario(username, nuevo_nombre, nuevos_apellidos, nuevo_sexo, nueva_pass)
            messagebox.showinfo("Cambios aplicados", "Tu perfil ha sido actualizado.")
            ajustes_window.destroy()

        # Botones para aplicar o cancelar los cambios
        Button(ajustes_window, text="Aplicar cambios", command=aplicar_cambios, bg="green", fg="white").pack(pady=10)
        Button(ajustes_window, text="Cancelar", command=ajustes_window.destroy).pack()

    # Muestra los mensajes que ha recibido el usuario logueado
    def abrir_mensajes(self):
        mensajes_win = Toplevel(self.panel_window)
        mensajes_win.title("Mis mensajes")
        centrar_ventana(mensajes_win, 550, 400)

        # Obtener mensajes desde la base de datos
        mensajes = database.obtener_mensajes_receptor(self.usuario_logado)

        Label(mensajes_win, text="Mensajes recibidos", font=("Arial", 14)).pack(pady=10)

        frame = Frame(mensajes_win)
        frame.pack(fill=BOTH, expand=True)

        if not mensajes:
            # Mostrar aviso si no hay mensajes
            Label(frame, text="No tienes mensajes.", font=("Arial", 12), fg="gray").pack(pady=20)
        else:
            for id_msg, emisor, texto, fecha in mensajes:
                vista_previa = (texto[:60] + "...") if len(texto) > 60 else texto

                fila = Frame(frame)
                fila.pack(fill=X, pady=4, padx=10)

                # Botón para ver el mensaje completo
                msg_btn = Button(
                    fila,
                    text=f"De: {emisor} | {fecha}\n{vista_previa}",
                    anchor="w",
                    justify=LEFT,
                    wraplength=400,
                    command=lambda m=(id_msg, emisor, texto, fecha): self.ver_mensaje_detalle(m)
                )
                msg_btn.pack(side=LEFT, fill=X, expand=True)

                # Botón para eliminar el mensaje
                eliminar_btn = Button(
                    fila,
                    text="🗑",
                    fg="red",
                    command=lambda idm=id_msg: self.eliminar_mensaje_confirmado(idm, mensajes_win)
                )
                eliminar_btn.pack(side=RIGHT, padx=5)
        
        # Botón para redactar mensaje nuevo
        Button(mensajes_win, text="Enviar mensaje", command=self.enviar_mensaje_popup).pack(pady=10)

    # Abre una ventana para enviar un nuevo mensaje a otro usuario
    def enviar_mensaje_popup(self):
        popup = Toplevel(self.panel_window)
        popup.title("Enviar mensaje")
        centrar_ventana(popup, 400, 300)

        Label(popup, text="Enviar mensaje", font=("Arial", 14)).pack(pady=10)

        frame = Frame(popup)
        frame.pack(pady=10)

        # Lista de usuarios válidos para enviar mensajes
        Label(frame, text="Para:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=E)
        usuarios = database.obtener_usuarios_destinatarios(excluir=self.usuario_logado)
        if not usuarios:
            messagebox.showerror("Error", "No hay usuarios disponibles para enviar mensajes.")
            popup.destroy()
            return

        destinatario_var = StringVar()
        destinatario_var.set(usuarios[0])   # primer usuario por defecto

        dropdown = OptionMenu(frame, destinatario_var, *usuarios)
        dropdown.config(font=("Arial", 12))
        dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Campo de texto para el mensaje
        Label(frame, text="Mensaje:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=NE)
        text_mensaje = Text(frame, font=("Arial", 12), height=6, width=30)
        text_mensaje.grid(row=1, column=1, padx=5, pady=5)

        # Acción de enviar mensaje
        def enviar():
            destinatario = destinatario_var.get()
            contenido = text_mensaje.get("1.0", END).strip()
            if not contenido:
                messagebox.showwarning("Campos vacíos", "Debes escribir un mensaje.")
                return
            if destinatario == self.usuario_logado:
                messagebox.showwarning("Error", "No puedes enviarte mensajes a ti mismo.")
                return
            database.enviar_mensaje(self.usuario_logado, destinatario, contenido)
            messagebox.showinfo("Enviado", "Mensaje enviado correctamente.")
            popup.destroy()

        Button(popup, text="Enviar", command=enviar, bg="blue", fg="white").pack(pady=10)

    # Muestra el contenido completo de un mensaje recibido
    def ver_mensaje_detalle(self, mensaje_info):
        id_mensaje, emisor, contenido, fecha = mensaje_info

        detalle = Toplevel(self.panel_window)
        detalle.title("Detalle del mensaje")
        centrar_ventana(detalle, 400, 300)

        Label(detalle, text=f"De: {emisor}", font=("Arial", 12)).pack(pady=5)
        Label(detalle, text=f"Fecha: {fecha}", font=("Arial", 10)).pack(pady=5)

        frame = Frame(detalle)
        frame.pack(pady=10, expand=True, fill=BOTH)

        # Caja de texto que muestra el mensaje en formato solo lectura
        text_box = Text(frame, wrap=WORD, font=("Arial", 11))
        text_box.insert(END, contenido)
        text_box.config(state=DISABLED)
        text_box.pack(expand=True, fill=BOTH, padx=10, pady=5)

        Button(detalle, text="Volver", command=detalle.destroy).pack(pady=10)

    # Elimina un mensaje después de confirmar con el usuario
    def eliminar_mensaje_confirmado(self, id_mensaje, ventana_actual):
        if messagebox.askyesno("Eliminar", "¿Seguro que deseas eliminar este mensaje?"):
            database.eliminar_mensaje(id_mensaje)
            ventana_actual.destroy()    # Cierra la vista actual
            self.abrir_mensajes()   # Recarga los mensajes actualizados
