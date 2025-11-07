# Proyecto: Interfaz de Usuario en Tkinter

Aplicación desarrollada en **Python** con **Tkinter** que permite el registro, inicio de sesión y gestión de usuarios con distintos roles (usuario normal y administrador).  
Incluye un sistema de mensajería entre usuarios y un panel de control para administración.

---

## Estructura del proyecto

```
interfaz_usuario/
│
├── app/
│   ├── login.py          # Ventana principal de inicio de sesión y paneles
│   ├── register.py       # Ventana de registro de usuarios
│   ├── database.py       # Lógica de base de datos SQLite
│   ├── utils.py          # Función para centrar las ventanas
│   ├── excep.py          # Excepciones personalizadas
│
├── data/
│   ├── usuarios.db       # Base de datos SQLite ya inicializada con datos de ejemplo
│   ├── depuracion.csv    # CSV con datos útiles para depurar o modificar la base existente
│
├── img/
│   ├── login.png         # Icono del inicio de sesión
│
└── main.py               # Archivo principal que inicia la aplicación
```

---

## Cómo usar

1. Asegúrate de tener **Python 3.10 o superior** instalado en tu equipo.
2. Descarga o clona el proyecto completo.
3. Abre una terminal o CMD y navega a la carpeta del proyecto:

   ```bash
   cd interfaz_usuario
   ```

4. Ejecuta el programa principal:

   ```bash
   python main.py
   ```

5. Aparecerá la ventana de **inicio de sesión**:
   - Si eres un usuario nuevo, pulsa **“Registrarse”**.
   - Si ya tienes cuenta, introduce tus credenciales.
   - Si entras como **admin**, accederás al **panel de administración**.

---

## Requisitos

Para ejecutar el proyecto correctamente, instala la siguiente dependencia:

```bash
pip install pillow
```

> **Nota:** Tkinter viene incluido por defecto con la mayoría de instalaciones de Python.

---

## Notas importantes

- La base de datos (`usuarios.db`) **ya contiene usuarios y mensajes**, listos para probar la app desde el inicio.
- En la carpeta `data/` hay un archivo llamado **`depuracion.csv`**, con datos útiles para modificar o restaurar la base de datos sin complicaciones.
- El administrador puede:
  - Crear usuarios nuevos.
  - Bloquear/desbloquear cuentas.
  - Eliminar usuarios existentes.
- Los usuarios normales pueden:
  - Editar su perfil.
  - Enviar mensajes a otros usuarios (menos a sí mismos).
  - Leer y eliminar sus mensajes recibidos.
- Las contraseñas se almacenan encriptadas usando **MD5**.
- Todos los campos marcados con `*` son **obligatorios**.

---