import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv


load_dotenv()

def test_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Conectado a MySQL Server versión", db_info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("Conectado a la base de datos:", record)
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("Conexión a MySQL cerrada.")

if __name__ == "__main__":
    test_db_connection()
