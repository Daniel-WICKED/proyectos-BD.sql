import psycopg2
import os

def establecer_conexion():
    limpiar_consola()
    while True:
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="instituto",
                user="postgres",
                password="password"
            )

            print("Conexión con la base de datos completada.")            
            return conn
        except psycopg2.Error as e:
            print("Error al conectar a la base de datos:", e)

def crear_tablas(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Profesores (
                dni VARCHAR(10) PRIMARY KEY,
                nombre VARCHAR(100),
                direccion VARCHAR(100),
                telefono VARCHAR(20)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Modulos (
                codigo VARCHAR(10) PRIMARY KEY,
                nombre VARCHAR(100),
                profesor_dni VARCHAR(10),
                FOREIGN KEY (profesor_dni) REFERENCES Profesores(dni)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alumnos (
                numero_expediente SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                apellidos VARCHAR(100),
                fecha_nacimiento DATE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Matriculas (
                id SERIAL PRIMARY KEY,
                alumno_numero_expediente INTEGER REFERENCES Alumnos(numero_expediente),
                modulo_codigo VARCHAR(10) REFERENCES Modulos(codigo)
    )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cursos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                delegado_alumno_numero_expediente INTEGER REFERENCES Alumnos(numero_expediente)
            )
        """)
        
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cursos_Alumnos (
        curso_id INTEGER REFERENCES Cursos(id),
        alumno_numero_expediente INTEGER REFERENCES Alumnos(numero_expediente),
        PRIMARY KEY (curso_id, alumno_numero_expediente)
    )
""")
        
        print("Tablas comprobadas correctamente.")
        input("Presione Enter para continuar hacia el menú del programa")
        
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)

def limpiar_consola():
    os.system("cls")

def insertar_profesor(cursor):
    limpiar_consola()
    while True:
        try:
            dni = input("Ingrese el DNI del profesor: ")
            nombre = input("Ingrese el nombre del profesor: ")
            direccion = input("Ingrese la dirección del profesor: ")
            telefono = input("Ingrese el teléfono del profesor: ")

            cursor.execute("""
                INSERT INTO Profesores (dni, nombre, direccion, telefono)
                VALUES (%s, %s, %s, %s)
            """, (dni, nombre, direccion, telefono))
            cursor.connection.commit()
            print("Profesor insertado correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al insertar el profesor:", e)
            opcion = input("¿Desea reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_modulo(cursor):
    limpiar_consola()
    while True:
        try:
            codigo = input("Ingrese el código del módulo: ")
            nombre = input("Ingrese el nombre del módulo: ")
            profesor_dni = input("Ingrese el DNI del profesor que imparte el módulo: ")
            cursor.execute("""
                INSERT INTO Modulos (codigo, nombre, profesor_dni)
                VALUES (%s, %s, %s)
            """, (codigo, nombre, profesor_dni))
            cursor.connection.commit()
            print("Módulo insertado correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al insertar el módulo:", e)
            opcion = input("¿Desea reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_alumno(cursor):
    limpiar_consola()
    while True:
        try:
            nombre = input("Ingrese el nombre del alumno: ")
            apellidos = input("Ingrese los apellidos del alumno: ")
            fecha_nacimiento = input("Ingrese la fecha de nacimiento del alumno (YYYY-MM-DD): ")

            cursor.execute("""
                INSERT INTO Alumnos (nombre, apellidos, fecha_nacimiento)
                VALUES (%s, %s, %s)
            """, (nombre, apellidos, fecha_nacimiento))
            cursor.connection.commit()
            print("Alumno insertado correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al insertar el alumno:", e)
            opcion = input("¿Desea reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_matricula(cursor):
    limpiar_consola()
    while True:
        try:
            alumno_numero_expediente = input("Ingrese el número de expediente del alumno: ")
            modulo_codigo = input("Ingrese el código del módulo: ")

            cursor.execute("""
                INSERT INTO Matriculas (alumno_numero_expediente, modulo_codigo)
                VALUES (%s, %s)
            """, (alumno_numero_expediente, modulo_codigo))
            cursor.connection.commit()
            input("Presione ENTER para continuar")
            print("Matrícula insertada correctamente.")
            break
        except psycopg2.Error as e:
            print("Error al insertar la matrícula:", e)
            opcion = input("¿Desea reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_curso(cursor):
    limpiar_consola()
    while True:
        try:
            nombre = input("Ingrese el nombre del curso: ")
            delegado_alumno_numero_expediente = input("Ingrese el número de expediente del delegado del curso: ")

            cursor.execute("""
                INSERT INTO Cursos (nombre, delegado_alumno_numero_expediente)
                VALUES (%s, %s)
            """, (nombre, delegado_alumno_numero_expediente))
            cursor.connection.commit()
            print("Curso insertado correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al insertar el curso:", e)
            opcion = input("¿Desea reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_alumno_curso(cursor):
    limpiar_consola()
    while True:
        try:
            curso_id = input("Ingrese el ID del curso: ")
            alumno_numero_expediente = input("Ingrese el número de expediente del alumno: ")

            cursor.execute("""
                INSERT INTO Cursos_Alumnos (curso_id, alumno_numero_expediente)
                VALUES (%s, %s)
            """, (curso_id, alumno_numero_expediente))
            cursor.connection.commit()
            print("Relación alumno-curso insertada correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al insertar la relación alumno-curso:", e)
            opcion = input("¿Desea reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def mostrar_profesores(cursor):
    limpiar_consola()
    cursor.execute("SELECT * FROM Profesores")
    profesores = cursor.fetchall()
    if len(profesores) == 0:
        print("No hay profesores registrados.")
    else:
        print("======== LISTA DE PROFESORES =======")
        for profesor in profesores:
            print("DNI:", profesor[0])
            print("Nombre:", profesor[1])
            print("Dirección:", profesor[2])
            print("Teléfono:", profesor[3])
            print("===================================")
            
    input("Presione ENTER para continuar")

def mostrar_modulos(cursor):
    limpiar_consola()
    cursor.execute("SELECT * FROM Modulos")
    modulos = cursor.fetchall()
    if len(modulos) == 0:
        print("No hay módulos registrados.")
    else:
        print("======== LISTA DE MÓDULOS =======")
        for modulo in modulos:
            print("Código:", modulo[0])
            print("Nombre:", modulo[1])
            print("Profesor DNI:", modulo[2])
            print("=================================")
    input("Presione ENTER para continuar")

def mostrar_alumnos(cursor):
    limpiar_consola()
    cursor.execute("SELECT * FROM Alumnos")
    alumnos = cursor.fetchall()
    if len(alumnos) == 0:
        print("No hay alumnos registrados.")
    else:
        print("======== LISTA DE ALUMNOS =======")
        for alumno in alumnos:
            print("Número de expediente:", alumno[0])
            print("Nombre:", alumno[1])
            print("Apellidos:", alumno[2])
            print("Fecha de nacimiento:", alumno[3])
            print("=================================")
    input("Presione ENTER para continuar")

def mostrar_matriculas(cursor):
    limpiar_consola()
    cursor.execute("SELECT * FROM Matriculas")
    matriculas = cursor.fetchall()
    if len(matriculas) == 0:
        print("No hay matrículas registradas.")
    else:
        print("======== LISTA DE MATRÍCULAS =======")
        for matricula in matriculas:
            print("Número de expediente del alumno:", matricula[0])
            print("Código del módulo:", matricula[1])
            print("====================================")
    input("Presione ENTER para continuar")

def mostrar_cursos(cursor):
    limpiar_consola()
    cursor.execute("""
        SELECT c.id, c.nombre, a.nombre AS delegado, array_agg(al.nombre) AS alumnos
        FROM Cursos c
        JOIN Alumnos a ON c.delegado_alumno_numero_expediente = a.numero_expediente
        LEFT JOIN Cursos_Alumnos ca ON c.id = ca.curso_id
        LEFT JOIN Alumnos al ON ca.alumno_numero_expediente = al.numero_expediente
        GROUP BY c.id, c.nombre, a.nombre
    """)
    cursos = cursor.fetchall()
    if len(cursos) == 0:
        print("No hay cursos registrados.")
    else:
        print("======== LISTA DE CURSOS =======")
        for curso in cursos:
            print("ID:", curso[0])
            print("Nombre:", curso[1])
            print("Delegado:", curso[2])
            print("Alumnos:", curso[3])
            print("================================")
    input("Presione ENTER para continuar")



def borrar_profesor(cursor):
    limpiar_consola()
    dni = input("Ingrese el DNI del profesor a borrar: ")
    cursor.execute("DELETE FROM Profesores WHERE dni = %s", (dni,))
    cursor.connection.commit()
    print("Profesor borrado correctamente.")
    input("Presione ENTER para continuar")

def borrar_modulo(cursor):
    limpiar_consola()
    codigo = input("Ingrese el código del módulo a borrar: ")
    cursor.execute("DELETE FROM Modulos WHERE codigo = %s", (codigo,))
    cursor.connection.commit()
    print("Módulo borrado correctamente.")
    input("Presione ENTER para continuar")

def borrar_alumno(cursor):
    limpiar_consola()
    numero_expediente = input("Ingrese el número de expediente del alumno a borrar: ")
    cursor.execute("DELETE FROM Alumnos WHERE numero_expediente = %s", (numero_expediente,))
    cursor.connection.commit()
    print("Alumno borrado correctamente.")
    input("Presione ENTER para continuar")

def borrar_matricula(cursor):
    limpiar_consola()
    alumno_numero_expediente = input("Ingrese el número de expediente del alumno: ")
    modulo_codigo = input("Ingrese el código del módulo a borrar de la matrícula: ")
    cursor.execute("DELETE FROM Matriculas WHERE alumno_numero_expediente = %s AND modulo_codigo = %s",
                   (alumno_numero_expediente, modulo_codigo))
    cursor.connection.commit()
    print("Matrícula borrada correctamente.")
    input("Presione ENTER para continuar")

def borrar_curso(cursor):
    limpiar_consola()
    id = input("Ingrese el ID del curso a borrar: ")
    cursor.execute("DELETE FROM Cursos_Alumnos WHERE curso_id = %s", (id,))
    cursor.execute("DELETE FROM Cursos WHERE id = %s", (id,))
    cursor.connection.commit()
    print("Curso borrado correctamente.")
    input("Presione ENTER para continuar")
    
def main():
    conn = establecer_conexion()
    cursor = conn.cursor()

    crear_tablas(cursor)

    while True:
        limpiar_consola()
        print("             ================== BASE DE DATOS DEL INSTITUTO ==================")
        print()
        print("| INSERTAR: 1-profesor        | MOSTRAR: 7-profesores    | ELIMINAR REGISTROS: 12-profesor   |")
        print("|           2-módulo          |          8-módulos       |                     13-módulos    |")
        print("|           3-alumno          |          9-alumnos       |                     14-alumnos    |")
        print("|           4-matricula       |          10-matrículas   |                     15-matrícula  |")
        print("|           5-curso           |          11-cursos       |                     16-curso      |")
        print("|           6-alumno a curso  |                          |                                   |")
        print()
        print("0. Salir del programa")
        print("===============================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            insertar_profesor(cursor)
        elif opcion == "2":
            insertar_modulo(cursor)
        elif opcion == "3":
            insertar_alumno(cursor)
        elif opcion == "4":
            insertar_matricula(cursor)
        elif opcion == "5":
            insertar_curso(cursor)
        elif opcion == "6":
            insertar_alumno_curso(cursor)
        elif opcion == "7":
            mostrar_profesores(cursor)
        elif opcion == "8":
            mostrar_modulos(cursor)
        elif opcion == "9":
            mostrar_alumnos(cursor)
        elif opcion == "10":
            mostrar_matriculas(cursor)
        elif opcion == "11":
            mostrar_cursos(cursor)
        elif opcion == "12":
            borrar_profesor(cursor)
        elif opcion == "13":
            borrar_modulo(cursor)
        elif opcion == "14":
            borrar_alumno(cursor)
        elif opcion == "15":
            borrar_matricula(cursor)
        elif opcion == "16":
            borrar_curso(cursor)
        elif opcion == "0":
            break
        else:
            print("Opción inválida. Intente nuevamente.")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
