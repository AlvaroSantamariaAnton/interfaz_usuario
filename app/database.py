import sqlite3
import hashlib
import os

DB_NAME = os.path.join("data", "usuarios.db")

def conectar():
    return sqlite3.connect(DB_NAME)

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
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

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
    