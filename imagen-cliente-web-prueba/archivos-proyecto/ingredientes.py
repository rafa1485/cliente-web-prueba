import sqlite3

# Conexión y creación de la base de datos
def conectar():
    return sqlite3.connect('./db/ingredientes.db')

# Creación de la tabla de ingredientes
def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        densidad REAL,
                        precio REAL,
                        color TEXT,
                        digestibilidad_proteica REAL,
                        contenido_proteico REAL,
                        contenido_carbohidratos REAL,
                        contenido_aceites REAL,
                        histidina REAL,
                        isoleucina REAL,
                        leucina REAL,
                        lisina REAL,
                        metionina REAL,
                        fenilalanina REAL,
                        treonina REAL,
                        triptofano REAL,
                        valina REAL
                    )''')
    conexion.commit()
    conexion.close()

# Verificamos que la tabla ingredientes exista
def tabla_existe(nombre_tabla):
    '''
        Esta función comprueba que exista la tabla "nombre_tabla" en la base de datos
    '''
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', (nombre_tabla,))
    existe = cursor.fetchone() is not None
    conexion.close()
    return existe

# Inicialización de datos de prueba
def inicializar_tabla_ingredientes():

    # Conectar a la base de datos (o crearla si no existe)
    conexion = conectar()
    cursor = conexion.cursor()

    # Crear la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            densidad REAL,
            precio REAL,
            color TEXT,
            digestibilidad_proteica REAL,
            contenido_proteico REAL,
            contenido_carbohidratos REAL,
            contenido_aceites REAL,
            histidina REAL,
            isoleucina REAL,
            leucina REAL,
            lisina REAL,
            metionina REAL,
            fenilalanina REAL,
            treonina REAL,
            triptofano REAL,
            valina REAL
        )
    ''')

    # Insertar los valores de cada ingrediente
    ingredientes = [
        ('Soja texturizada', 0.25, 3.5, 'Beige', 0.95, 50, 30, 1.2, 6.50, 23.00, 38.00, 39.00, 5.00, 25.00, 22.00, 6.00, 25.00),
        ('Harina de trigo', 0.6, 1, 'Blanco', 0.85, 11, 73, 1.5, 1.70, 4.80, 8.30, 2.90, 1.60, 6.70, 3.10, 0.90, 5.70),
        ('Harina integral de trigo', 0.6, 1,'Marrón', 0.8, 13, 67, 2.5, 2.50, 6.80, 12.00, 3.20, 1.80, 8.00, 4.00, 1.20, 6.00),
        ('Harina de garbanzo', 0.7, 2, 'Amarillo', 0.85, 22, 58, 6, 3.40, 8.20, 15.00, 17.00, 2.20, 10.40, 6.20, 1.50, 10.80),
        ('Harina de algarroba', 0.5, 5, 'Marrón', 0.80,4, 90, 0.6, 0.60, 1.90, 3.20, 3.50, 0.50, 1.80, 0.90, 0.30, 2.10),
        ('Fécula de mandioca', 0.5, 1, 'Blanco', 0.8,1, 88, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ('Harina de arvejas', 0.6, 2, 'Verde', 0.85,22, 60, 2.5, 4.20, 10.00, 16.00, 17.00, 2.50, 11.00, 7.80, 2.00, 10.00)
    ]

    cursor.executemany('''
        INSERT INTO ingredientes (nombre, densidad, precio, color, digestibilidad_proteica, contenido_proteico, contenido_carbohidratos, 
                                  contenido_aceites, histidina, isoleucina, leucina, lisina, metionina, fenilalanina, 
                                  treonina, triptofano, valina)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ingredientes)

    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()
    print("Tabla 'ingredientes' inicializada con éxito.")

# Alta de ingrediente
def agregar_ingrediente(nombre, densidad, precio, color, digestibilidad_proteica, contenido_proteico, contenido_carbohidratos, contenido_aceites,
                        histidina, isoleucina, leucina, lisina, metionina, fenilalanina, treonina, triptofano, valina):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''INSERT INTO ingredientes (nombre, densidad, precio, color, digestibilidad_proteica, contenido_proteico, contenido_carbohidratos, contenido_aceites, 
                      histidina, isoleucina, leucina, lisina, metionina, fenilalanina, treonina, triptofano, valina) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (nombre, densidad, precio, color, digestibilidad_proteica, contenido_proteico, contenido_carbohidratos, contenido_aceites,
                    histidina, isoleucina, leucina, lisina, metionina, fenilalanina, treonina, triptofano, valina))
    conexion.commit()
    conexion.close()

# Búsqueda y consulta de ingredientes
#TODO
# CORREGIR: Se esta pasando un numero para buscar el ingrediente, mientras que los ingredientes estan nombrados con texto
def obtener_ingrediente(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ingredientes WHERE id = ?", (id,))
    ingrediente = cursor.fetchone()
    conexion.close()
    if ingrediente == None:
        breakpoint()
    return ingrediente

# Búsqueda y consulta de la informacion de los ingredientes
def obtener_info_ingrediente(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ingredientes WHERE id = ?", (id,))
    ingrediente_info = cursor.fetchone()
    conexion.close()
    if ingrediente_info == None:
        breakpoint()
    return ingrediente_info

#TODO
# No me permite cambiar el nombre de los ingredientes, sería bueno agregarlo
# Modificación de un ingrediente
def modificar_ingrediente(id, densidad=None, precio=None, color=None, digestibilidad_proteica=None, contenido_proteico=None, contenido_carbohidratos=None,
                          contenido_aceites=None, histidina=None, isoleucina=None, leucina=None, lisina=None,
                          metionina=None, fenilalanina=None, treonina=None, triptofano=None, valina=None):
    conexion = conectar()
    cursor = conexion.cursor()
    valores = {
        "densidad": densidad, "precio": precio, "color": color, "digestibilidad_proteica":digestibilidad_proteica, "contenido_proteico": contenido_proteico,
        "contenido_carbohidratos": contenido_carbohidratos, "contenido_aceites": contenido_aceites,
        "histidina": histidina, "isoleucina": isoleucina, "leucina": leucina, "lisina": lisina,
        "metionina": metionina, "fenilalanina": fenilalanina, "treonina": treonina, "triptofano": triptofano,
        "valina": valina
    }
    # Filtrar solo los valores que no son None
    actualizaciones = ", ".join(f"{col} = ?" for col, val in valores.items() if val is not None)
    valores_actualizados = [val for val in valores.values() if val is not None]
    if actualizaciones:
        cursor.execute(f"UPDATE ingredientes SET {actualizaciones} WHERE id = ?", valores_actualizados + [id])
        conexion.commit()
    conexion.close()

# Borrar un ingrediente
def borrar_ingrediente(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM ingredientes WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()

# Ejemplo de uso
if __name__ == "__main__":
    # Crear la tabla al inicio
    crear_tabla()
    
    # Agregar un ingrediente
    agregar_ingrediente(
        nombre="Soja",
        densidad=0.68,
        precio=1.5,
        color="Amarillo",
        digestibilidad_proteica=1,
        contenido_proteico=36.49,
        contenido_carbohidratos=30.16,
        contenido_aceites=19.94,
        histidina=2.14,
        isoleucina=4.32,
        leucina=7.07,
        lisina=6.4,
        metionina=1.07,
        fenilalanina=4.63,
        treonina=3.01,
        triptofano=1.04,
        valina=4.46
    )

    # Consultar un ingrediente
    ingrediente = obtener_ingrediente("Soja")
    print("Ingrediente consultado:", ingrediente)
    
    # Modificar un ingrediente
    if ingrediente:
        modificar_ingrediente(ingrediente[0], precio=2.0, contenido_proteico=37.0)
        print("Ingrediente modificado:", obtener_ingrediente("Soja"))

    # Eliminar un ingrediente
    if ingrediente:
        borrar_ingrediente(ingrediente[0])
        print("Ingrediente eliminado:", obtener_ingrediente("Soja"))
