import sqlite3

# Conexión y creación de la base de datos
def conectar(db_dir_path):
    return sqlite3.connect(db_dir_path+'ingredientes.db')

# Creación de la tabla de ingredientes
def crear_tabla(db_dir_path):
    conexion = conectar(db_dir_path)
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
def tabla_existe(nombre_tabla, db_dir_path):
    '''
        Esta función comprueba que exista la tabla "nombre_tabla" en la base de datos
    '''
    conexion = conectar(db_dir_path)
    cursor = conexion.cursor()
    cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', (nombre_tabla,))
    existe = cursor.fetchone() is not None
    conexion.close()
    return existe

# Inicialización de datos de prueba
def inicializar_tabla_ingredientes(db_dir_path):

    # Conectar a la base de datos (o crearla si no existe)
    conexion = conectar(db_dir_path)
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
    # Valores revisados:
    # - Composicion aminoacidos
    # - Proteinas
    # - carbohidratos
    # - aceites



    ingredientes = [
        ('Soja texturizada',         0.25, 3.5, 'Beige',    0.95, 50, 30, 4.0,     24.8, 45.2,  80.4,  59.9,  12.2, 56.0,  38.5,  12.0, 45.2), #listo
        ('Harina integral de trigo', 0.6,  1,   'Marrón',    0.8, 13, 75, 1.0,     23.5, 38.9,  68.3,  22.1,  16.1, 49.8,  26.7,  12.9, 43.4), #listo FDC ID: 169721
        ('Harina de garbanzo',       0.7,  10,   'Amarillo', 0.85, 22, 58, 6.0,     27.7, 43.1,  71.6,  67.4,  13.2, 53.9,  37.5,  9.80, 42.3), #listo FDC ID: 173756
        ('Harina de Arroz',          0.5,  5,   'Blanco',   0.80, 4,  80, 1.4,     25.0, 41.0,  82.0,  35.8,  24.2, 53.3,  35.3,  12.1, 58.5), #listo FDC ID: 169714
        ('Harina de arvejas',        0.6,  2,   'Verde',    0.85, 22, 60, 2.0,     19.7, 36.00, 60.00, 58.50, 15.1, 36.90, 37.5,  6.80, 43.40) #listo
        ('Harina de avena',          0.6,  2,   'Beige',    0.85, 13, 66, 7.0,     22.1, 38.7,  72.4,  32.1,  18.1, 49.3,  29.4,  13.8, 46.8)  #listo FDC ID: 172678
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
def agregar_ingrediente(db_dir_path, nombre, densidad, precio, color, digestibilidad_proteica, contenido_proteico, contenido_carbohidratos, contenido_aceites,
                        histidina, isoleucina, leucina, lisina, metionina, fenilalanina, treonina, triptofano, valina):
    conexion = conectar(db_dir_path)
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
def obtener_ingrediente(id, db_dir_path):
    conexion = conectar(db_dir_path)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ingredientes WHERE id = ?", (id,))
    ingrediente = cursor.fetchone()
    conexion.close()
    if ingrediente == None:
        breakpoint()
    return ingrediente

# Búsqueda y consulta de la informacion de los ingredientes
def obtener_info_ingrediente(id, db_dir_path):
    conexion = conectar(db_dir_path)
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
def modificar_ingrediente(db_dir_path, id, densidad=None, precio=None, color=None, digestibilidad_proteica=None, contenido_proteico=None, contenido_carbohidratos=None,
                          contenido_aceites=None, histidina=None, isoleucina=None, leucina=None, lisina=None,
                          metionina=None, fenilalanina=None, treonina=None, triptofano=None, valina=None):
    conexion = conectar(db_dir_path)
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
def borrar_ingrediente(id, db_dir_path):
    conexion = conectar(db_dir_path)
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
