import os
import psycopg2
from psycopg2 import sql
import datetime

os.system("cls")

def conectar():
    try:
        conn = psycopg2.connect(
            database="escuela",
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
            CREATE TABLE IF NOT EXISTS Profesores (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                direccion VARCHAR(200) NOT NULL,
                poblacion VARCHAR(100) NOT NULL,
                dni VARCHAR(10) NOT NULL,
                fecha_nacimiento DATE NOT NULL,
                codigo_postal VARCHAR(10) NOT NULL,
                telefono VARCHAR(20) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alumnos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                direccion VARCHAR(200) NOT NULL,
                poblacion VARCHAR(100) NOT NULL,
                dni VARCHAR(10) NOT NULL,
                fecha_nacimiento DATE NOT NULL,
                codigo_postal VARCHAR(10) NOT NULL,
                telefono VARCHAR(20) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Asignaturas (
                id SERIAL PRIMARY KEY,
                codigo VARCHAR(10) NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                horas_semana INTEGER NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Notas (
                id SERIAL PRIMARY KEY,
                alumno_id INTEGER REFERENCES Alumnos (id) NOT NULL,
                asignatura_id INTEGER REFERENCES Asignaturas (id) NOT NULL,
                nota DECIMAL(5, 2) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Incidencias (
                id SERIAL PRIMARY KEY,
                alumno_id INTEGER REFERENCES Alumnos (id) NOT NULL,
                asignatura_id INTEGER REFERENCES Asignaturas (id) NOT NULL,
                incidencia TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cursos (
                id SERIAL PRIMARY KEY,
                codigo VARCHAR(10) NOT NULL,
                nombre VARCHAR(100) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Aulas (
                id SERIAL PRIMARY KEY,
                codigo VARCHAR(10) NOT NULL,
                piso INTEGER NOT NULL,
                pupitres INTEGER NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AsignaturasAulas (
                id SERIAL PRIMARY KEY,
                asignatura_id INTEGER REFERENCES Asignaturas (id) NOT NULL,
                aula_id INTEGER REFERENCES Aulas (id) NOT NULL,
                fecha_hora TIMESTAMP NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tutores (
                id SERIAL PRIMARY KEY,
                profesor_id INTEGER REFERENCES Profesores (id) NOT NULL,
                alumno_id INTEGER REFERENCES Alumnos (id) NOT NULL
            )
        """)
        
        print("Tablas creadas exitosamente")
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)

def mostrar_menu():
    os.system("cls")
    print("--- ADMINISTRACIÓN DE LA ESCUELA ---")
    print("1. Registrar profesor")
    print("2. Registrar alumno")
    print("3. Registrar asignatura")
    print("4. Registrar aula")
    print("5. Asignar asignatura a un aula")
    print("6. Registrar nota de un alumno")
    print("7. Registrar incidencia de un alumno")
    print("8. Asignar tutor a un alumno")
    print("9. Salir")

def obtener_fecha_nacimiento():
    while True:
        fecha_nacimiento = input("Ingrese la fecha de nacimiento (formato: DD/MM/AAAA): ")
        try:
            fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
            return fecha_nacimiento
        except ValueError:
            print("Formato de fecha incorrecto. Intente nuevamente.")    

def insertar_aula(cursor):
    os.system("cls")
    try:
        print("=== Insertar Aula ===")
        codigo = input("Código del aula: ")
        piso = input("Piso del centro en el que se encuentra: ")
        numero_pupitres = int(input("Número de pupitres disponibles: "))

        cursor.execute("""
            INSERT INTO Aulas (codigo, piso, pupitres)
            VALUES (%s, %s, %s)
        """, (codigo, piso, numero_pupitres))
        cursor.connection.commit()
        print("Aula guardada correctamente.")
    except psycopg2.Error as e:
        print("Error al insertar los datos:", e)
    input("Presione ENTER para continuar")

def registrar_profesor(cursor):
    os.system("cls")
    print("--- REGISTRO DE PROFESOR ---")
    nombre = input("Ingrese el nombre del profesor: ")
    apellidos = input("Ingrese los apellidos del profesor: ")
    direccion = input("Ingrese la dirección del profesor: ")
    poblacion = input("Ingrese la población del profesor: ")
    dni = input("Ingrese el DNI del profesor: ")
    fecha_nacimiento = obtener_fecha_nacimiento()
    codigo_postal = input("Ingrese el código postal del profesor: ")
    telefono = input("Ingrese el teléfono del profesor: ")

    try:
        insert_query = sql.SQL("""
            INSERT INTO Profesores (nombre, apellidos, direccion, poblacion, dni, fecha_nacimiento, codigo_postal, telefono)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (nombre, apellidos, direccion, poblacion, dni, fecha_nacimiento, codigo_postal, telefono))
        print("Profesor registrado correctamente")
    except psycopg2.Error as e:
        print("Error al registrar el profesor:", e)
    input("Presione ENTER para continuar... ")
    

def registrar_alumno(cursor):
    os.system("cls")
    print("--- REGISTRO DE ALUMNO ---")
    nombre = input("Ingrese el nombre del alumno: ")
    apellidos = input("Ingrese los apellidos del alumno: ")
    direccion = input("Ingrese la dirección del alumno: ")
    poblacion = input("Ingrese la población del alumno: ")
    dni = input("Ingrese el DNI del alumno: ")
    fecha_nacimiento = obtener_fecha_nacimiento()
    codigo_postal = input("Ingrese el código postal del alumno: ")
    telefono = input("Ingrese el teléfono del alumno: ")

    try:
        insert_query = sql.SQL("""
            INSERT INTO Alumnos (nombre, apellidos, direccion, poblacion, dni, fecha_nacimiento, codigo_postal, telefono)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (nombre, apellidos, direccion, poblacion, dni, fecha_nacimiento, codigo_postal, telefono))
        print("Alumno registrado correctamente")
    except psycopg2.Error as e:
        print("Error al registrar el alumno:", e)
    input("Presione ENTER para continuar... ")

def registrar_asignatura(cursor):
    os.system("cls")
    print("--- REGISTRO DE ASIGNATURA ---")
    codigo = input("Ingrese el código de la asignatura: ")
    nombre = input("Ingrese el nombre de la asignatura: ")
    horas_semana = int(input("Ingrese las horas semanales de la asignatura: "))

    try:
        insert_query = sql.SQL("""
            INSERT INTO Asignaturas (codigo, nombre, horas_semana)
            VALUES (%s, %s, %s)
        """)
        cursor.execute(insert_query, (codigo, nombre, horas_semana))
        print("Asignatura registrada correctamente")
    except psycopg2.Error as e:
        print("Error al registrar la asignatura:", e)
    input("Presione ENTER para continuar... ")

def asignar_asignatura_aula(cursor):
    os.system("cls")
    print("--- ASIGNACIÓN DE ASIGNATURA A AULA ---")
    asignatura_id = int(input("Ingrese el ID de la asignatura: "))
    aula_id = int(input("Ingrese el ID del aula: "))
    fecha_hora = datetime.datetime.now()

    try:
        insert_query = sql.SQL("""
            INSERT INTO AsignaturasAulas (asignatura_id, aula_id, fecha_hora)
            VALUES (%s, %s, %s)
        """)
        cursor.execute(insert_query, (asignatura_id, aula_id, fecha_hora))
        print("Asignatura asignada a aula correctamente")
    except psycopg2.Error as e:
        print("Error al asignar la asignatura a aula:", e)
    input("Presione ENTER para continuar... ")

def registrar_nota(cursor):
    os.system("cls")
    print("--- REGISTRO DE NOTA ---")
    alumno_id = int(input("Ingrese el ID del alumno: "))
    asignatura_id = int(input("Ingrese el ID de la asignatura: "))
    nota = float(input("Ingrese la nota del alumno: "))

    try:
        insert_query = sql.SQL("""
            INSERT INTO Notas (alumno_id, asignatura_id, nota)
            VALUES (%s, %s, %s)
        """)
        cursor.execute(insert_query, (alumno_id, asignatura_id, nota))
        print("Nota registrada correctamente")
    except psycopg2.Error as e:
        print("Error al registrar la nota:", e)
    input("Presione ENTER para continuar... ")

def registrar_incidencia(cursor):
    os.system("cls")
    print("--- REGISTRO DE INCIDENCIA ---")
    alumno_id = int(input("Ingrese el ID del alumno: "))
    asignatura_id = int(input("Ingrese el ID de la asignatura: "))
    incidencia = input("Ingrese la incidencia: ")

    try:
        insert_query = sql.SQL("""
            INSERT INTO Incidencias (alumno_id, asignatura_id, incidencia)
            VALUES (%s, %s, %s)
        """)
        cursor.execute(insert_query, (alumno_id, asignatura_id, incidencia))
        print("Incidencia registrada correctamente")
    except psycopg2.Error as e:
        print("Error al registrar la incidencia:", e)
    input("Presione ENTER para continuar... ")

def asignar_tutor(cursor):
    os.system("cls")
    print("--- ASIGNACIÓN DE TUTOR ---")
    profesor_id = int(input("Ingrese el ID del profesor: "))
    alumno_id = int(input("Ingrese el ID del alumno: "))

    try:
        insert_query = sql.SQL("""
            INSERT INTO Tutores (profesor_id, alumno_id)
            VALUES (%s, %s)
        """)
        cursor.execute(insert_query, (profesor_id, alumno_id))
        print("Tutor asignado correctamente")
    except psycopg2.Error as e:
        print("Error al asignar el tutor:", e)
    input("Presione ENTER para continuar... ")

conexion = conectar()
if conexion is not None:
    cursor = conexion.cursor()
    crear_tablas(cursor)
    conexion.commit()
    input("Presione ENTER para continuar... ")

    while True:
        mostrar_menu()
        opcion = input("Ingrese una opción: ")
        if opcion == "1":
            registrar_profesor(cursor)
            conexion.commit()
        elif opcion == "2":
            registrar_alumno(cursor)
            conexion.commit()
        elif opcion == "3":
            registrar_asignatura(cursor)
            conexion.commit()
        elif opcion == "4":
            insertar_aula(cursor)
            conexion.commit()
        elif opcion == "5":
            asignar_asignatura_aula(cursor)
            conexion.commit()
        elif opcion == "6":
            registrar_nota(cursor)
            conexion.commit()
        elif opcion == "7":
            registrar_incidencia(cursor)
            conexion.commit()
        elif opcion == "8":
            asignar_tutor(cursor)
            conexion.commit()
        elif opcion == "9":
            break
        else:
            input("Opción inválida. Intente nuevamente.")

    cursor.close()
    conexion.close()
    print("Programa finalizado")
