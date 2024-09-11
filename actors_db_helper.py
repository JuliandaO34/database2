import os
import mysql.connector
from mysql.connector import Error


def insert_performances_in_bulk(df, table_name='performances'):
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            
            insert_query = f"""
            INSERT INTO {table_name} (Performances_Date, Performances_Hour, Name_Performances, Performances_Price)
            VALUES (%s, %s, %s, %s)
            """  

            
            performances_data = df[['Performances_Date', 'Performances_Hour', 'Name_Performances', 'Performances_Price']].values.tolist()

            
            cursor.executemany(insert_query, performances_data)


            connection.commit()

            print(f"{cursor.rowcount} filas insertadas exitosamente en la tabla de performances.")

    except Error as e:
        print(f"Error durante la inserción: {e}")
        if connection:
            connection.rollback()  

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def insert_actors_in_bulk(df, performance_id, table_name='actors'):
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            
            insert_query = f"""
            INSERT INTO {table_name} (FullName, Code, Phone_Number, Email, performances_id)
            VALUES (%s, %s, %s, %s, %s)
            """

            actors_data = df[['FullName', 'Code', 'Phone_Number', 'Email']].values.tolist()
            for actor in actors_data:
                actor.append(performance_id)  

            cursor.executemany(insert_query, actors_data)

            connection.commit()

            print(f"{cursor.rowcount} filas insertadas exitosamente en la tabla de actores.")

    except Error as e:
        print(f"Error durante la inserción de actores: {e}")
        if connection:
            connection.rollback()  

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_joined_data():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()


            select_query = """
            SELECT a.FullName, a.Code, a.Phone_Number, a.Email, 
                p.Performances_Date, p.Performances_Hour, p.Name_Performances, p.Performances_Price
            FROM actors a
            JOIN performances p ON a.performances_id = p.id
            """

            cursor.execute(select_query)
            joined_data = cursor.fetchall()

            return joined_data

    except Error as e:
        print(f"Error durante la obtención de datos combinados: {e}")
        return []

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
