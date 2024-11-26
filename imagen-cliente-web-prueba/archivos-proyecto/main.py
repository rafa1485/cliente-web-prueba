import numpy as np
from flask import Flask, request, redirect, url_for, render_template, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ingredientes import conectar, tabla_existe, crear_tabla, inicializar_tabla_ingredientes, agregar_ingrediente, obtener_ingrediente, obtener_info_ingrediente, modificar_ingrediente, borrar_ingrediente

from excel_output import crear_tabla_calculos


## Defino los contenidos de referencia de los distintos aminoacidos
requerimiento_aminoacidos_esenciales = {'histidina':18, 'isoleucina':25, 'leucina':55, 'lisina':51, 'metionina':25, 'fenilalanina':47, 'treonina':27, 'triptofano':7, 'valina':32}
aminoacidos = [x for x in requerimiento_aminoacidos_esenciales.keys()]


conectar()

existencia_tabla_ingredientes = tabla_existe('ingredientes')
if not existencia_tabla_ingredientes:
    crear_tabla()
    inicializar_tabla_ingredientes()

# Configuración inicial
app = Flask(__name__)
app.secret_key = b'elsecretodetusojos'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige a /login si no está autenticado

# Lista de usuarios (usuario, clave) en formato (nombre, contraseña_hash)
usuarios = [
    ("admin", generate_password_hash("admin")),
    ("edgar", generate_password_hash("ceape2024")),
    ("user", generate_password_hash("test2024")),
]

# Clase de usuario que extiende UserMixin para integración con Flask-Login
class Usuario(UserMixin):
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

# Cargar usuario por ID (Flask-Login necesita esta función)
@login_manager.user_loader
def load_user(user_id):
    for i, (nombre, _) in enumerate(usuarios):
        if str(i) == user_id:
            return Usuario(i, nombre)
    return None

# Ruta protegida que solo puede accederse si el usuario está autenticado
@app.route("/")
@login_required
def home():
    #flash("Bienvenido, se ha logeado correctamente", "message")
    return f"<h1>Bienvenido, {current_user.nombre}!</h1><a href='/logout'>Cerrar sesión</a>"

# Ruta para iniciar sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Validar credenciales contra la lista de usuarios
        for i, (nombre, clave_hash) in enumerate(usuarios):
            if nombre == username and check_password_hash(clave_hash, password):
                user = Usuario(i, nombre)
                login_user(user)
                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for('seleccion_app'))

        flash("Usuario o contraseña incorrectos", "danger")

    return render_template("login.html")

# Ruta para cerrar sesión
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for("login"))


# Seleccionar app
@app.route('/seleccion_app')
@login_required
def seleccion_app():
    return render_template('select_apps.html')


##*****************************************************************************************
# Ruta principal que muestra todos los ingredientes
@app.route('/abm_ingredientes')
@login_required
def abm_ingredientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ingredientes")
    ingredientes = cursor.fetchall()
    conexion.close()
    return render_template('ingredientes.html', ingredientes=ingredientes)

# Ruta para agregar un nuevo ingrediente
@app.route('/abm_ingredientes/agregar', methods=['POST'])
@login_required
def agregar():
    nombre = request.form['nombre']
    densidad = request.form['densidad']
    precio = request.form['precio']
    color = request.form['color']
    digestibilidad_proteica = request.form['digestibilidad_proteica']
    contenido_proteico = request.form['contenido_proteico']
    contenido_carbohidratos = request.form['contenido_carbohidratos']
    contenido_aceites = request.form['contenido_aceites']
    histidina = request.form['histidina']
    isoleucina = request.form['isoleucina']
    leucina = request.form['leucina']
    lisina = request.form['lisina']
    metionina = request.form['metionina']
    fenilalanina = request.form['fenilalanina']
    treonina = request.form['treonina']
    triptofano = request.form['triptofano']
    valina = request.form['valina']
    
    agregar_ingrediente(nombre, float(densidad), float(precio), color, float(digestibilidad_proteica), float(contenido_proteico),
                                     float(contenido_carbohidratos), float(contenido_aceites), float(histidina),
                                     float(isoleucina), float(leucina), float(lisina), float(metionina),
                                     float(fenilalanina), float(treonina), float(triptofano), float(valina))
    return redirect(url_for('abm_ingredientes'))

# Ruta para eliminar un ingrediente
@app.route('/abm_ingredientes/eliminar/<int:id>')
@login_required
def eliminar(id):
    borrar_ingrediente(id)
    return redirect(url_for('abm_ingredientes'))

# Ruta para editar un ingrediente
@app.route('/abm_ingredientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if request.method == 'POST':
        densidad = request.form['densidad']
        precio = request.form['precio']
        color = request.form['color']
        digestibilidad_proteica = request.form['digestibilidad_proteica']
        contenido_proteico = request.form['contenido_proteico']
        contenido_carbohidratos = request.form['contenido_carbohidratos']
        contenido_aceites = request.form['contenido_aceites']
        histidina = request.form['histidina']
        isoleucina = request.form['isoleucina']
        leucina = request.form['leucina']
        lisina = request.form['lisina']
        metionina = request.form['metionina']
        fenilalanina = request.form['fenilalanina']
        treonina = request.form['treonina']
        triptofano = request.form['triptofano']
        valina = request.form['valina']

        modificar_ingrediente(id, float(densidad), float(precio), color, float(digestibilidad_proteica), float(contenido_proteico),
                                           float(contenido_carbohidratos), float(contenido_aceites), float(histidina),
                                           float(isoleucina), float(leucina), float(lisina), float(metionina),
                                           float(fenilalanina), float(treonina), float(triptofano), float(valina))
        return redirect(url_for('abm_ingredientes'))
    else:
        ingrediente = obtener_ingrediente(id)
        return render_template('ingredientes.html', editar=True, ingrediente=ingrediente)


##*************************************************************************************************************

# Aplicacion de mezcla óptima

# Ruta para seleccionar ingredientes y calcular los valores
@app.route('/mezcla_manual', methods=['GET', 'POST'])
@login_required
def mezcla_manual():
    #ingredientes = []
    score_proteico = 0
    costo_por_kg = 0
    porcentaje_total = 0

    # Muestra todos los ingredientes para seleccionar
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, nombre FROM ingredientes")
    ingredientes = cursor.fetchall()

    cursor.execute("SELECT id, digestibilidad_proteica FROM ingredientes")
    digestibilidades = cursor.fetchall()
    
    conexion.close()

    #dict_id_ingredientes = dict(ingredientes)

    # Creo un diccionario de las digestibilidades indexado por el id
    dict_id_digestibilidades = dict(digestibilidades)

    if request.method == 'POST':

        # Cargar datos de la selección y porcentajes
        #id_ingredientes_seleccionados = request.form.getlist('ingrediente')
        digestibilidades_form = request.form.getlist('digestibilidad')

        ##TODO Esto debería borrarse, porque no tiene sentido que la digestibilidad se modifique durante la mezcla
        # obtengo las digestibilidades y actualizo sus valores por si el usuario cambio alguno de los mismos
        digestibilidades = [(id,float(digestibilidades_form[i])) for i,id in enumerate(dict_id_digestibilidades.keys())]
        # creo un diccionario que devuelve la digestibilidad para cada ingrediente dado por su id
        dict_id_digestibilidades = dict(digestibilidades)

        porcentajes = request.form.getlist('porcentaje')
        print('porcentajes')
        print(porcentajes)

        # obtengo los porcentajes en mezcla y creo un diccionario que vincula cada ingrediente
        # dado por su 'id' con el porcentaje correspondiente
        porcentajes_num = [int(x) if x != '' else 0 for x in porcentajes]
        lista_ingredientes = [id for id,_ in ingredientes]
        dict_id_porcentajes = dict(zip(lista_ingredientes,porcentajes_num))
        print(dict_id_porcentajes)

        id_ingredientes_seleccionados = []
        for id in lista_ingredientes:
            if dict_id_porcentajes[id] > 0:
                id_ingredientes_seleccionados.append(id)
        
        if len(id_ingredientes_seleccionados) != 0:
        

            print('ingredientes seleccionados')
            print(id_ingredientes_seleccionados)

            # Calculamos el porcentaje total de los ingredientes.
            # En caso que los ingredientes sumen un valor distinto de 100% se debe imprimir un alerta.
            porcentaje_total = sum(porcentajes_num)
            if porcentaje_total < 100:
                flash("Porcentaje total menor a 100%: Aumentar los porcentajes de los ingredientes", "info")
            elif porcentaje_total > 100:
                flash("Porcentaje total major a 100%: Disminuir los porcentajes de los ingredientes", "info")
            
            # icializo los diccionarios necesarios para hacer las cuentas
            dict_id_nombre = {}
            dict_id_cont_proteina = {}
            dict_id_digest_proteina = {}
            dict_id_precio = {}
            dict_id_amino = {}
            dict_id_carbohidr = {}
            dict_id_lipidos = {}


            for id_ingrediente_seleccionado in id_ingredientes_seleccionados:
                porcentaje_str = str(dict_id_porcentajes[id_ingrediente_seleccionado])
                ingrediente_info = obtener_info_ingrediente(id_ingrediente_seleccionado)
                
                if ingrediente_info:
                    print('porcentaje: '+ porcentaje_str)
                    print('ingrediente info: ')
                    print(ingrediente_info)
                    
                    nombre_ingre = ingrediente_info[1]

                    contenido_proteico = float(ingrediente_info[6])

                    digest_proteina = float(ingrediente_info[5])

                    precio = float(ingrediente_info[3])

                    densidad = float(ingrediente_info[2])

                    contenido_carbohidr = float(ingrediente_info[7])
                    
                    contenido_lipidos = float(ingrediente_info[8])

                    dict_id_nombre.update({id_ingrediente_seleccionado:nombre_ingre})

                    dict_id_precio.update({id_ingrediente_seleccionado:precio})

                    dict_id_cont_proteina.update({id_ingrediente_seleccionado:contenido_proteico})

                    dict_id_digest_proteina.update({id_ingrediente_seleccionado:digest_proteina})

                    dict_id_amino.update({id_ingrediente_seleccionado:list(ingrediente_info[9:18])})

                    dict_id_carbohidr.update({id_ingrediente_seleccionado:contenido_carbohidr})

                    dict_id_lipidos.update({id_ingrediente_seleccionado:contenido_lipidos})

                    #score_proteico += (contenido_proteico * float(porcentaje_str) / 100)
                    #costo_por_kg += (precio * float(porcentaje_str) / 100)
                else:
                    print('El ingrediente '+id_ingrediente_seleccionado+' no se encuentra en la base de datos.')
                    breakpoint()
            #print(dict_id_precio)
            #print(dict_id_cont_proteina)
            #print(contenido_carbohidr)
            #print(contenido_lipidos)
            #print(dict_id_amino)
            
            
            D_i = [] # Vector Digestibilidad de la proteína de cada ingrediente
            W_i = [] # Vector Porcentajes de Ingrediente
            Costo_i = [] # Vector Costo de ingredientes
            P_i = [] # Vector Composición Proteica de Ingredientes por gr de ingrediente
            AA_ij = [] # Matriz del j-esimo Amino Ácidos del ingrediente i
            

            for id in id_ingredientes_seleccionados:
                D_i.append([dict_id_digest_proteina[id]])
                W_i.append([dict_id_porcentajes[id]])
                Costo_i.append([dict_id_precio[id]])
                P_i.append([dict_id_cont_proteina[id]])
                AA_ij.append(dict_id_amino[id])

            
            req_AA = [[requerimiento_aminoacidos_esenciales[j] for j in requerimiento_aminoacidos_esenciales.keys()]] # Requerimientos de amonoacidos esenciales
            
            D = np.array(D_i)
            W = np.array(W_i)/100
            C = np.array(Costo_i)
            P = np.array(P_i)/100
            AA = np.array(AA_ij)
            rAA = np.array(req_AA)
            

            #---------------------------------------------------------------------------------------
            # Calculo del costo de la materia prima
            costo_por_kg = np.dot(W.transpose(),C)[0,0]

            #----------------------------------------------------
            # Contenido proteico
            print(P)

            #----------------------------------------------------
            # Fracción de cada proteína presente en la mezcla
            WP = W*P
            print(WP)
            print('Proteína total en un gr de mezcla')
            P_mezcla = WP.sum()
            print(P_mezcla)

            #---------------------------------------------------------------------------------------
            # Calculo de la digestigilidad promedio de la mezcla
            Dm = (np.dot(WP.transpose(),D)/P_mezcla)[0,0]
            print('Digestibilidad promedio')
            print(Dm)

            #--------------------------------------------------------------------------------------
            # mg del j-esimo Aminoacido esencial para cada gramo del ingrediente i
            print('mg de Aminoácido por cada gr de ingredietne i')
            print(AA)
            
            #--------------------------------------------------------------------------------------
            # mg del j-esimo Aminoacido esencial en cada gramo de mezcla
            print('mgr de Aminoacidos por gr de mezcla')
            AA_mezcla = np.dot(WP.transpose(),AA)
            print(AA_mezcla)

            #--------------------------------------------------------------------------------------
            # calculo de los ASS_j
            AAS = np.divide((AA_mezcla / P_mezcla) , rAA)
            print('Puntuación de Aminoácidos (AAS)')
            print(AAS)

            PDCAAS = AAS.min() * Dm

            wb = crear_tabla_calculos(nombres=dict_id_nombre, fraccion_proteina=dict_id_cont_proteina, digestibilidad_proteina=dict_id_digest_proteina, contenido_aminoacidos=dict_id_amino, requerimientos=req_AA, porcentajes_mezcla=W, aminoacidos_mezcla_gr_mezcla=AA_mezcla, fraccion_proteina_mezcla=P_mezcla ,puntaje_aminoacidos=AAS, digestibilidad=Dm, PDCAAS=PDCAAS)

            wb.save('./resultados_calculos_ejemplo.xlsx')

            return render_template('mezcla_manual.html', ingredientes=ingredientes, digestibilidades=dict_id_digestibilidades, porcentajes_num=dict_id_porcentajes,
                                aminoacidos=aminoacidos ,referencia_aminoacidos=requerimiento_aminoacidos_esenciales,
                                score_proteico=score_proteico, costo_por_kg=costo_por_kg, 
                                porcentaje_total=porcentaje_total)

    
    return render_template('mezcla_manual.html', ingredientes=ingredientes, digestibilidades=dict_id_digestibilidades, porcentajes_num=False,
                            aminoacidos=aminoacidos ,referencia_aminoacidos=requerimiento_aminoacidos_esenciales,
                            score_proteico=score_proteico, costo_por_kg=costo_por_kg, 
                            porcentaje_total=porcentaje_total)

# Descarga de resultado y cálculos de mezcla manual
@app.route('/descargar-mezcla-manual')
@login_required
def descargar_resultados_manual():
    PATH='resultados_calculos_ejemplo.xlsx'
    try:
        return send_file(PATH, as_attachment=True)
    except Exception as e:
        return f"Error al descargar el archivo: {str(e)}", 500

# Aplicacion de mezcla óptima
@app.route('/mezcla_optima')
@login_required
def mezcla_optima():
    return f'''
               <h1>Bienvenido a la prueba de Mezcla Óptima, {current_user.nombre}!</h1>
               <a href='/logout'>Cerrar sesión</a>
            '''




# Punto de entrada de la aplicación
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
