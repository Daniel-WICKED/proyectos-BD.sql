import os
import time
import psycopg2
import psycopg2.extras


def establecer_conexion():
    os.system("cls")   

    while True:
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="gest_bib",
                user="postgres",
                password="password"
            )

            print("Conexión con la base de datos completada.")
            time.sleep(1)
            return conn
        except psycopg2.Error as e:
            print("Error al conectar a la base de datos:", e)    
            input("Presione Enter para reintentar...")

def crear_tablas(cursor):
    while True:
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Temas (
                    id SERIAL PRIMARY KEY,
                    tema VARCHAR(255) NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Bibliografias (
                    id SERIAL PRIMARY KEY,
                    id_tema INTEGER REFERENCES Temas (id),
                    subtema VARCHAR(255) NOT NULL,
                    nombre_libro VARCHAR(255) NOT NULL,
                    autor VARCHAR(255) NOT NULL,
                    fecha_publicacion DATE NOT NULL,
                    lugar_publicacion VARCHAR(255) NOT NULL,
                    isbn VARCHAR(20) NOT NULL,
                    issn VARCHAR(20) NOT NULL,
                    editorial VARCHAR(255) NOT NULL,
                    tipo_bibliografia VARCHAR(20) NOT NULL,
                    edicion VARCHAR(50),
                    idioma VARCHAR(50),
                    cantidad_paginas INTEGER,
                    estanteria VARCHAR(50),
                    fecha_agregado DATE,
                    cantidad_ejemplares INTEGER,
                    original_copia VARCHAR(10),
                    enlace_web VARCHAR(255),
                    nombre_revista VARCHAR(255),
                    pagina INTEGER,
                    series_articulo VARCHAR(255),
                    nombre_periodico VARCHAR(255),
                    cantidad INTEGER,
                    comentarios_extra TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Personas (
                    id SERIAL PRIMARY KEY,
                    nombre_completo VARCHAR(255) NOT NULL,
                    carnet_identidad VARCHAR(20) NOT NULL,
                    tipo_persona VARCHAR(20) NOT NULL,
                    acreditacion BOOLEAN NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Solicitudes (
                    id_persona INTEGER REFERENCES Personas (id),
                    id_bibliografia INTEGER REFERENCES Bibliografias (id),
                    PRIMARY KEY (id_persona, id_bibliografia)
                )
            """)
            
            cursor.connection.commit()
            
            print("Tablas comprobadas correctamente.")
            time.sleep(1)
            print("Iniciando el programa...")
            time.sleep(2)
            break
            
        except psycopg2.Error as e:
            print("Error al crear las tablas:", e)
            input("Presione Enter para reintentar...")

def insertar_tema(cursor, tema):
    cursor.execute("""
        INSERT INTO Temas (tema)
        VALUES (%s)
    """, (tema,))
    cursor.connection.commit()

def eliminar_tema(cursor, id_tema):
    cursor.execute("""
        DELETE FROM Temas WHERE id = %s
    """, (id_tema,))
    cursor.connection.commit()


def insertar_bibliografia(cursor):
    while True:
        try:
            os.system("cls")
            mostrar_temas(cursor)
            print("==============================================================")
            id_tema = int(input("Ingrese el ID del tema al que pertenece la bibliografía: "))
            subtema = input("Ingrese el subtema: ")
            nombre_libro = input("Ingrese el nombre de la bibliografía: ")
            autor = input("Ingrese el autor del libro: ")
            fecha_publicacion = input("Ingrese la fecha de publicación (YYYY-MM-DD): ")
            lugar_publicacion = input("Ingrese el lugar de publicación: ")
            isbn = input("Ingrese el ISBN: ")
            issn = input("Ingrese el ISSN: ")
            editorial = input("Ingrese la editorial: ")
            tipo_bibliografia = input("Ingrese el tipo de bibliografía (libro, documento, articulo_revista, articulo_periodistico): ")

            if tipo_bibliografia == "libro":
                edicion = input("Ingrese la edición del libro: ")
                idioma = input("Ingrese el idioma del libro: ")
                cantidad_paginas = int(input("Ingrese la cantidad de páginas del libro: "))
                estanteria = input("Ingrese la estantería donde se encuentra el libro: ")
                fecha_agregado = input("Ingrese la fecha en que fue agregado el libro (YYYY-MM-DD): ")
                cantidad_ejemplares = int(input("Ingrese la cantidad de ejemplares disponibles: "))
                original_copia = input("Ingrese si es un libro original o copia: ")
                enlace_web = input("Ingrese el enlace web del libro: ")

                cursor.execute("""
                    INSERT INTO Bibliografias (
                        id_tema, subtema, nombre_libro, autor, fecha_publicacion, lugar_publicacion, isbn, issn, editorial,
                        tipo_bibliografia, edicion, idioma, cantidad_paginas, estanteria, fecha_agregado, cantidad_ejemplares,
                        original_copia, enlace_web
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_tema, subtema, nombre_libro, autor, fecha_publicacion, lugar_publicacion, isbn, issn, editorial,
                      tipo_bibliografia, edicion, idioma, cantidad_paginas, estanteria, fecha_agregado, cantidad_ejemplares,
                      original_copia, enlace_web))

            elif tipo_bibliografia == "documento":
                idioma = input("Ingrese el idioma del documento: ")
                enlace_web = input("Ingrese el enlace web del documento: ")
                estanteria = input("Ingrese la estantería donde se encuentra el documento: ")
                cantidad = int(input("Ingrese la cantidad de documentos disponibles: "))
                fecha_agregado = input("Ingrese la fecha en que fue agregado el documento (YYYY-MM-DD): ")
                comentarios_extra = input("Ingrese comentarios adicionales sobre el documento: ")

                cursor.execute("""
                    INSERT INTO Bibliografias (
                        id_tema, subtema, nombre_libro, autor, fecha_publicacion, lugar_publicacion, isbn, issn, editorial,
                        tipo_bibliografia, idioma, enlace_web, estanteria, cantidad, fecha_agregado, comentarios_extra
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_tema, subtema, nombre_libro, autor, fecha_publicacion, lugar_publicacion, isbn, issn, editorial,
                      tipo_bibliografia, idioma, enlace_web, estanteria, cantidad, fecha_agregado, comentarios_extra))

            elif tipo_bibliografia == "articulo_revista":
                nombre_revista = input("Ingrese el nombre de la revista: ")
                pagina = int(input("Ingrese la página del artículo en la revista: "))
                cantidad_paginas = int(input("Ingrese la cantidad de páginas del artículo: "))
                series_articulo = input("Ingrese las series del artículo: ")
                idioma = input("Ingrese el idioma del artículo: ")
                enlace_web = input("Ingrese el enlace web del artículo: ")
                estanteria = input("Ingrese la estantería donde se encuentra el artículo: ")
                fecha_agregado = input("Ingrese la fecha en que fue agregado el artículo (YYYY-MM-DD): ")
                comentarios_extra = input("Ingrese comentarios adicionales sobre el artículo: ")

                cursor.execute("""
                    INSERT INTO Bibliografias (
                        id_tema, subtema, nombre_libro, autor, fecha_publicacion, lugar_publicacion, isbn, issn, editorial,
                        tipo_bibliografia, nombre_revista, pagina, cantidad_paginas, series_articulo, idioma, enlace_web,
                        estanteria, fecha_agregado, comentarios_extra
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_tema, subtema, nombre_libro, autor, fecha_publicacion, lugar_publicacion, isbn, issn, editorial,
                      tipo_bibliografia, nombre_revista, pagina, cantidad_paginas, series_articulo, idioma, enlace_web,
                      estanteria, fecha_agregado, comentarios_extra))

            elif tipo_bibliografia == "articulo_periodistico":
                nombre_periodico = input("Ingrese el nombre del periódico: ")
                pagina = int(input("Ingrese la página del artículo en el periódico: "))
                cantidad_paginas = int(input("Ingrese la cantidad de páginas del artículo: "))
                idioma = input("Ingrese el idioma del artículo: ")
                enlace_web = input("Ingrese el enlace web del artículo: ")
                cantidad = int(input("Ingrese la cantidad de artículos disponibles: "))
                estanteria = input("Ingrese la estantería donde se encuentra el artículo: ")
                fecha_agregado = input("Ingrese la fecha en que fue agregado el artículo (YYYY-MM-DD): ")
                comentarios_extra = input("Ingrese comentarios adicionales sobre el artículo: ")

                cursor.execute("""
                    INSERT INTO Bibliografias (
                        id_tema, subtema, nombre_libro, autor, fecha_publicacion, lugar_publicacion, isbn, issn, editorial,
                        tipo_bibliografia, nombre_periodico, pagina, cantidad_paginas, idioma, enlace_web, cantidad,
                        estanteria, fecha_agregado, comentarios_extra
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_tema, subtema, nombre_libro, autor, fecha_publicacion, lugar_publicacion, isbn, issn, editorial,
                      tipo_bibliografia, nombre_periodico, pagina, cantidad_paginas, idioma, enlace_web, cantidad,
                      estanteria, fecha_agregado, comentarios_extra))

            cursor.connection.commit()
            print("Bibliografía agregada exitosamente.")
            input("Presione Enter para volver al menú continuar...")
            break
        except Exception as e:
            print(f"Ocurrió un error: {str(e)}")
            opcion = input("¿Desea reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def registrar_persona(cursor):
    while True:
        try:
            os.system("cls")
            nombre_completo = input("Ingrese el nombre completo de la persona: ")
            carnet_identidad = input("Ingrese el carnet de identidad de la persona: ")
            tipo_persona = input("Ingrese el tipo de persona (estudiante, docente, otro): ")
            acreditacion = input("¿Tiene acreditación para descargar materiales? (si/no): ").lower() == "si"

            cursor.execute("""
                INSERT INTO Personas (nombre_completo, carnet_identidad, tipo_persona, acreditacion)
                VALUES (%s, %s, %s, %s)
            """, (nombre_completo, carnet_identidad, tipo_persona, acreditacion))
            cursor.connection.commit()
            print("Persona registrada exitosamente.")
            input("Presione Enter para continuar...")
            break
        except Exception as e:
            print(f"Ocurrió un error: {str(e)}")
            opcion = input("¿Desea reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def asignar_bibliografia(cursor):
    os.system("cls")
    while True:
        try:
            cursor.execute("SELECT * FROM Personas")
            personas = cursor.fetchall()

            if personas:
                print("Personas registradas:")
            for persona in personas:
                id_persona = persona[0]
                nombre_completo = persona[1]
                print(f"ID: {id_persona}")
                print(f"Nombre completo: {nombre_completo}")
            print("===================================")    
            id_persona = int(input("Ingrese el ID de la persona a la cual se le asignará la bibliografía: "))
            
            id_bibliografia = int(input("Ingrese el ID de la bibliografía: "))

            cursor.execute("""
                INSERT INTO Solicitudes (id_persona, id_bibliografia)
                VALUES (%s, %s)
            """, (id_persona, id_bibliografia))
            cursor.connection.commit()
            print("Bibliografía asignada exitosamente.")
            input("Presione Enter para continuar...")
            break
        except ValueError:
            print("Error: Ingrese un número entero válido.")
        except Exception as e:
            os.system("cls")
            print(f"Error: {str(e)}")
            retry = input("¿Desea reintentar? (s/n): ")
            if retry.lower() != "s":
                break

def mostrar_personas_registradas(cursor):
    os.system("cls")
    cursor.execute("SELECT * FROM Personas")
    personas = cursor.fetchall()

    if personas:
        print("Personas registradas:")
        for persona in personas:
            id_persona = persona[0]
            nombre_completo = persona[1]
            carnet_identidad = persona[2]
            tipo_persona = persona[3]
            acreditacion = persona[4]

            print(f"ID: {id_persona}")
            print(f"Nombre completo: {nombre_completo}")
            print(f"Carnet de identidad: {carnet_identidad}")
            print(f"Tipo de persona: {tipo_persona}")
            print(f"Acreditación para descargar materiales: {acreditacion}")
            print("------------------------------------")

    else:
        print("No hay personas registradas en el sistema.")
    
    input("Presione Enter para volver al menú anterior...")



def mostrar_solicitudes(cursor):
    os.system("cls")
    cursor.execute("""
        SELECT p.nombre_completo, b.nombre_libro
        FROM Personas p
        INNER JOIN Solicitudes s ON p.id = s.id_persona
        INNER JOIN Bibliografias b ON b.id = s.id_bibliografia
    """)
    solicitudes = cursor.fetchall()

    if not solicitudes:
        print("No hay solicitudes registradas.")
        input("Presione Enter para volver al menú anterior...")
        return

    print("Solicitudes Registradas:")
    for solicitud in solicitudes:
        nombre_persona, nombre_libro = solicitud
        print(f"Persona: {nombre_persona}")
        print(f"Libro: {nombre_libro}")
        print("------------------------------")
        
        input("Presione Enter para volver al menú anterior...")



def agregar_eliminar_temas(cursor):
    os.system("cls")
    print("1. Agregar tema")
    print("2. Eliminar tema")
    opcion = int(input("Ingrese una opción: "))

    if opcion == 1:
        os.system("cls")
        tema = input("Ingrese el nombre del tema: ")
        insertar_tema(cursor, tema)
        print("Tema agregado exitosamente.")
        input("Presione Enter para continuar...")
        
    elif opcion == 2:
        os.system("cls")
        mostrar_temas(cursor)
        id_tema = int(input("Ingrese el ID del tema a eliminar: "))
        eliminar_tema(cursor, id_tema)
        print("Tema eliminado exitosamente.")
        input("Presione Enter para continuar...")

    else:
        print("Opción inválida.")
        input("Presione Enter para reintentar...")


def mostrar_temas(cursor):
    os.system("cls")
    cursor.execute("""
        SELECT id, tema FROM Temas
    """)

    temas = cursor.fetchall()

    print("Temas:")
    for tema in temas:
        print(f"ID: {tema[0]} | Tema: {tema[1]}")

def mostrar_bibliografias(cursor):
    cursor.execute("""
        SELECT b.nombre_libro, b.subtema, b.fecha_publicacion, b.idioma, b.cantidad_paginas, b.tipo_bibliografia
        FROM Bibliografias b
    """)

    bibliografias = cursor.fetchall()
    
    if not bibliografias:
        print("No hay bibliografías registradas.")
        input("Presione Enter para volver al menú anterior...")

        return

    print("Bibliografías:")
    for bibliografia in bibliografias:
        print(f"Nombre del libro: {bibliografia[0]} | Subtema: {bibliografia[1]} | Fecha de publicación: {bibliografia[2]} | "
              f"Idioma: {bibliografia[3]} | Cantidad de páginas: {bibliografia[4]} | Tipo de bibliografía: {bibliografia[5]}")
        input("Presione Enter para volver al menú anterior...")

def mostrar_temas_y_bibliografias(cursor):
    os.system("cls")
    cursor.execute("""
        SELECT Temas.id, Temas.tema, Bibliografias.subtema, Bibliografias.nombre_libro, Bibliografias.autor, Bibliografias.cantidad_paginas, Bibliografias.fecha_publicacion, Bibliografias.estanteria, Bibliografias.tipo_bibliografia, Bibliografias.id
        FROM Temas
        LEFT JOIN Bibliografias ON Bibliografias.id_tema = Temas.id
    """)

    temas_bibliografias = cursor.fetchall()

    if temas_bibliografias:
        temas = {}
        for tema_bibliografia in temas_bibliografias:
            tema_id, tema, subtema, nombre_libro, autor, paginas, fecha_publicacion, estanteria, tipo_bibliografia, libro_id = tema_bibliografia
            if tema_id not in temas:
                temas[tema_id] = {
                    'tema': tema,
                    'subtemas': [],
                    'bibliografias': []
                }
            if subtema is not None:
                temas[tema_id]['subtemas'].append(subtema)
            if nombre_libro is not None:
                temas[tema_id]['bibliografias'].append({
                    'id': libro_id,
                    'nombre_libro': nombre_libro,
                    'autor': autor,
                    'paginas': paginas,
                    'fecha_publicacion': fecha_publicacion,
                    'estanteria': estanteria,
                    'tipo_bibliografia': tipo_bibliografia,
                    'subtema': subtema
                })

        for tema_id, tema_info in temas.items():
            print(f"Tema ID: {tema_id}")
            print(f"Tema: {tema_info['tema']}")
            if tema_info['bibliografias']:
                print("Bibliografías:")
                print("==============")
                for bibliografia in tema_info['bibliografias']:
                    print(f"ID: {bibliografia['id']}")
                    if bibliografia['subtema']:
                        print(f"Subtema: {bibliografia['subtema']}")
                    print(f"Tipo de bibliografía: {bibliografia['tipo_bibliografia']}")
                    print(f"Nombre del libro: {bibliografia['nombre_libro']}") 
                    print(f"Autor: {bibliografia['autor']}")
                    print(f"Año: {bibliografia['fecha_publicacion'].year}")
                    print(f"Páginas: {bibliografia['paginas']}")
                    print(f"Estantería: {bibliografia['estanteria']}")
                    print("------------------------------------")
            else:
                print("No hay bibliografías registradas para este tema.")
            print("------------------------------------")
    else:
        print("No hay temas registrados en el sistema.")

    input("Presione Enter para volver al menú anterior...")


def ejecutar_programa():
    
    conn = establecer_conexion()
    cursor = conn.cursor()
    crear_tablas(cursor)

    while True:
        os.system("cls")
        print("Cargando menú principal...")
        time.sleep(1)
        os.system("cls")
        print("====== SISTEMA DE GESTIÓN BIBLIOGRÁFICA ======")
        print("1. Registrar nueva persona")
        print("2. Listar personas registradas")
        print("3. Asignar bibliografía a una persona registrada")
        print("4. Mostrar datos de personas y bibliografías asignadas")
        print("5. Agregar o eliminar temas")
        print("6. Agregar bibliografía")
        print("7. Consultar temas y bibliografías")
        print("8. Finalizar programa")
        opcion = int(input("Ingrese una opción: "))

        if opcion == 1:
            registrar_persona(cursor)
        elif opcion == 2:
            mostrar_personas_registradas(cursor)
        elif opcion == 3:
            asignar_bibliografia(cursor)
        elif opcion == 4:
            mostrar_solicitudes(cursor)
        elif opcion == 5:
            agregar_eliminar_temas(cursor)
        elif opcion == 6:
            insertar_bibliografia(cursor)
        elif opcion == 7:
            mostrar_temas_y_bibliografias(cursor)
            
        elif opcion == 8:
            os.system("cls")
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, vuelva a intentarlo")
            
            input("Presione Enter para reintentar...")

    cursor.close()
    conn.close()

ejecutar_programa()
