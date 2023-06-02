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

def mostrar_datos(cursor):
    print("\n----- DATOS ALMACENADOS -----")

    cursor.execute("SELECT * FROM Autores")
    autores = cursor.fetchall()
    print("\nAutores:")
    for autor in autores:
        print(f"Código: {autor[0]}, Nombre: {autor[1]}")

    cursor.execute("SELECT * FROM Libros")
    libros = cursor.fetchall()
    print("\nLibros:")
    for libro in libros:
        print(f"Código: {libro[0]}, Título: {libro[1]}, ISBN: {libro[2]}, Editorial: {libro[3]}, Páginas: {libro[4]}")

    cursor.execute("SELECT * FROM Ejemplares")
    ejemplares = cursor.fetchall()
    print("\nEjemplares:")
    for ejemplar in ejemplares:
        print(f"Código: {ejemplar[0]}, Código del libro: {ejemplar[1]}, Localización: {ejemplar[2]}")

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
        print("4. Mostrar datos almacenados")
        print("5. Guardar cambios")
        print("6. Salir")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            insertar_autor(cursor)
        elif opcion == "2":
            insertar_libro(cursor)
        elif opcion == "3":
            insertar_ejemplar(cursor)
        elif opcion == "4":
            mostrar_datos(cursor)
        elif opcion == "5":
            guardar_cambios(conn)
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Inténtelo nuevamente.")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
