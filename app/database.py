import sqlite3
import hashlib
import os

# Ruta absoluta del archivo de base de datos (../data/usuarios.db)
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "usuarios.db")


# ----------------------------------------
# Conexión y tablas
# ----------------------------------------

def conectar():
    """
    Establece y retorna la conexión con la base de datos.
    """
    return sqlite3.connect(DB_NAME)


def crear_tabla():
    """
    Crea la tabla de usuarios si no existe.
    Inserta también al usuario admin por defecto si no está en la base de datos.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            edad INTEGER NOT NULL,
            bloqueado INTEGER DEFAULT 0,
            nombre TEXT,
            apellidos TEXT,
            sexo TEXT
        )
    """)

    # Crear usuario admin si no existe
    cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO usuarios (username, password, edad, bloqueado, nombre)
            VALUES (?, ?, ?, ?, ?)
        """, ("admin", hash_password("admin2025"), 99, 0, "Administrador"))

    conn.commit()
    conn.close()


def crear_tabla_mensajes():
    """
    Crea la tabla de mensajes si no existe.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emisor TEXT NOT NULL,
            receptor TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# ----------------------------------------
# Funciones de autenticación y registro
# ----------------------------------------

def hash_password(password):
    """
    Hashea una contraseña usando MD5.
    """
    return hashlib.md5(password.encode()).hexdigest()


def registrar_usuario(username, password, edad, bloqueado=0):
    """
    Registra un nuevo usuario en la base de datos.
    Retorna True si el registro fue exitoso, False si el usuario ya existe.
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (username, password, edad, bloqueado)
            VALUES (?, ?, ?, ?)
        """, (username, hash_password(password), edad, bloqueado))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verificar_usuario(username, password):
    """
    Verifica si existe un usuario con esa combinación usuario/contraseña.
    Devuelve los datos si es válido, None si no lo es.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, edad, bloqueado FROM usuarios
        WHERE username = ? AND password = ?
    """, (username, hash_password(password)))
    result = cursor.fetchone()
    conn.close()
    return result


# ----------------------------------------
# Funciones de perfil
# ----------------------------------------

def obtener_datos_usuario(username):
    """
    Devuelve todos los datos personales de un usuario específico.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, apellidos, sexo, username, password, edad
        FROM usuarios
        WHERE username = ?
    """, (username,))
    datos = cursor.fetchone()
    conn.close()
    return datos


def actualizar_datos_usuario(username, nombre, apellidos, sexo, nueva_contra=None):
    """
    Actualiza los datos del perfil de un usuario.
    Si se indica nueva contraseña, también se actualiza.
    """
    conn = conectar()
    cursor = conn.cursor()
    if nueva_contra:
        hashed_pw = hash_password(nueva_contra)
        cursor.execute("""
            UPDATE usuarios
            SET nombre = ?, apellidos = ?, sexo = ?, password = ?
            WHERE username = ?
        """, (nombre, apellidos, sexo, hashed_pw, username))
    else:
        cursor.execute("""
            UPDATE usuarios
            SET nombre = ?, apellidos = ?, sexo = ?
            WHERE username = ?
        """, (nombre, apellidos, sexo, username))
    conn.commit()
    conn.close()


# ----------------------------------------
# Funciones de administración
# ----------------------------------------

def obtener_todos_los_usuarios():
    """
    Devuelve una lista con todos los usuarios, excepto el admin.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, bloqueado FROM usuarios
        WHERE username != 'admin'
    """)
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios


def actualizar_estado_bloqueo(username, estado):
    """
    Cambia el estado de bloqueo de un usuario (0 o 1).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET bloqueado = ? WHERE username = ?", (estado, username))
    conn.commit()
    conn.close()


def eliminar_usuario(username):
    """
    Elimina completamente un usuario de la base de datos.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
    conn.commit()
    conn.close()


# ----------------------------------------
# Funciones de mensajes
# ----------------------------------------

def enviar_mensaje(emisor, receptor, mensaje):
    """
    Guarda un nuevo mensaje entre usuarios.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mensajes (emisor, receptor, mensaje)
        VALUES (?, ?, ?)
    """, (emisor, receptor, mensaje))
    conn.commit()
    conn.close()


def obtener_mensajes_receptor(usuario):
    """
    Devuelve los mensajes recibidos por un usuario, ordenados por fecha.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, emisor, mensaje, fecha
        FROM mensajes
        WHERE receptor = ?
        ORDER BY fecha DESC
    """, (usuario,))
    mensajes = cursor.fetchall()
    conn.close()
    return mensajes


def obtener_usuarios_destinatarios(excluir=None):
    """
    Devuelve una lista de usuarios a los que se les puede enviar mensajes.
    Se excluye a 'admin' y al propio usuario (si se indica).
    """
    conn = conectar()
    cursor = conn.cursor()
    if excluir:
        cursor.execute("SELECT username FROM usuarios WHERE username != 'admin' AND username != ?", (excluir,))
    else:
        cursor.execute("SELECT username FROM usuarios WHERE username != 'admin'")
    usuarios = [row[0] for row in cursor.fetchall()]
    conn.close()
    return usuarios


def eliminar_mensaje(id_mensaje):
    """
    Elimina un mensaje por su ID.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mensajes WHERE id = ?", (id_mensaje,))
    conn.commit()
    conn.close()
