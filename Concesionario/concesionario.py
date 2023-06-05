#Proyecto H

#A un concesionario de coches llegan clientes para comprar automóviles. De cada coche
#interesa saber la matrícula, modelo, marca y color. Un cliente puede comprar varios
#coches en el concesionario. Cuando un cliente compra un coche, se le hace una ficha en
#el concesionario con la siguiente información: dni, nombre, apellidos, dirección y teléfono.
#Los coches que el concesionario vende pueden ser nuevos o usados (de segunda mano).
#De los coches nuevos interesa saber el número de unidades que hay en el concesionario.
#De los coches viejos interesa el número de kilómetros que lleva recorridos.
#El concesionario también dispone de un taller en el que los mecánicos reparan los coches
#que llevan los clientes. Un mecánico repara varios coches a lo largo del día, y un coche
#puede ser reparado por varios mecánicos. Los mecánicos tienen un dni, nombre,
#apellidos, fecha de contratación y salario. Se desea guardar también la fecha en la que se
#repara cada vehículo y el número de horas que se tardado en arreglar cada automóvil.


import psycopg2
import os

def borrar_consola():
    os.system("cls")

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="concesionario",
    user="postgres",
    password="password"
)

# Crear tablas si no existen
def crear_tablas():
    try:
        cursor = conn.cursor()
        # Tabla coches
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coches (
                matricula VARCHAR(10) PRIMARY KEY,
                modelo VARCHAR(50),
                marca VARCHAR(50),
                color VARCHAR(20),
                tipo VARCHAR(10),
                unidades_nuevas INTEGER,
                kilometros INTEGER
            )
        """)
        # Tabla clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                dni VARCHAR(10) PRIMARY KEY,
                nombre VARCHAR(50),
                apellidos VARCHAR(50),
                direccion VARCHAR(100),
                telefono VARCHAR(20)
            )
        """)
        # Tabla fichas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fichas (
                dni_cliente VARCHAR(10) REFERENCES clientes(dni),
                matricula_coche VARCHAR(10) REFERENCES coches(matricula),
                fecha_compra DATE,
                PRIMARY KEY (dni_cliente, matricula_coche)
            )
        """)
        # Tabla mecanicos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mecanicos (
                dni VARCHAR(10) PRIMARY KEY,
                nombre VARCHAR(50),
                apellidos VARCHAR(50),
                fecha_contratacion DATE,
                salario DECIMAL(8, 2)
            )
        """)
        # Tabla reparaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reparaciones (
                dni_mecanico VARCHAR(10) REFERENCES mecanicos(dni),
                matricula_coche VARCHAR(10) REFERENCES coches(matricula),
                fecha_reparacion DATE,
                horas_trabajadas DECIMAL(5, 2),
                PRIMARY KEY (dni_mecanico, matricula_coche, fecha_reparacion)
            )
        """)
        conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Función para insertar un coche en la base de datos
def insertar_coche(matricula, modelo, marca, color, tipo, unidades_nuevas=None, kilometros=None):
    borrar_consola()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO coches (matricula, modelo, marca, color, tipo, unidades_nuevas, kilometros)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (matricula, modelo, marca, color, tipo, unidades_nuevas, kilometros))
        print("Coche insertado correctamente.")
        input("Presione Enter para continuar...")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Función para insertar un cliente en la base de datos
def insertar_cliente(dni, nombre, apellidos, direccion, telefono):
    borrar_consola()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (dni, nombre, apellidos, direccion, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (dni, nombre, apellidos, direccion, telefono))
        print("Cliente insertado correctamente.")
        input("Presione Enter para continuar...")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Función para crear una ficha de compra en la base de datos
def crear_ficha_compra(dni_cliente, matricula_coche, fecha_compra):
    borrar_consola()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fichas (dni_cliente, matricula_coche, fecha_compra)
            VALUES (%s, %s, %s)
        """, (dni_cliente, matricula_coche, fecha_compra))
        print("Ficha de compra creada correctamente.")
        input("Presione Enter para continuar...")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Función para insertar un mecánico en la base de datos
def insertar_mecanico(dni, nombre, apellidos, fecha_contratacion, salario):
    borrar_consola()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mecanicos (dni, nombre, apellidos, fecha_contratacion, salario)
            VALUES (%s, %s, %s, %s, %s)
        """, (dni, nombre, apellidos, fecha_contratacion, salario))
        print("Mecánico insertado correctamente.")
        input("Presione Enter para continuar...")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Función para registrar una reparación en la base de datos
def registrar_reparacion(dni_mecanico, matricula_coche, fecha_reparacion, horas_trabajadas):
    borrar_consola()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reparaciones (dni_mecanico, matricula_coche, fecha_reparacion, horas_trabajadas)
            VALUES (%s, %s, %s, %s)
        """, (dni_mecanico, matricula_coche, fecha_reparacion, horas_trabajadas))
        print("Reparación registrada correctamente.")
        input("Presione Enter para continuar...")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        input("Presione Enter para continuar...")
# Función para mostrar los datos de la base de datos
def mostrar_datos():
    borrar_consola()
    try:
        cursor = conn.cursor()
        # Mostrar coches
        print("Coches:")
        cursor.execute("SELECT * FROM coches")
        coches = cursor.fetchall()
        for coche in coches:
            print(coche)
        print()
        # Mostrar clientes
        print("Clientes:")
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        for cliente in clientes:
            print(cliente)
        print()
        # Mostrar fichas de compra
        print("Fichas de compra:")
        cursor.execute("SELECT * FROM fichas")
        fichas = cursor.fetchall()
        for ficha in fichas:
            print(ficha)
        print()
        # Mostrar mecánicos
        print("Mecánicos:")
        cursor.execute("SELECT * FROM mecanicos")
        mecanicos = cursor.fetchall()
        for mecanico in mecanicos:
            print(mecanico)
        print()
        # Mostrar reparaciones
        print("Reparaciones:")
        cursor.execute("SELECT * FROM reparaciones")
        reparaciones = cursor.fetchall()
        for reparacion in reparaciones:
            print(reparacion)
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    input("Presione Enter para continuar...")
    
# Función para borrar un coche de la base de datos
def borrar_coche(matricula):
    borrar_consola()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM coches WHERE matricula = %s", (matricula,))
        print("Coche borrado correctamente.")
        input("Presione Enter para continuar...")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Función para borrar un cliente de la base de datos
def borrar_cliente(dni):
    borrar_consola()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE dni = %s", (dni,))
        print("Cliente borrado correctamente.")
        input("Presione Enter para continuar...")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Función para borrar un mecánico de la base de datos
def borrar_mecanico(dni):
    borrar_consola()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mecanicos WHERE dni = %s", (dni,))
        print("Mecánico borrado correctamente.")
        input("Presione Enter para continuar...")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Función para borrar todas las tablas de la base de datos
def borrar_todo():
    borrar_consola()
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS reparaciones")
        cursor.execute("DROP TABLE IF EXISTS fichas")
        cursor.execute("DROP TABLE IF EXISTS mecanicos")
        cursor.execute("DROP TABLE IF EXISTS coches")
        cursor.execute("DROP TABLE IF EXISTS clientes")
        print("Se han borrado todas las tablas.")
        input("Presione Enter para continuar...")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Función para guardar los cambios en la base de datos
def guardar_cambios():
    borrar_consola()
    conn.commit()
    print("Cambios guardados correctamente.")
    input("Presione Enter para continuar...")
# Menú principal
def menu_principal():
    
    while True:
        borrar_consola()
        print("----- CONCESIONARIO DE COCHES -----")
        print("1. Insertar coche")
        print("2. Insertar cliente")
        print("3. Crear ficha de compra")
        print("4. Insertar mecánico")
        print("5. Registrar reparación")
        print("6. Mostrar datos")
        print("7. Borrar coche")
        print("8. Borrar cliente")
        print("9. Borrar mecánico")
        print("10. Borrar todo (tablas)")
        print("11. Guardar cambios")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            borrar_consola()
            matricula = input("Matrícula del coche: ")
            modelo = input("Modelo del coche: ")
            marca = input("Marca del coche: ")
            color = input("Color del coche: ")
            tipo = input("Tipo del coche (Nuevo/Usado): ")
            if tipo == "Nuevo":
                unidades_nuevas = int(input("Número de unidades nuevas: "))
                insertar_coche(matricula, modelo, marca, color, tipo, unidades_nuevas=unidades_nuevas)
            elif tipo == "Usado":
                kilometros = int(input("Número de kilómetros recorridos: "))
                insertar_coche(matricula, modelo, marca, color, tipo, kilometros=kilometros)
            else:
                print("Tipo de coche no válido.")

        elif opcion == "2":
            borrar_consola()
            dni = input("DNI del cliente: ")
            nombre = input("Nombre del cliente: ")
            apellidos = input("Apellidos del cliente: ")
            direccion = input("Dirección del cliente: ")
            telefono = input("Teléfono del cliente: ")
            insertar_cliente(dni, nombre, apellidos, direccion, telefono)

        elif opcion == "3":
            borrar_consola()
            dni_cliente = input("DNI del cliente: ")
            matricula_coche = input("Matrícula del coche: ")
            fecha_compra = input("Fecha de compra (AAAA-MM-DD): ")
            crear_ficha_compra(dni_cliente, matricula_coche, fecha_compra)

        elif opcion == "4":
            borrar_consola()
            dni = input("DNI del mecánico: ")
            nombre = input("Nombre del mecánico: ")
            apellidos = input("Apellidos del mecánico: ")
            fecha_contratacion = input("Fecha de contratación (AAAA-MM-DD): ")
            salario = float(input("Salario del mecánico: "))
            insertar_mecanico(dni, nombre, apellidos, fecha_contratacion, salario)

        elif opcion == "5":
            borrar_consola()
            dni_mecanico = input("DNI del mecánico: ")
            matricula_coche = input("Matrícula del coche: ")
            fecha_reparacion = input("Fecha de reparación (AAAA-MM-DD): ")
            horas_trabajadas = float(input("Número de horas trabajadas: "))
            registrar_reparacion(dni_mecanico, matricula_coche, fecha_reparacion, horas_trabajadas)

        elif opcion == "6":
            mostrar_datos()

        elif opcion == "7":
            borrar_consola()
            matricula = input("Matrícula del coche a borrar: ")
            borrar_coche(matricula)

        elif opcion == "8":
            borrar_consola()
            dni = input("DNI del cliente a borrar: ")
            borrar_cliente(dni)

        elif opcion == "9":
            borrar_consola()
            dni = input("DNI del mecánico a borrar: ")
            borrar_mecanico(dni)

        elif opcion == "10":
            borrar_consola()
            confirmacion = input("¿Está seguro de borrar todas las tablas? (S/N): ")
            if confirmacion.upper() == "S":
                borrar_todo()

        elif opcion == "11":
            guardar_cambios()

        elif opcion == "0":
            conn.close()
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

# Crear tablas si no existen
crear_tablas()

# Ejecutar el menú principal
menu_principal()
