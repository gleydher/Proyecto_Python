# pip install mysql-connector-python
import mysql.connector

class CConexion:
    def ConectorBaseDatos():
        try:
            conexion = mysql.connector.connect(
                user='root',
                password='',
                host='127.0.0.1',
                database='python',
                port='3306'
            )

            print("Conexión correcta")
            return conexion

        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos {}".format(error))
            return None  # Si hay error, no devuelve conexión válida


# Probar conexión al ejecutar directamente este archivo
if __name__ == "__main__":
    CConexion.ConectorBaseDatos()

