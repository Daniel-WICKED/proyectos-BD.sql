import psycopg2
import os
import time

def conectar():
    os.system("cls")
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="centro_investigacion",
            user="postgres",
            password="password"
        )
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def crear_tablas(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Campos (
                id SERIAL PRIMARY KEY,
                nombre_campo TEXT,
                profesor_encargado TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Investigadores (
                id SERIAL PRIMARY KEY,
                nombre TEXT,
                edad INTEGER,
                carnet_identidad VARCHAR(15),
                campo_accion INTEGER REFERENCES Campos(id),
                grado_academico TEXT
            )
        """)
        

        cursor.connection.commit()
        print("Programa iniciado con éxito. Cargando Menú Principal...")
        time.sleep(2)
        
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)
        os.system("pause")

def obtener_grado_academico(inicial):
    if inicial == 'm':
        return "Máster"
    elif inicial == 'd':
        return "Doctorado"
    else:
        return "Ninguno"

def insertar_campo(cursor):
    os.system("cls")
    try:
        nombre_campo = input("Nombre del campo: ")
        profesor_encargado = input("Nombre del profesor encargado: ")

        cursor.execute("""
            INSERT INTO Campos (nombre_campo, profesor_encargado)
            VALUES (%s, %s)
        """, (nombre_campo, profesor_encargado))

        cursor.connection.commit()
        print("Campo insertado correctamente.")
        input("Presione ENTER para continuar...")
    except psycopg2.Error as e:
        print("Error al insertar el campo:", e)
        os.system("pause")

def insertar_investigador(cursor):
    os.system("cls")
    try:
        print("Ingrese los siguientes datos del investigador:")
        nombre = input("Nombre: ")
        edad = int(input("Edad: "))
        carnet_identidad = input("Número de carnet de identidad: ")
        
        # Listar campos disponibles
        cursor.execute("SELECT * FROM Campos")
        campos = cursor.fetchall()
        print("Campos disponibles:")
        for campo in campos:
            print("ID:", campo[0])
            print("Nombre del campo:", campo[1])
            print("Nombre del profesor encargado:", campo[2])
            print("-----------------------------------")

        campo_id = int(input("Ingrese el ID del campo de acción: "))
        grado_academico_inicial = input("Inicial del grado académico [Máster(m), Doctorado(d), Ninguno(n)]: ")

        grado_academico = obtener_grado_academico(grado_academico_inicial)

        cursor.execute("""
            INSERT INTO Investigadores (nombre, edad, carnet_identidad, campo_accion, grado_academico)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, edad, carnet_identidad, campo_id, grado_academico))
        
        cursor.connection.commit()
        print("Datos del investigador guardados correctamente.")
        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al insertar los datos:", e)
        os.system("pause")
def listar_investigadores(cursor):
    os.system("cls")
    try:
        cursor.execute("SELECT * FROM Investigadores")
        investigadores = cursor.fetchall()

        if len(investigadores) == 0:
            print("No hay investigadores registrados.")
            
            return

        print("Lista de investigadores:")
        for investigador in investigadores:
            print("ID:", investigador[0])
            print("Nombre:", investigador[1])
            print("Edad:", investigador[2])
            print("Número de carnet de identidad:", investigador[3])
            print("Campo de acción:", investigador[4])
            print("Grado académico:", investigador[5])
            print("-----------------------------------")

        
    except psycopg2.Error as e:
        print("Error al obtener la lista de investigadores:", e)
    input("Presione ENTER para volver...")
    
def modificar_investigador(cursor):
    os.system("cls")
    try:
        #listar_investigadores(cursor)
        id_investigador = int(input("Ingrese el ID del investigador a modificar: "))

        cursor.execute("SELECT * FROM Investigadores WHERE id = %s", (id_investigador,))
        investigador = cursor.fetchone()

        if investigador is None:
            print("No se encontró ningún investigador con ese ID.")
            input("Presione ENTER para continuar")
            return

        print("Datos actuales del investigador:")
        print("ID:", investigador[0])
        print("Nombre:", investigador[1])
        print("Edad:", investigador[2])
        print("Número de carnet de identidad:", investigador[3])
        print("Campo de acción:", investigador[4])
        print("Grado académico:", investigador[5])

        print("Ingrese los nuevos datos del investigador:")
        nombre = input("Nombre: ")
        edad = int(input("Edad: "))
        carnet_identidad = input("Número de carnet de identidad: ")
        
        # Listar campos disponibles
        cursor.execute("SELECT * FROM Campos")
        campos = cursor.fetchall()
        print("Campos disponibles:")
        for campo in campos:
            print("ID:", campo[0])
            print("Nombre del campo:", campo[1])
            print("Nombre del profesor encargado:", campo[2])
            print("-----------------------------------")

        campo_id = int(input("Ingrese el ID del campo de acción: "))
        grado_academico_inicial = input("Inicial del grado académico [Máster(m), Doctorado(d), Ninguno(n)]: ")

        grado_academico = obtener_grado_academico(grado_academico_inicial)

        cursor.execute("""
            UPDATE Investigadores
            SET nombre = %s, edad = %s, carnet_identidad = %s, campo_accion = %s, grado_academico = %s
            WHERE id = %s
        """, (nombre, edad, carnet_identidad, campo_id, grado_academico, id_investigador))
        
        cursor.connection.commit()
        print("Datos del investigador modificados correctamente.")
        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al modificar los datos del investigador:", e)

def buscar_investigador(cursor):
    os.system("cls")
    try:
        nombre = input("Ingrese el nombre del investigador a buscar: ")

        cursor.execute("SELECT * FROM Investigadores WHERE nombre ILIKE %s", (f"%{nombre}%",))
        investigadores = cursor.fetchall()

        if len(investigadores) == 0:
            print("No se encontraron investigadores con ese nombre.")
            input("Presione ENTER para continuar")
            return

        print("Investigadores encontrados:")
        for investigador in investigadores:
            print("ID:", investigador[0])
            print("Nombre:", investigador[1])
            print("Edad:", investigador[2])
            print("Número de carnet de identidad:", investigador[3])
            print("Campo de acción:", investigador[4])
            print("Grado académico:", investigador[5])
            print("-----------------------------------")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al buscar el investigador:", e)

def dar_de_baja_investigador(cursor):
    os.system("cls")
    try:
        #listar_investigadores(cursor)
        
        id_investigador = int(input("Ingrese el ID del investigador a dar de baja: "))

        cursor.execute("SELECT * FROM Investigadores WHERE id = %s", (id_investigador,))
        investigador = cursor.fetchone()

        if investigador is None:
            print("No se encontró ningún investigador con ese ID.")
            input("Presione ENTER para continuar")
            return

        print("Datos del investigador a dar de baja:")
        print("ID:", investigador[0])
        print("Nombre:", investigador[1])
        print("Edad:", investigador[2])
        print("Número de carnet de identidad:", investigador[3])
        print("Campo de acción:", investigador[4])
        print("Grado académico:", investigador[5])

        confirmacion = input("¿Está seguro de que desea dar de baja a este investigador? (s/n): ")
        if confirmacion.lower() == 's':
            cursor.execute("DELETE FROM Investigadores WHERE id = %s", (id_investigador,))
            cursor.connection.commit()
            print("Investigador dado de baja correctamente.")
        else:
            print("Operación cancelada.")

        #input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al dar de baja al investigador:", e)
    input("Presione ENTER para continuar")

def menu_principal(cursor):
    while True:
        os.system("cls")
        print("------ Menú Principal ------")
        print("1. Insertar campo de investigación")
        print("2. Insertar investigador")
        print("3. Listar investigadores")
        print("4. Modificar investigador")
        print("5. Buscar investigador")
        print("6. Dar de baja investigador")
        print("7. Salir")

        opcion = input("Seleccione una opción (1-6): ")
        if opcion == '1':
            insertar_campo(cursor)
        elif opcion == '2':
            insertar_investigador(cursor)
        elif opcion == '3':
            listar_investigadores(cursor)
        elif opcion == '4':
            modificar_investigador(cursor)
        elif opcion == '5':
            buscar_investigador(cursor)
        elif opcion == '6':
            dar_de_baja_investigador(cursor)
        elif opcion == '7':
            os.system("cls")
            print("Programa finalizado...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

def main():
    conn = conectar()
    if conn is None:
        return

    cursor = conn.cursor()

    crear_tablas(cursor)
    menu_principal(cursor)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
