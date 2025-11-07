import sqlite3
import hashlib
import os

# Definir la ruta de la base de datos
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "usuarios.db")

# Conexión a la base de datos
def conectar():
    return sqlite3.connect(DB_NAME)

# Crear tabla de usuarios si no existe
def crear_tabla():
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

# Función para hashear contraseñas
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Registra un nuevo usuario
def registrar_usuario(username, password, edad, bloqueado=0):
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

# Verifica si un usuario existe y si la contraseña coincide
def verificar_usuario(username, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, edad, bloqueado FROM usuarios
        WHERE username = ? AND password = ?
    """, (username, hash_password(password)))
    result = cursor.fetchone()
    conn.close()
    return result

# Obtiene los datos de un usuario concreto
def obtener_datos_usuario(username):
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

# Guarda información adicional del usuario (perfil)
def actualizar_datos_usuario(username, nombre, apellidos, sexo, nueva_contra=None):
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

# Consulta todos los usuarios (usado por admin)
def obtener_todos_los_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, bloqueado FROM usuarios
        WHERE username != 'admin'
    """)
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

# Cambia el estado de bloqueo de un usuario
def actualizar_estado_bloqueo(username, estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET bloqueado = ? WHERE username = ?", (estado, username))
    conn.commit()
    conn.close()

# Elimina un usuario
def eliminar_usuario(username):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
    conn.commit()
    conn.close()

# Crea la tabla de mensajes si no existe
def crear_tabla_mensajes():
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

# Guarda un mensaje en la tabla de mensajes
def enviar_mensaje(emisor, receptor, mensaje):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mensajes (emisor, receptor, mensaje)
        VALUES (?, ?, ?)
    """, (emisor, receptor, mensaje))
    conn.commit()
    conn.close()

# Devuelve los mensajes recibidos por un usuario
def obtener_mensajes_receptor(usuario):
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

# Lista todos los usuarios a los que se puede enviar un mensaje (excepto el actual)
def obtener_usuarios_destinatarios(excluir=None):
    conn = conectar()
    cursor = conn.cursor()
    if excluir:
        cursor.execute("SELECT username FROM usuarios WHERE username != 'admin' AND username != ?", (excluir,))
    else:
        cursor.execute("SELECT username FROM usuarios WHERE username != 'admin'")
    usuarios = [row[0] for row in cursor.fetchall()]
    conn.close()
    return usuarios

# Elimina un mensaje por ID
def eliminar_mensaje(id_mensaje):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mensajes WHERE id = ?", (id_mensaje,))
    conn.commit()
    conn.close()
