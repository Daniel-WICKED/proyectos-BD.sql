#Proyecto I 
#La liga de fútbol profesional, presidida por Don Ángel María Villar, ha decidido informatizar
#sus instalaciones creando una base de datos para guardar la información de los partidos
#que se juegan en la liga.
#Se desea guardar en primer lugar los datos de los jugadores. De cada jugador se quiere
#guardar el nombre, fecha de nacimiento y posición en la que juega (portero, defensa,
#centrocampista…). Cada jugador tiene un código de jugador que lo identifica de manera
#única.
#De cada uno de los equipos de la liga es necesario registrar el nombre del equipo, nombre
#del estadio en el que juega, el aforo que tiene, el año de fundación del equipo y la ciudad
#de la que es el equipo. Cada equipo también tiene un código que lo identifica de manera
#única. Un jugador solo puede pertenecer a un único equipo.
#De cada partido que los equipos de la liga juegan hay que registrar la fecha en la que se
#juega el partido, los goles que ha metido el equipo de casa y los goles que ha metido el
#equipo de fuera. Cada partido tendrá un código numérico para identificar el partido.
#Por último se quiere almacenar, en la base de datos, los datos de los presidentes de los
#equipos de fútbol (dni, nombre, apellidos, fecha de nacimiento, equipo del que es
#presidente y año en el que fue elegido presidente). Un equipo de fútbol tan sólo puede
#tener un presidente, y una persona sólo puede ser presidente de un equipo de la liga.

import psycopg2
import os

os.system("cls")

def conectar():
    try:
        conn = psycopg2.connect(
            database="futbol",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        print("Conexión exitosa con la base de datos")
        return conn

    except psycopg2.Error as e:
        print("Error al conectar a la base de datos, revise los parámetros de conexión.", e)
        return None

def crear_tablas(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Jugadores (
                codigo SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                fecha_nacimiento DATE NOT NULL,
                posicion VARCHAR(20) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Equipos (
                codigo SERIAL PRIMARY KEY,
                nombre_equipo VARCHAR(100) NOT NULL,
                nombre_estadio VARCHAR(100) NOT NULL,
                aforo INTEGER NOT NULL,
                anio_fundacion INTEGER NOT NULL,
                ciudad VARCHAR(100) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Partidos (
                codigo SERIAL PRIMARY KEY,
                fecha_partido DATE NOT NULL,
                equipo_local_id INTEGER REFERENCES Equipos(codigo),
                equipo_visitante_id INTEGER REFERENCES Equipos(codigo),
                goles_local INTEGER NOT NULL,
                goles_visitante INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Presidentes (
                dni VARCHAR(20) PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                apellidos VARCHAR(50) NOT NULL,
                fecha_nacimiento DATE NOT NULL,
                equipo_id INTEGER REFERENCES Equipos(codigo),
                anio_eleccion INTEGER NOT NULL
            )
        """)
        cursor.connection.commit()
        print("Tablas comprobadas con éxito")

    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)
    input("Presione ENTER para continuar...")

def insertar_jugador(cursor):
    os.system("cls")
    try:
        print("=== Insertar Jugador ===")
        nombre = input("Nombre del jugador: ")
        fecha_nacimiento = input("Fecha de nacimiento del jugador (YYYY-MM-DD): ")
        posicion = input("Posición del jugador (portero/defensa/centrocampista/delantero): ")

        cursor.execute("""
            INSERT INTO Jugadores (nombre, fecha_nacimiento, posicion)
            VALUES (%s, %s, %s)
        """, (nombre, fecha_nacimiento, posicion))
        cursor.connection.commit()
        print("Jugador guardado correctamente.")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al insertar los datos:", e)

def insertar_equipo(cursor):
    os.system("cls")
    try:
        print("=== Insertar Equipo ===")
        nombre_equipo = input("Nombre del equipo: ")
        nombre_estadio = input("Nombre del estadio: ")
        aforo = int(input("Aforo del estadio: "))
        anio_fundacion = int(input("Año de fundación del equipo: "))
        ciudad = input("Ciudad del equipo: ")

        cursor.execute("""
            INSERT INTO Equipos (nombre_equipo, nombre_estadio, aforo, anio_fundacion, ciudad)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre_equipo, nombre_estadio, aforo, anio_fundacion, ciudad))
        cursor.connection.commit()
        print("Equipo guardado correctamente.")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al insertar los datos:", e)

def insertar_partido(cursor):
    os.system("cls")
    try:
        print("=== Insertar Partido ===")
        fecha_partido = input("Fecha del partido (YYYY-MM-DD): ")
        equipos = obtener_equipos(cursor)

        print("Equipos disponibles:")
        for equipo in equipos:
            print(f"{equipo[0]}. {equipo[1]}")

        equipo_local_id = int(input("Seleccione el equipo local: "))
        equipo_visitante_id = int(input("Seleccione el equipo visitante: "))
        goles_local = int(input("Goles del equipo local: "))
        goles_visitante = int(input("Goles del equipo visitante: "))

        cursor.execute("""
            INSERT INTO Partidos (fecha_partido, equipo_local_id, equipo_visitante_id, goles_local, goles_visitante)
            VALUES (%s, %s, %s, %s, %s)
        """, (fecha_partido, equipo_local_id, equipo_visitante_id, goles_local, goles_visitante))
        cursor.connection.commit()
        print("Partido guardado correctamente.")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al insertar los datos:", e)

def insertar_presidente(cursor):
    os.system("cls")
    try:
        print("=== Insertar Presidente ===")
        dni = input("DNI del presidente: ")
        nombre = input("Nombre del presidente: ")
        apellidos = input("Apellidos del presidente: ")
        fecha_nacimiento = input("Fecha de nacimiento del presidente (YYYY-MM-DD): ")
        equipos = obtener_equipos(cursor)

        print("Equipos disponibles:")
        for equipo in equipos:
            print(f"{equipo[0]}. {equipo[1]}")

        equipo_id = int(input("Seleccione el equipo: "))
        anio_eleccion = int(input("Año de elección del presidente: "))

        cursor.execute("""
            INSERT INTO Presidentes (dni, nombre, apellidos, fecha_nacimiento, equipo_id, anio_eleccion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (dni, nombre, apellidos, fecha_nacimiento, equipo_id, anio_eleccion))
        cursor.connection.commit()
        print("Presidente guardado correctamente.")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al insertar los datos:", e)

def obtener_equipos(cursor):
    cursor.execute("SELECT codigo, nombre_equipo FROM Equipos")
    return cursor.fetchall()

def listar_jugadores(cursor):
    os.system("cls")
    try:
        print("=== Listado de Jugadores ===")
        cursor.execute("SELECT * FROM Jugadores")
        jugadores = cursor.fetchall()

        if len(jugadores) > 0:
            for jugador in jugadores:
                print(f"ID: {jugador[0]}\tNombre: {jugador[1]}\tFecha de nacimiento:{jugador[2]}\tPosición: {jugador[3]}")
                print("-----------------------------------------------------------------------------------------------")
        else:
            print("No hay jugadores registrados.")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al obtener los jugadores:", e)

def listar_equipos(cursor):
    os.system("cls")
    try:
        print("=== Listado de Equipos ===")
        cursor.execute("SELECT * FROM Equipos")
        equipos = cursor.fetchall()

        if len(equipos) > 0:
            for equipo in equipos:
                print(f"ID: {equipo[0]}\tNombre: {equipo[1]}\tEstadio: {equipo[2]}\tAforo: {equipo[3]}\tAño de fundación: {equipo[4]}\tCiudad: {equipo[5]}")
                print("----------------------------------------------------------------------------------------------------------------------------------")

        else:
            print("No hay equipos registrados.")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al obtener los equipos:", e)

def listar_partidos(cursor):
    os.system("cls")
    try:
        print("=== Listado de Partidos ===")
        cursor.execute("""
            SELECT p.codigo, p.fecha_partido, e1.nombre_equipo AS equipo_local, e2.nombre_equipo AS equipo_visitante,
            p.goles_local, p.goles_visitante
            FROM Partidos p
            INNER JOIN Equipos e1 ON p.equipo_local_id = e1.codigo
            INNER JOIN Equipos e2 ON p.equipo_visitante_id = e2.codigo
        """)
        partidos = cursor.fetchall()

        if len(partidos) > 0:

            for partido in partidos:
                print(f"ID:{partido[0]}\tFecha:{partido[1]}\tEquipo Local: {partido[2]}\tEquipo visitante: {partido[3]}\t\tGoles Local: {partido[4]}\tGoles visitante: {partido[5]}")
                print("-----------------------------------------------------------------------------------------------------------------------------")

        else:
            print("No hay partidos registrados.")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al obtener los partidos:", e)

def listar_presidentes(cursor):
    os.system("cls")
    try:
        print("=== Listado de Presidentes ===")
        cursor.execute("""
            SELECT pr.dni, pr.nombre, pr.apellidos, pr.fecha_nacimiento, e.nombre_equipo AS equipo,
            pr.anio_eleccion
            FROM Presidentes pr
            INNER JOIN Equipos e ON pr.equipo_id = e.codigo
        """)
        presidentes = cursor.fetchall()

        if len(presidentes) > 0:

            for presidente in presidentes:
                print(f"DNI: {presidente[0]}\tNombre y apellidos: {presidente[1]} {presidente[2]}\tFecha de Nacimiento: {presidente[3]}\tEquipo: {presidente[4]}\tAño en que fue elegido: {presidente[5]}")
                print("-------------------------------------------------------------------------------------------------------------------------------------")

        else:
            print("No hay presidentes registrados.")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al obtener los presidentes:", e)

def menu_principal(conn):
    cursor = conn.cursor()

    if conn is None:
        return

    crear_tablas(cursor)

    while True:
        os.system("cls")
        print("=== Liga de Fútbol ===")
        print("1. Insertar Jugador")
        print("2. Insertar Equipo")
        print("3. Insertar Partido")
        print("4. Insertar Presidente")
        print("5. Listar Jugadores")
        print("6. Listar Equipos")
        print("7. Historial de Partidos")
        print("8. Listar Presidentes")
        print("9. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            insertar_jugador(cursor)
        elif opcion == "2":
            insertar_equipo(cursor)
        elif opcion == "3":
            insertar_partido(cursor)
        elif opcion == "4":
            insertar_presidente(cursor)
        elif opcion == "5":
            listar_jugadores(cursor)
        elif opcion == "6":
            listar_equipos(cursor)
        elif opcion == "7":
            listar_partidos(cursor)
        elif opcion == "8":
            listar_presidentes(cursor)
        elif opcion == "9":
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

    cursor.close()
    conn.close()

conn = conectar()
menu_principal(conn)
