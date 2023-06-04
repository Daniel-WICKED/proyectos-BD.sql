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
#repara cada vehículo y el número de horas que se tardado en arreglar cada automóvil”.

import psycopg2
import os

def crear_tablas(cursor):
    create_table_coches_nuevos = """
    CREATE TABLE IF NOT EXISTS CochesNuevos (
        Matricula VARCHAR PRIMARY KEY,
        Modelo VARCHAR,
        Marca VARCHAR,
        Color VARCHAR,
        Unidades INTEGER
    )
    """

    create_table_coches_usados = """
    CREATE TABLE IF NOT EXISTS CochesUsados (
        Matricula VARCHAR PRIMARY KEY,
        Modelo VARCHAR,
        Marca VARCHAR,
        Color VARCHAR,
        Kilometros INTEGER
    )
    """

    create_table_clientes = """
    CREATE TABLE IF NOT EXISTS Clientes (
        DNI VARCHAR PRIMARY KEY,
        Nombre VARCHAR,
        Apellidos VARCHAR,
        Direccion VARCHAR,
        Telefono VARCHAR
    )
    """

    create_table_compras = """
    CREATE TABLE IF NOT EXISTS Compras (
        DNI_Cliente VARCHAR REFERENCES Clientes(DNI),
        Matricula_Coche VARCHAR,
        Fecha_Compra DATE,
        PRIMARY KEY (DNI_Cliente, Matricula_Coche)
    )
    """

    create_table_mecanicos = """
    CREATE TABLE IF NOT EXISTS Mecanicos (
        DNI VARCHAR PRIMARY KEY,
        Nombre VARCHAR,
        Apellidos VARCHAR,
        Fecha_Contratacion DATE,
        Salario DECIMAL
    )
    """

    create_table_reparaciones = """
    CREATE TABLE IF NOT EXISTS Reparaciones (
        Matricula_Coche VARCHAR REFERENCES CochesNuevos(Matricula) ON DELETE CASCADE,
        DNI_Mecanico VARCHAR REFERENCES Mecanicos(DNI) ON DELETE CASCADE,
        Fecha_Reparacion DATE,
        Horas_Trabajadas DECIMAL,
        PRIMARY KEY (Matricula_Coche, DNI_Mecanico)
    )
    """

    cursor.execute(create_table_coches_nuevos)
    cursor.execute(create_table_coches_usados)
    cursor.execute(create_table_clientes)
    cursor.execute(create_table_compras)
    cursor.execute(create_table_mecanicos)
    cursor.execute(create_table_reparaciones)


def conectar_bd():
    while True:
        try:
            host = input("Ingrese el nombre del host de la base de datos: ")
            database = input("Ingrese el nombre de la base de datos: ")
            user = input("Ingrese el nombre de usuario de la base de datos: ")
            password = input("Ingrese la contraseña de la base de datos: ")

            conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            print("Conexión exitosa a la base de datos.")
            crear_tablas(conn.cursor())
            input("Presione Enter para continuar...")   
            return conn
        
        except psycopg2.Error as e:
            print("Error al conectar a la base de datos:", e)
            opcion = input("¿Desea volver a ingresar los parámetros de conexión? (s/n): ")
            if opcion.lower() != "s":
                return None


def borrar_consola():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")


def insertar_coche_nuevo(cursor):
    borrar_consola()
    matricula = input("Ingrese la matrícula del coche: ")
    modelo = input("Ingrese el modelo del coche: ")
    marca = input("Ingrese la marca del coche: ")
    color = input("Ingrese el color del coche: ")
    unidades = int(input("Ingrese el número de unidades disponibles: "))
    cursor.execute("INSERT INTO Coches (matricula, modelo, marca, color, tipo, unidades) VALUES (%s, %s, %s, %s, 'nuevo', %s)",
                   (matricula, modelo, marca, color, unidades))


def insertar_coche_usado(cursor):
    borrar_consola()
    matricula = input("Ingrese la matrícula del coche: ")
    modelo = input("Ingrese el modelo del coche: ")
    marca = input("Ingrese la marca del coche: ")
    color = input("Ingrese el color del coche: ")
    kilometros = float(input("Ingrese el número de kilómetros recorridos: "))
    cursor.execute("INSERT INTO Coches (matricula, modelo, marca, color, tipo, kilometros) VALUES (%s, %s, %s, %s, 'usado', %s)",
                   (matricula, modelo, marca, color, kilometros))


def insertar_cliente(cursor):
    borrar_consola()
    dni = input("Ingrese el DNI del cliente: ")
    nombre = input("Ingrese el nombre del cliente: ")
    apellidos = input("Ingrese los apellidos del cliente: ")
    direccion = input("Ingrese la dirección del cliente: ")
    telefono = input("Ingrese el teléfono del cliente: ")
    cursor.execute("INSERT INTO Clientes (dni, nombre, apellidos, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
                   (dni, nombre, apellidos, direccion, telefono))


def realizar_compra(cursor):
    borrar_consola()
    dni_cliente = input("Ingrese el DNI del cliente: ")
    matricula_coche = input("Ingrese la matrícula del coche: ")
    fecha_compra = input("Ingrese la fecha de compra (YYYY-MM-DD): ")
    cursor.execute(
        "INSERT INTO Compras (dni_cliente, matricula_coche, fecha_compra) VALUES (%s, %s, %s)",
        (dni_cliente, matricula_coche, fecha_compra))


def insertar_mecanico(cursor):
    borrar_consola()
    dni = input("Ingrese el DNI del mecánico: ")
    nombre = input("Ingrese el nombre del mecánico: ")
    apellidos = input("Ingrese los apellidos del mecánico: ")
    fecha_contratacion = input("Ingrese la fecha de contratación del mecánico (YYYY-MM-DD): ")
    salario = float(input("Ingrese el salario del mecánico: "))
    cursor.execute("INSERT INTO Mecanicos (dni, nombre, apellidos, fecha_contratacion, salario) VALUES (%s, %s, %s, %s, %s)",
                   (dni, nombre, apellidos, fecha_contratacion, salario))


def reparar_coche(cursor):
    borrar_consola()
    matricula_coche = input("Ingrese la matrícula del coche a reparar: ")
    dni_mecanico = input("Ingrese el DNI del mecánico encargado de la reparación: ")
    fecha_reparacion = input("Ingrese la fecha de reparación (YYYY-MM-DD): ")
    horas_trabajadas = float(input("Ingrese el número de horas trabajadas en la reparación: "))
    cursor.execute(
        "INSERT INTO Reparaciones (matricula_coche, dni_mecanico, fecha_reparacion, horas_trabajadas) VALUES (%s, %s, %s, %s)",
        (matricula_coche, dni_mecanico, fecha_reparacion, horas_trabajadas))


def mostrar_datos(cursor):
    while True:
        borrar_consola()
        print("\n----- DATOS -----")
        print("1. Mostrar coches nuevos")
        print("2. Mostrar coches usados")
        print("3. Mostrar clientes")
        print("4. Mostrar compras")
        print("5. Mostrar mecánicos")
        print("6. Mostrar reparaciones")
        print("7. Volver al menú principal")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            cursor.execute("SELECT * FROM Coches WHERE tipo = 'nuevo'")
            coches_nuevos = cursor.fetchall()
            if coches_nuevos:
                print("Coches nuevos:")
                for coche in coches_nuevos:
                    print(f"Matrícula: {coche[0]}, Modelo: {coche[1]}, Marca: {coche[2]}, Color: {coche[3]}, Unidades: {coche[6]}")
            else:
                print("No hay coches nuevos registrados.")
        elif opcion == "2":
            cursor.execute("SELECT * FROM Coches WHERE tipo = 'usado'")
            coches_usados = cursor.fetchall()
            if coches_usados:
                print("Coches usados:")
                for coche in coches_usados:
                    print(f"Matrícula: {coche[0]}, Modelo: {coche[1]}, Marca: {coche[2]}, Color: {coche[3]}, Kilómetros: {coche[7]}")
            else:
                print("No hay coches usados registrados.")
        elif opcion == "3":
            cursor.execute("SELECT * FROM Clientes")
            clientes = cursor.fetchall()
            if clientes:
                print("Clientes:")
                for cliente in clientes:
                    print(
                        f"DNI: {cliente[0]}, Nombre: {cliente[1]}, Apellidos: {cliente[2]}, Dirección: {cliente[3]}, Teléfono: {cliente[4]}")
            else:
                print("No hay clientes registrados.")
        elif opcion == "4":
            cursor.execute("SELECT * FROM Compras")
            compras = cursor.fetchall()
            if compras:
                print("Compras:")
                for compra in compras:
                    print(f"DNI Cliente: {compra[0]}, Matrícula Coche: {compra[1]}, Fecha Compra: {compra[2]}")
            else:
                print("No hay compras registradas.")
        elif opcion == "5":
            cursor.execute("SELECT * FROM Mecanicos")
            mecanicos = cursor.fetchall()
            if mecanicos:
                print("Mecánicos:")
                for mecanico in mecanicos:
                    print(
                        f"DNI: {mecanico[0]}, Nombre: {mecanico[1]}, Apellidos: {mecanico[2]}, Fecha Contratación: {mecanico[3]}, Salario: {mecanico[4]}")
            else:
                print("No hay mecánicos registrados.")
        elif opcion == "6":
            cursor.execute("SELECT * FROM Reparaciones")
            reparaciones = cursor.fetchall()
            if reparaciones:
                print("Reparaciones:")
                for reparacion in reparaciones:
                    print(
                        f"Matrícula Coche: {reparacion[0]}, DNI Mecánico: {reparacion[1]}, Fecha Reparación: {reparacion[2]}, Horas Trabajadas: {reparacion[3]}")
            else:
                print("No hay reparaciones registradas.")
        elif opcion == "7":
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

        input("\nPresione Enter para continuar...")


def menu_principal():
    conn = conectar_bd()
    if not conn:
        return

    cursor = conn.cursor()

    while True:
        borrar_consola()
        print("----- MENÚ PRINCIPAL -----")
        print("1. Insertar coche nuevo")
        print("2. Insertar coche usado")
        print("3. Insertar cliente")
        print("4. Realizar compra")
        print("5. Insertar mecánico")
        print("6. Reparar coche")
        print("7. Mostrar datos")
        print("8. Salir")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            insertar_coche_nuevo(cursor)
            conn.commit()
            print("Coche nuevo insertado exitosamente.")
        elif opcion == "2":
            insertar_coche_usado(cursor)
            conn.commit()
            print("Coche usado insertado exitosamente.")
        elif opcion == "3":
            insertar_cliente(cursor)
            conn.commit()
            print("Cliente insertado exitosamente.")
        elif opcion == "4":
            realizar_compra(cursor)
            conn.commit()
            print("Compra realizada exitosamente.")
        elif opcion == "5":
            insertar_mecanico(cursor)
            conn.commit()
            print("Mecánico insertado exitosamente.")
        elif opcion == "6":
            reparar_coche(cursor)
            conn.commit()
            print("Coche reparado exitosamente.")
        elif opcion == "7":
            mostrar_datos(cursor)
        elif opcion == "8":
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

        input("\nPresione Enter para continuar...")

    cursor.close()
    conn.close()


menu_principal()
