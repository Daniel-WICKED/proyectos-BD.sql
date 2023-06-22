import psycopg2
import os
import time

def conectar_bd():
    os.system("cls")
    while True:
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="instituto",
                user="postgres",
                password="password"
            )

            print("Conexión exitosa con la Base de Datos del Instituto.") 
            time.sleep(1)           
            return conn
        except psycopg2.Error as e:
            print("Ha ocurrido un error al intentar conectar con la base de datos. Revise los parámetros de la conexión", e)

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
        
        print("Tablas creadas o comprobadas exitosamente.")
        time.sleep(1)
        print("Cargando Menú Principal...")
        time.sleep(2)
        
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)
    

def insertar_profesor(cursor):
    os.system("cls")
    while True:
        try:
            print("Ingrese los siguientes datos solicitados:")
            dni = input("DNI del profesor: ")
            nombre = input("Nombre: ")
            direccion = input("Dirección particular: ")
            telefono = input("Número de teléfono: ")

            cursor.execute("""
                INSERT INTO Profesores (dni, nombre, direccion, telefono)
                VALUES (%s, %s, %s, %s)
            """, (dni, nombre, direccion, telefono))
            cursor.connection.commit()
            print("Datos del profesor guardados correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al insertar los datos:", e)
            opcion = input("¿Reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_modulo(cursor):
    os.system("cls")
    while True:
        try:
            print("Ingrese los siguientes datos solicitados:")
            codigo = input("Código del módulo: ")
            nombre = input("Nombre: ")
            profesor_dni = input("DNI del profesor designado al módulo: ")
            cursor.execute("""
                INSERT INTO Modulos (codigo, nombre, profesor_dni)
                VALUES (%s, %s, %s)
            """, (codigo, nombre, profesor_dni))
            cursor.connection.commit()
            print("Módulo insertado con éxito.")
            input("Presione ENTER para continuar")
            break
        
        except psycopg2.Error as e:
            print("Error al insertar los datos del módulo:", e)
            opcion = input("¿Reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_alumno(cursor):
    os.system("cls")
    while True:
        try:
            print("Ingrese los siguientes datos solicitados:")
            nombre = input("Nombre del alumno: ")
            apellidos = input("Apellidos: ")
            fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")

            cursor.execute("""
                INSERT INTO Alumnos (nombre, apellidos, fecha_nacimiento)
                VALUES (%s, %s, %s)
            """, (nombre, apellidos, fecha_nacimiento))
            cursor.connection.commit()
            print("Datos del alumno insertados de forma exitosa")
            input("Presione ENTER para continuar")
            break
        
        except psycopg2.Error as e:
            print("Ha ocurrido un error al insertar los datos del alumno:", e)
            opcion = input("¿Reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_matricula(cursor):
    os.system("cls")
    while True:
        try:
            print("Ingrese los siguientes datos solicitados:")
            alumno_numero_expediente = input("Número de expediente del alumno: ")
            modulo_codigo = input("Código del módulo: ")

            cursor.execute("""
                INSERT INTO Matriculas (alumno_numero_expediente, modulo_codigo)
                VALUES (%s, %s)
            """, (alumno_numero_expediente, modulo_codigo))
            cursor.connection.commit()
            input("Presione ENTER para continuar")
            print("Matrícula insertada exitosamente.")
            break
        except psycopg2.Error as e:
            print("Ha ocurrido un error al insertar la matrícula:", e)
            opcion = input("¿Reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_curso(cursor):
    os.system("cls")
    while True:
        try:
            print("Ingrese los siguientes datos solicitados:")
            nombre = input("Nombre del curso: ")
            delegado_alumno_numero_expediente = input("Número de expediente del delegado del curso: ")
            cursor.execute("""
                INSERT INTO Cursos (nombre, delegado_alumno_numero_expediente)
                VALUES (%s, %s)
            """, (nombre, delegado_alumno_numero_expediente))
            cursor.connection.commit()
            print("Datos del curso insertados exitosamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Ha ocurrido un error al insertar el curso:", e)
            opcion = input("¿Reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_alumno_curso(cursor):
    os.system("cls")
    while True:
        try:
            print("Ingrese los siguientes datos solicitados:")
            curso_id = input("ID del curso: ")
            alumno_numero_expediente = input("Número del expediente del alumno: ")

            cursor.execute("""
                INSERT INTO Cursos_Alumnos (curso_id, alumno_numero_expediente)
                VALUES (%s, %s)
            """, (curso_id, alumno_numero_expediente))
            cursor.connection.commit()
            print("Alumno insertado al curso exitosamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Ha ocurrido un error al insertar el alumno al curso:", e)
            opcion = input("¿Reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def mostrar_profesores(cursor):
    os.system("cls")
    cursor.execute("SELECT * FROM Profesores")
    profesores = cursor.fetchall()
    if len(profesores) == 0:
        print("No hay profesores registrados.")
    else:
        print("LISTADO DE PROFESORES: ")
        for profesor in profesores:
            print("DNI:", profesor[0])
            print("Nombre:", profesor[1])
            print("Dirección:", profesor[2])
            print("Teléfono:", profesor[3])
            print("-------------------------")
            
    input("Presione ENTER para volver")

def mostrar_modulos(cursor):
    os.system("cls")
    cursor.execute("SELECT * FROM Modulos")
    modulos = cursor.fetchall()
    if len(modulos) == 0:
        print("No hay módulos registrados.")
    else:
        print("LISTADO DE MÓDULOS REGISTRADOS:")
        for modulo in modulos:
            print("Código:", modulo[0])
            print("Nombre:", modulo[1])
            print("DNI del profesor:", modulo[2])
            print("--------------------------------")
    input("Presione ENTER para volver")

def mostrar_alumnos(cursor):
    os.system("cls")
    cursor.execute("SELECT * FROM Alumnos")
    alumnos = cursor.fetchall()
    if len(alumnos) == 0:
        print("No hay alumnos registrados.")
    else:
        print("LISTADO DE LOS ALUMNOS:")
        for alumno in alumnos:
            print("Número expediente:", alumno[0])
            print("Nombre:", alumno[1])
            print("Apellidos:", alumno[2])
            print("Fecha de nacimiento:", alumno[3])
            print("----------------------------------")
    input("Presione ENTER para volver")

def mostrar_matriculas(cursor):
    os.system("cls")
    cursor.execute("SELECT * FROM Matriculas")
    matriculas = cursor.fetchall()
    if len(matriculas) == 0:
        print("No se encontraron matrículas registradas.")
    else:
        print("LISTADO DE MATRÍCULAS REGISTRADAS:")
        for matricula in matriculas:
            print("Número de expediente del alumno:", matricula[0])
            print("Código del módulo:", matricula[1])
            print("----------------------------------------")
    input("Presione ENTER para volver")

def mostrar_cursos(cursor):
    os.system("cls")
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
        print("LISTADO DE CURSOS:")
        for curso in cursos:
            print("ID:", curso[0])
            print("Nombre:", curso[1])
            print("Delegado:", curso[2])
            print("Alumnos:", curso[3])
            print("----------------------------")
    input("Presione ENTER para volver")



def borrar_profesor(cursor):
    os.system("cls")
    dni = input("Ingrese el DNI del profesor a borrar: ")
    cursor.execute("DELETE FROM Profesores WHERE dni = %s", (dni,))
    cursor.connection.commit()
    print("Profesor borrado.")
    input("Presione ENTER para volver")

def borrar_modulo(cursor):
    os.system("cls")
    codigo = input("Ingrese el código del módulo a borrar: ")
    cursor.execute("DELETE FROM Modulos WHERE codigo = %s", (codigo,))
    cursor.connection.commit()
    print("Módulo borrado.")
    input("Presione ENTER para volver")

def borrar_alumno(cursor):
    os.system("cls")
    numero_expediente = input("Ingrese el número de expediente del alumno a borrar: ")
    cursor.execute("DELETE FROM Alumnos WHERE numero_expediente = %s", (numero_expediente,))
    cursor.connection.commit()
    print("Alumno borrado.")
    input("Presione ENTER para volver")

def borrar_matricula(cursor):
    os.system("cls")
    alumno_numero_expediente = input("Ingrese el número de expediente del alumno: ")
    modulo_codigo = input("Ingrese el código del módulo a borrar de la matrícula: ")
    cursor.execute("DELETE FROM Matriculas WHERE alumno_numero_expediente = %s AND modulo_codigo = %s",
                   (alumno_numero_expediente, modulo_codigo))
    cursor.connection.commit()
    print("Matrícula borrada.")
    input("Presione ENTER para volver")

def borrar_curso(cursor):
    os.system("cls")
    id = input("Ingrese el ID del curso a borrar: ")
    cursor.execute("DELETE FROM Cursos_Alumnos WHERE curso_id = %s", (id,))
    cursor.execute("DELETE FROM Cursos WHERE id = %s", (id,))
    cursor.connection.commit()
    print("Curso borrado.")
    input("Presione ENTER para volver")


def main():
    conn = conectar_bd()
    cursor = conn.cursor()

    crear_tablas(cursor)

    while True:
        os.system("cls")
        print("ADMINISTRACIÓN DE DATOS DEL INSTITUTO")
        print()
        print("1. Insertar datos")
        print("2. Mostrar datos")
        print("3. Eliminar registros")
        print("0. Salir del programa")
        print("===============================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            while True:
                os.system("cls")
                print("INSERTAR:")
                print()
                print("1. Insertar profesor")
                print("2. Insertar módulo")
                print("3. Insertar alumno")
                print("4. Insertar matrícula")
                print("5. Insertar curso")
                print("6. Insertar alumno a curso")
                print()
                print("0. Volver al menú principal")
                print("===============================")
                subopcion = input("Seleccione una opción: ")

                if subopcion == "1":
                    insertar_profesor(cursor)
                elif subopcion == "2":
                    insertar_modulo(cursor)
                elif subopcion == "3":
                    insertar_alumno(cursor)
                elif subopcion == "4":
                    insertar_matricula(cursor)
                elif subopcion == "5":
                    insertar_curso(cursor)
                elif subopcion == "6":
                    insertar_alumno_curso(cursor)
                elif subopcion == "0":
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")
                    time.sleep(1)
        elif opcion == "2":
            while True:
                os.system("cls")
                print("MOSTRAR:")
                print()
                print("1. Mostrar profesores")
                print("2. Mostrar módulos")
                print("3. Mostrar alumnos")
                print("4. Mostrar matrículas")
                print("5. Mostrar cursos")
                print()
                print("0. Volver al menú principal")
                print("===============================")
                subopcion = input("Seleccione una opción: ")

                if subopcion == "1":
                    mostrar_profesores(cursor)
                elif subopcion == "2":
                    mostrar_modulos(cursor)
                elif subopcion == "3":
                    mostrar_alumnos(cursor)
                elif subopcion == "4":
                    mostrar_matriculas(cursor)
                elif subopcion == "5":
                    mostrar_cursos(cursor)
                elif subopcion == "0":
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")
                    time.sleep(1)
        elif opcion == "3":
            while True:
                os.system("cls")
                print("ELIMINAR:")
                print()
                print("1. Eliminar profesor")
                print("2. Eliminar módulo")
                print("3. Eliminar alumno")
                print("4. Eliminar matrícula")
                print("5. Eliminar curso")
                print()
                print("0. Volver al menú principal")
                print("===============================")
                subopcion = input("Seleccione una opción: ")

                if subopcion == "1":
                    borrar_profesor(cursor)
                elif subopcion == "2":
                    borrar_modulo(cursor)
                elif subopcion == "3":
                    borrar_alumno(cursor)
                elif subopcion == "4":
                    borrar_matricula(cursor)
                elif subopcion == "5":
                    borrar_curso(cursor)
                elif subopcion == "0":
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")
                    time.sleep(1)
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
            time.sleep(1)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
