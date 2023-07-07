import sqlite3 #Importamos el módulo sqlite3 para poder trabajar con bases de datos SQLite.
from sqlite3 import Error #importamos el submódulo Error para manejar excepciones específicas de SQLite.

class QueriesSQLite:
    def create_connection(path): #crear conexion a la base de datos
        connection = None
        try:
            connection = sqlite3.connect(path)# Establece la conexión a la base de datos SQLite usando la ruta proporcionada
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")# Si ocurre un error al establecer la conexión, se muestra el mensaje de error

        return connection

#La clase "QueriesSQLite" contiene métodos para interactuar con la base de datos SQLite.
#El método "create_connection" crea una conexión a la base de datos especificada por la ruta "path".
#Retorna el objeto de conexión "connection". Si ocurre un error, se muestra un mensaje de error.


    def execute_query(connection, query, data_tuple): #Ejecuta una consulta en la base de datos a través de la conexión.
        cursor = connection.cursor() ## Creamos un cursor para ejecutar la consulta
        try:
            cursor.execute(query, data_tuple) # Ejecutamos la consulta con los datos proporcionados
            connection.commit() # Confirmamos los cambios en la base de datos
            print("Query executed successfully")
            return cursor.lastrowid # Retornamos el ID de la última fila afectada por la consulta
        except Error as e:
            print(f"The error '{e}' occurred")


    def execute_read_query(connection, query, data_tuple=()):  #Ejecuta una consulta de lectura en la base de datos a través de la conexión.
        cursor = connection.cursor() # Creamos un cursor para ejecutar la consulta
        result = None
        try:
            cursor.execute(query, data_tuple)# Ejecutamos la consulta con los datos proporcionados
            result = cursor.fetchall()# Obtenemos todas las filas resultantes de la consulta
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    # 
    def create_tables(): #Crea una nueva tabla en la base de datos.
        connection = QueriesSQLite.create_connection("pdvDB.sqlite") # Creamos una conexión a la base de datos utilizando el método "create_connection" de la clase "QueriesSQLite"

        tabla_productos = """
        CREATE TABLE IF NOT EXISTS productos(
         codigo TEXT PRIMARY KEY, 
         nombre TEXT NOT NULL, 
         precio REAL NOT NULL, 
         cantidad INTEGER NOT NULL
        );
        """
        # Definimos la estructura de la tabla "productos" con sus respectivos campos

        tabla_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios(
         username TEXT PRIMARY KEY, 
         nombre TEXT NOT NULL, 
         password TEXT NOT NULL,
         tipo TEXT NOT NULL
        );
        """

        tabla_ventas = """
        CREATE TABLE IF NOT EXISTS ventas(
         id INTEGER PRIMARY KEY, 
         total REAL NOT NULL, 
         fecha TIMESTAMP,
         username TEXT  NOT NULL, 
         FOREIGN KEY(username) REFERENCES usuarios(username)
        );
        """

        tabla_ventas_detalle = """
        CREATE TABLE IF NOT EXISTS ventas_detalle(
         id INTEGER PRIMARY KEY, 
         id_venta TEXT NOT NULL, 
         precio REAL NOT NULL,
         producto TEXT NOT NULL,
         cantidad INTEGER NOT NULL,
         FOREIGN KEY(id_venta) REFERENCES ventas(id),
         FOREIGN KEY(producto) REFERENCES productos(codigo)
        );
        """

        QueriesSQLite.execute_query(connection, tabla_productos, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_usuarios, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_ventas, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_ventas_detalle, tuple()) 


        #Se ejecutan las consultas para crear las tablas utilizando el método "execute_query" de la clase "QueriesSQLite" 
        #y pasando la conexión establecida. Cada consulta crea una tabla si no existe en la base de datos.

if __name__=="__main__":
    from datetime import datetime, timedelta
    connection = QueriesSQLite.create_connection("pdvDB.sqlite")

    #Si el script es ejecutado directamente (es decir, no es importado como módulo), se importa el módulo datetime 
    #y se crea una conexión a la base de datos utilizando el método "create_connection" de la clase "QueriesSQLite".
    #La conexión se establece con el archivo de base de datos "pdvDB.sqlite".


    fecha1= datetime.today()-timedelta(days=5)
    neuva_data=(fecha1, 4)
    actualizar = """
    UPDATE
      ventas
    SET
      fecha=?
    WHERE
      id = ?
    """

    #Se crea una variable "fecha1" que almacena la fecha actual menos 5 días utilizando el módulo datetime y la función timedelta.
    #Luego se crea una tupla "nueva_data" que contiene los valores de "fecha1" y el número 4.
    #Por último, se define la consulta SQL "actualizar" que actualiza la columna "fecha" en la tabla "ventas" para el registro con un ID de 4.

    QueriesSQLite.execute_query(connection, actualizar, neuva_data)

    select_ventas = "SELECT * from ventas"
    ventas = QueriesSQLite.execute_read_query(connection, select_ventas)
    if ventas:
        for venta in ventas:
            print("type:", type(venta), "venta:",venta)

    #Se ejecuta la consulta "actualizar" utilizando el método "execute_query" de la clase "QueriesSQLite" y pasando la conexión y los datos de "nueva_data".
    #Luego, se define la consulta "select_ventas" para seleccionar todos los registros de la tabla "ventas".
    #Se utiliza el método "execute_read_query" de la clase "QueriesSQLite" para ejecutar la consulta y obtener los resultados en la variable "ventas".
    #Si hay registros en "ventas", se itera sobre ellos y se imprime el tipo y el contenido de cada registro.


    select_ventas_detalle = "SELECT * from ventas_detalle"
    ventas_detalle = QueriesSQLite.execute_read_query(connection, select_ventas_detalle)
    if ventas_detalle:
        for venta in ventas_detalle:
            print("type:", type(venta), "venta:",venta)

    #Se define la consulta "select_ventas_detalle" para seleccionar todos los registros de la tabla "ventas_detalle".
    #Se utiliza el método "execute_read_query" de la clase "QueriesSQLite" para ejecutar la consulta y obtener los resultados en la variable "ventas_detalle".
    #Si hay registros en "ventas_detalle", se itera sobre ellos y se imprime el tipo y el contenido de cada registro.

    # crear_producto = """
    # INSERT INTO
    #   productos (codigo, nombre, precio, cantidad)
    # VALUES
    #     ('111', 'leche 1l', 20.0, 20),
    #     ('222', 'cereal 500g', 50.5, 15), 
    #     ('333', 'yogurt 1L', 25.0, 10),
    #     ('444', 'helado 2L', 80.0, 20),
    #     ('555', 'alimento para perro 20kg', 750.0, 5),
    #     ('666', 'shampoo', 100.0, 25),
    #     ('777', 'papel higiénico 4 rollos', 35.5, 30),
    #     ('888', 'jabón para trastes', 65.0, 5)
    # """
    # QueriesSQLite.execute_query(connection, crear_producto, tuple()) 

    # select_products = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)


    # usuario_tuple=('test', 'Persona 1', '123', 'admin')
    # crear_usuario = """
    # INSERT INTO
    #   usuarios (username, nombre, password, tipo)
    # VALUES
    #     (?,?,?,?);
    # """
    # QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple) 


    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:",usuario)

    # neuva_data=('Persona 55', '123', 'admin', 'persona1')
    # actualizar = """
    # UPDATE
    #   usuarios
    # SET
    #   nombre=?, password=?, tipo = ?
    # WHERE
    #   username = ?
    # """
    # QueriesSQLite.execute_query(connection, actualizar, neuva_data)

    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:",usuario)



    # select_products = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)

    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:",usuario)

    # producto_a_borrar=('888',)
    # borrar = """DELETE from productos where codigo = ?"""
    # QueriesSQLite.execute_query(connection, borrar, producto_a_borrar)

    # select_products = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)
