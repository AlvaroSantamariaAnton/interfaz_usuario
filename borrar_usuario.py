import sqlite3
import os

# Ruta a la base de datos
DB_PATH = os.path.join("data", "usuarios.db")

def borrar_usuario(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    usuario = cursor.fetchone()

    if not usuario:
        print(f"❌ El usuario '{username}' no existe.")
    else:
        cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
        conn.commit()
        print(f"✅ Usuario '{username}' eliminado correctamente.")

    conn.close()

if __name__ == "__main__":
    usuario = input("Introduce el nombre de usuario a eliminar: ").strip()
    borrar_usuario(usuario)
