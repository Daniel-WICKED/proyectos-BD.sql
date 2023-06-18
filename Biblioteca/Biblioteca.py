# Proyecto G
# En la biblioteca del centro se manejan fichas de autores y libros. En la ficha de cada
# autor se tiene el código de autor y el nombre. De cada libro se guarda el código, título,
# ISBN, editorial y número de página. Un autor puede escribir varios libros, y un libro puede
# ser escrito por varios autores. Un libro está formado por ejemplares. Cada ejemplar tiene
# un código y una localización. Un libro tiene muchos ejemplares y un ejemplar pertenece
# sólo a un libro.
# Los usuarios de la biblioteca del centro también disponen de ficha en la biblioteca y sacan
# ejemplares de ella. De cada usuario se guarda el código, nombre, dirección y teléfono.
# Los ejemplares son prestados a los usuarios. Un usuario puede tomar prestados varios
# ejemplares, y un ejemplar puede ser prestado a varios usuarios. De cada préstamos
# interesa guardar la fecha de préstamo y la fecha de devolución”.

import psycopg2
import os

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
            input("Presione Enter para continuar...")
            return conn
        except psycopg2.Error as e:
            print("Error al conectar a la base de datos:", e)
            opcion = input("¿Desea volver a ingresar los parámetros de conexión? (s/n): ")
            if opcion.lower() != "s":
                return None


def crear_tablas(conn):
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Autores (
                codigo_autor SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Libros (
                codigo_libro SERIAL PRIMARY KEY,
                titulo VARCHAR(100) NOT NULL,
                isbn VARCHAR(20) NOT NULL,
                editorial VARCHAR(100) NOT NULL,
                numero_pagina INTEGER NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ejemplares (
                codigo_ejemplar SERIAL PRIMARY KEY,
                codigo_libro INTEGER REFERENCES Libros(codigo_libro),
                localizacion VARCHAR(100) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
                codigo_usuario SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                direccion VARCHAR(200) NOT NULL,
                telefono VARCHAR(20) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Prestamos (
                codigo_prestamo SERIAL PRIMARY KEY,
                codigo_usuario INTEGER REFERENCES Usuarios(codigo_usuario),
                codigo_ejemplar INTEGER REFERENCES Ejemplares(codigo_ejemplar),
                fecha_prestamo DATE NOT NULL,
                fecha_devolucion DATE NOT NULL
            )
        """)

        conn.commit()
        print("Tablas creadas exitosamente.")
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)
        conn.rollback()

    cursor.close()


def borrar_consola():
    os.system("cls")


def insertar_autor(cursor):
    borrar_consola()
    nombre = input("Ingrese el nombre del autor: ")
    cursor.execute("SELECT MAX(codigo_autor) FROM Autores")
    ultimo_codigo = cursor.fetchone()[0] 
    if ultimo_codigo is not None:
        nuevo_codigo = ultimo_codigo + 1
    else:
        nuevo_codigo = 1
    cursor.execute("INSERT INTO Autores (codigo_autor, nombre) VALUES (%s, %s)", (nuevo_codigo, nombre))
    cursor.connection.commit()
    print("Autor insertado correctamente. Código del autor:", nuevo_codigo)



def insertar_libro(cursor):
    borrar_consola()
    titulo = input("Ingrese el título del libro: ")
    isbn = input("Ingrese el ISBN del libro: ")
    editorial = input("Ingrese la editorial del libro: ")
    numero_pagina = int(input("Ingrese el número de páginas del libro: "))
    cursor.execute("INSERT INTO Libros (titulo, isbn, editorial, numero_pagina) VALUES (%s, %s, %s, %s)",
                   (titulo, isbn, editorial, numero_pagina))
    cursor.connection.commit()

def insertar_ejemplar(cursor):
    borrar_consola()
    codigo_libro = int(input("Ingrese el código del libro: "))
    localizacion = input("Ingrese la localización del ejemplar: ")
    cursor.execute("INSERT INTO Ejemplares (codigo_libro, localizacion) VALUES (%s, %s)",
                   (codigo_libro, localizacion))
    cursor.connection.commit()

def insertar_usuario(cursor):
    borrar_consola()
    nombre = input("Ingrese el nombre del usuario: ")
    direccion = input("Ingrese la dirección del usuario: ")
    telefono = input("Ingrese el teléfono del usuario: ")
    cursor.execute("INSERT INTO Usuarios (nombre, direccion, telefono) VALUES (%s, %s, %s)",
                   (nombre, direccion, telefono))
    cursor.connection.commit()

def realizar_prestamo(cursor):
    borrar_consola()
    codigo_usuario = int(input("Ingrese el código del usuario: "))
    codigo_ejemplar = int(input("Ingrese el código del ejemplar: "))
    fecha_prestamo = input("Ingrese la fecha de préstamo (YYYY-MM-DD): ")
    fecha_devolucion = input("Ingrese la fecha de devolución (YYYY-MM-DD): ")
    cursor.execute(
        "INSERT INTO Prestamos (codigo_usuario, codigo_ejemplar, fecha_prestamo, fecha_devolucion) VALUES (%s, %s, %s, %s)",
        (codigo_usuario, codigo_ejemplar, fecha_prestamo, fecha_devolucion))
    cursor.connection.commit()

def mostrar_datos(cursor):
    while True:
        borrar_consola()
        print("\n----- DATOS -----")
        print("1. Mostrar autores")
        print("2. Mostrar libros")
        print("3. Mostrar ejemplares")
        print("4. Mostrar usuarios")
        print("5. Mostrar préstamos")
        print("6. Volver al menú principal")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            borrar_consola()
            cursor.execute("SELECT * FROM Autores")
            autores = cursor.fetchall()
            if autores:
                print("Autores:")
                for autor in autores:
                    print(f"Código: {autor[0]}, Nombre: {autor[1]}")
            else:
                print("No hay autores registrados.")
        elif opcion == "2":
            borrar_consola()
            cursor.execute("SELECT * FROM Libros")
            libros = cursor.fetchall()
            if libros:
                print("Libros:")
                for libro in libros:
                    print(
                        f"Código: {libro[0]}, Título: {libro[1]}, ISBN: {libro[2]}, Editorial: {libro[3]}, Número de páginas: {libro[4]}")
            else:
                print("No hay libros registrados.")
        elif opcion == "3":
            borrar_consola()
            cursor.execute("SELECT * FROM Ejemplares")
            ejemplares = cursor.fetchall()
            if ejemplares:
                print("Ejemplares:")
                for ejemplar in ejemplares:
                    print(f"Código: {ejemplar[0]}, Código del libro: {ejemplar[1]}, Localización: {ejemplar[2]}")
            else:
                print("No hay ejemplares registrados.")
        elif opcion == "4":
            borrar_consola()
            cursor.execute("SELECT * FROM Usuarios")
            usuarios = cursor.fetchall()
            if usuarios:
                print("Usuarios:")
                for usuario in usuarios:
                    print(
                        f"Código: {usuario[0]}, Nombre: {usuario[1]}, Dirección: {usuario[2]}, Teléfono: {usuario[3]}")
            else:
                print("No hay usuarios registrados.")
        elif opcion == "5":
            borrar_consola()
            cursor.execute("SELECT * FROM Prestamos")
            prestamos = cursor.fetchall()
            if prestamos:
                print("Préstamos:")
                for prestamo in prestamos:
                    print(
                        f"Código: {prestamo[0]}, Código del usuario: {prestamo[1]}, Código del ejemplar: {prestamo[2]}, Fecha de préstamo: {prestamo[3]}, Fecha de devolución: {prestamo[4]}")
            else:
                print("No hay préstamos registrados.")
        elif opcion == "6":
            break
        else:
            print("Opción inválida. Inténtelo nuevamente.")
        input("Presione Enter para continuar...")


def borrar_datos(cursor):
    while True:
        borrar_consola()
        print("\n----- BORRAR DATOS -----")
        print("1. Borrar autor")
        print("2. Borrar libro")
        print("3. Borrar ejemplar")
        print("4. Borrar usuario")
        print("5. Borrar préstamo")
        print("6. Volver al menú principal")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            borrar_consola()
            codigo_autor = int(input("Ingrese el código del autor a borrar: "))
            cursor.execute("DELETE FROM Autores WHERE codigo_autor = %s", (codigo_autor,))
            print("Autor borrado correctamente.") 
            cursor.connection.commit()
            
        elif opcion == "2":
            borrar_consola()
            codigo_libro = int(input("Ingrese el código del libro a borrar: "))
            cursor.execute("DELETE FROM Libros WHERE codigo_libro = %s", (codigo_libro,))
            print("Libro borrado correctamente.")
            cursor.connection.commit()
           
        elif opcion == "3":
            borrar_consola()
            codigo_ejemplar = int(input("Ingrese el código del ejemplar a borrar: "))
            cursor.execute("DELETE FROM Ejemplares WHERE codigo_ejemplar = %s", (codigo_ejemplar,))
            print("Ejemplar borrado correctamente.")
            cursor.connection.commit()
            
        elif opcion == "4":
            borrar_consola()
            codigo_usuario = int(input("Ingrese el código del usuario a borrar: "))
            cursor.execute("DELETE FROM Usuarios WHERE codigo_usuario = %s", (codigo_usuario,))
            print("Usuario borrado correctamente.")
            cursor.connection.commit()
           
        elif opcion == "5":
            borrar_consola()
            codigo_prestamo = int(input("Ingrese el código del préstamo a borrar: "))
            cursor.execute("DELETE FROM Prestamos WHERE codigo_prestamo = %s", (codigo_prestamo,))
            print("Préstamo borrado correctamente.")
            cursor.connection.commit()
           
        elif opcion == "6":
            break
        else:
            print("Opción inválida. Inténtelo nuevamente.")
        input("Presione Enter para continuar...")


def menu_principal():
    borrar_consola()
    conn = conectar_bd()
    if conn is None:
        return

    cursor = conn.cursor()

    while True:
        borrar_consola()
        print("\n----- ADMINISTRACIÓN BIBLIOTECA -----")
        print("1. Insertar datos")
        print("2. Mostrar datos")
        print("3. Borrar datos")
        print("4. Salir")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            while True:
                borrar_consola()
                print("\n----- INSERTAR DATOS -----")
                print("1. Insertar autor")
                print("2. Insertar libro")
                print("3. Insertar ejemplar")
                print("4. Insertar usuario")
                print("5. Realizar préstamo")
                print("6. Volver al menú principal")

                opcion_insertar = input("Ingrese la opción deseada: ")

                if opcion_insertar == "1":
                    insertar_autor(cursor)
                elif opcion_insertar == "2":
                    insertar_libro(cursor)
                elif opcion_insertar == "3":
                    insertar_ejemplar(cursor)
                elif opcion_insertar == "4":
                    insertar_usuario(cursor)
                elif opcion_insertar == "5":
                    realizar_prestamo(cursor)
                elif opcion_insertar == "6":
                    break
                else:
                    print("Opción inválida. Inténtelo nuevamente.")
                input("Presione Enter para continuar...")
        elif opcion == "2":
            mostrar_datos(cursor)
        elif opcion == "3":
            borrar_datos(cursor)
        elif opcion == "4":
            print ("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Inténtelo nuevamente.")
        input("Presione Enter para continuar...")

    cursor.close()
    conn.close()


menu_principal()
