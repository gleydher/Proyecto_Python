from Conexion import *

class CCliente:
    def IngresarCliente(nombre, apellido, sexo):
        try:
            cone = CConexion.ConectorBaseDatos()
            cursor = cone.cursor()
            sql = "INSERT INTO usuario VALUES (NULL, %s, %s, %s);"

            # La variable 'valores' tiene que ser una tupla -> array que no se puede modificar
            # Como mínima expresión es: (valor,) la coma hace que sea una tupla
            # Las tuplas son listas inmutables, eso quiere decir que no se pueden modificar
            valores = (nombre, apellido, sexo)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "registro ingresado")
            cone.close()

        except mysql.connector.Error as error:
            print("error al ingresar datos {}".format(error))
