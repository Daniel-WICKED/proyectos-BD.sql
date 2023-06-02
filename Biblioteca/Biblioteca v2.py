#Proyecto G
#En la biblioteca del centro se manejan fichas de autores y libros. En la ficha de cada
#autor se tiene el código de autor y el nombre. De cada libro se guarda el código, título,
#ISBN, editorial y número de página. Un autor puede escribir varios libros, y un libro puede
#ser escrito por varios autores. Un libro está formado por ejemplares. Cada ejemplar tiene
#un código y una localización. Un libro tiene muchos ejemplares y un ejemplar pertenece
#sólo a un libro.
#Los usuarios de la biblioteca del centro también disponen de ficha en la biblioteca y sacan
#ejemplares de ella. De cada usuario se guarda el código, nombre, dirección y teléfono.
#Los ejemplares son prestados a los usuarios. Un usuario puede tomar prestados varios
#ejemplares, y un ejemplar puede ser prestado a varios usuarios. De cada préstamos
#interesa guardar la fecha de préstamo y la fecha de devolución”.

import psycopg2

def crear_tablas(cursor):
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
            direccion VARCHAR(100) NOT NULL,
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

def insertar_autor(cursor):
    nombre = input("Ingrese el nombre del autor: ")
    cursor.execute("INSERT INTO Autores (nombre) VALUES (%s)", (nombre,))

def insertar_libro(cursor):
    titulo = input("Ingrese el título del libro: ")
    isbn = input("Ingrese el ISBN del libro: ")
    editorial = input("Ingrese la editorial del libro: ")
    numero_pagina = int(input("Ingrese el número de páginas del libro: "))
    cursor.execute("INSERT INTO Libros (titulo, isbn, editorial, numero_pagina) VALUES (%s, %s, %s, %s)",
                   (titulo, isbn, editorial, numero_pagina))

def insertar_ejemplar(cursor):
    codigo_libro = int(input("Ingrese el código del libro: "))
    localizacion = input("Ingrese la localización del ejemplar: ")
    cursor.execute("INSERT INTO Ejemplares (codigo_libro, localizacion) VALUES (%s, %s)",
                   (codigo_libro, localizacion))

def insertar_usuario(cursor):
    nombre = input("Ingrese el nombre del usuario: ")
    direccion = input("Ingrese la dirección del usuario: ")
    telefono = input("Ingrese el teléfono del usuario: ")
    cursor.execute("INSERT INTO Usuarios (nombre, direccion, telefono) VALUES (%s, %s, %s)",
                   (nombre, direccion, telefono))

def realizar_prestamo(cursor):
    codigo_usuario = int(input("Ingrese el código del usuario: "))
    codigo_ejemplar = int(input("Ingrese el código del ejemplar: "))
    fecha_prestamo = input("Ingrese la fecha de préstamo (YYYY-MM-DD): ")
    fecha_devolucion = input("Ingrese la fecha de devolución (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO Prestamos (codigo_usuario, codigo_ejemplar, fecha_prestamo, fecha_devolucion) VALUES (%s, %s, %s, %s)",
                   (codigo_usuario, codigo_ejemplar, fecha_prestamo, fecha_devolucion))

def mostrar_datos(cursor):
    while True:
        print("\n----- DATOS -----")
        print("1. Mostrar autores")
        print("2. Mostrar libros")
        print("3. Mostrar ejemplares")
        print("4. Mostrar usuarios")
        print("5. Mostrar préstamos")
        print("6. Volver al menú principal")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            cursor.execute("SELECT * FROM Autores")
            autores = cursor.fetchall()
            if autores:
                print("Autores:")
                for autor in autores:
                    print(f"Código: {autor[0]}, Nombre: {autor[1]}")
            else:
                print("No hay autores registrados.")
        elif opcion == "2":
            cursor.execute("SELECT * FROM Libros")
            libros = cursor.fetchall()
            if libros:
                print("Libros:")
                for libro in libros:
                    print(f"Código: {libro[0]}, Título: {libro[1]}, ISBN: {libro[2]}, Editorial: {libro[3]}, Número de páginas: {libro[4]}")
            else:
                print("No hay libros registrados.")
        elif opcion == "3":
            cursor.execute("SELECT * FROM Ejemplares")
            ejemplares = cursor.fetchall()
            if ejemplares:
                print("Ejemplares:")
                for ejemplar in ejemplares:
                    print(f"Código: {ejemplar[0]}, Código del libro: {ejemplar[1]}, Localización: {ejemplar[2]}")
            else:
                print("No hay ejemplares registrados.")
        elif opcion == "4":
            cursor.execute("SELECT * FROM Usuarios")
            usuarios = cursor.fetchall()
            if usuarios:
                print("Usuarios:")
                for usuario in usuarios:
                    print(f"Código: {usuario[0]}, Nombre: {usuario[1]}, Dirección: {usuario[2]}, Teléfono: {usuario[3]}")
            else:
                print("No hay usuarios registrados.")
        elif opcion == "5":
            cursor.execute("SELECT * FROM Prestamos")
            prestamos = cursor.fetchall()
            if prestamos:
                print("Préstamos:")
                for prestamo in prestamos:
                    print(f"Código: {prestamo[0]}, Código del usuario: {prestamo[1]}, Código del ejemplar: {prestamo[2]}, Fecha de préstamo: {prestamo[3]}, Fecha de devolución: {prestamo[4]}")
            else:
                print("No hay préstamos registrados.")
        elif opcion == "6":
            break
        else:
            print("Opción inválida. Inténtelo nuevamente.")

def borrar_datos(cursor):
    while True:
        print("\n----- BORRAR DATOS -----")
        print("1. Borrar autor")
        print("2. Borrar libro")
        print("3. Borrar ejemplar")
        print("4. Borrar usuario")
        print("5. Borrar préstamo")
        print("6. Volver al menú principal")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            codigo_autor = int(input("Ingrese el código del autor a borrar: "))
            cursor.execute("DELETE FROM Autores WHERE codigo_autor = %s", (codigo_autor,))
            print("Autor borrado correctamente.")
        elif opcion == "2":
            codigo_libro = int(input("Ingrese el código del libro a borrar: "))
            cursor.execute("DELETE FROM Libros WHERE codigo_libro = %s", (codigo_libro,))
            print("Libro borrado correctamente.")
        elif opcion == "3":
            codigo_ejemplar = int(input("Ingrese el código del ejemplar a borrar: "))
            cursor.execute("DELETE FROM Ejemplares WHERE codigo_ejemplar = %s", (codigo_ejemplar,))
            print("Ejemplar borrado correctamente.")
        elif opcion == "4":
            codigo_usuario = int(input("Ingrese el código del usuario a borrar: "))
            cursor.execute("DELETE FROM Usuarios WHERE codigo_usuario = %s", (codigo_usuario,))
            print("Usuario borrado correctamente.")
        elif opcion == "5":
            codigo_prestamo = int(input("Ingrese el código del préstamo a borrar: "))
            cursor.execute("DELETE FROM Prestamos WHERE codigo_prestamo = %s", (codigo_prestamo,))
            print("Préstamo borrado correctamente.")
        elif opcion == "6":
            break
        else:
            print("Opción inválida. Inténtelo nuevamente.")

def guardar_cambios(conn):
    conn.commit()
    print("Cambios guardados correctamente.")

def main():
    conn = psycopg2.connect(
        host="localhost",
        database="biblioteca",
        user="postgres",
        password="password"
    )

    cursor = conn.cursor()

    crear_tablas(cursor)

    while True:
        print("\n----- MENÚ -----")
        print("1. Agregar autor")
        print("2. Agregar libro")
        print("3. Agregar ejemplar")
        print("4. Agregar usuario")
        print("5. Realizar préstamo")
        print("6. Mostrar datos")
        print("7. Borrar datos")
        print("8. Guardar cambios")
        print("9. Salir")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            insertar_autor(cursor)
        elif opcion == "2":
            insertar_libro(cursor)
        elif opcion == "3":
            insertar_ejemplar(cursor)
        elif opcion == "4":
            insertar_usuario(cursor)
        elif opcion == "5":
            realizar_prestamo(cursor)
        elif opcion == "6":
            mostrar_datos(cursor)
        elif opcion == "7":
            borrar_datos(cursor)
        elif opcion == "8":
            guardar_cambios(conn)
        elif opcion == "9":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Inténtelo nuevamente.")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
