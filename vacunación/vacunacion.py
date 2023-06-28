import os
import psycopg2

os.system("cls")

def conectar():
    try:
        conn = psycopg2.connect(
            database="vacunacion",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        print("Conexión exitosa a la base de datos.")
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def crear_tablas(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Personas (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                dni VARCHAR(15) NOT NULL,
                edad INTEGER NOT NULL,
                direccion VARCHAR(200) NOT NULL,
                telefono VARCHAR(15) NOT NULL,
                municipio VARCHAR(100) NOT NULL,
                provincia VARCHAR(100) NOT NULL,
                enfermedades_agravantes TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Medicos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                dni VARCHAR(15) NOT NULL,
                especialidad VARCHAR(100) NOT NULL,
                telefono VARCHAR(15) NOT NULL,
                edad INTEGER NOT NULL,
                centro_trabajo VARCHAR(100) NOT NULL,
                nombre_centro_trabajo VARCHAR(100) NOT NULL,
                municipio VARCHAR(100) NOT NULL,
                provincia VARCHAR(100) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Vacunas (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                dosis INTEGER NOT NULL,
                persona_id INTEGER REFERENCES Personas(id),
                medico_id INTEGER REFERENCES Medicos(id),
                colaboradores BOOLEAN NOT NULL,
                fecha DATE NOT NULL
            )
        """)

        cursor.connection.commit()
        print("Tablas creadas correctamente.")
        input("Pulse ENTER para continuar hacia el Menú Principal...")
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)

def insertar_persona(cursor):
    os.system("cls")
    try:
        print("----- INSERTAR PERSONA -----")
        nombre = input("Nombre: ")
        dni = input("DNI: ")
        edad = int(input("Edad: "))
        direccion = input("Dirección: ")
        telefono = input("Teléfono: ")
        municipio = input("Municipio: ")
        provincia = input("Provincia: ")
        enfermedades_agravantes = input("Enfermedades agravantes: ")

        cursor.execute("""
            INSERT INTO Personas (nombre, dni, edad, direccion, telefono, municipio, provincia, enfermedades_agravantes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, dni, edad, direccion, telefono, municipio, provincia, enfermedades_agravantes))
        cursor.connection.commit()
        print("Persona registrada correctamente.")
        
    except psycopg2.Error as e:
        print("Error al insertar la persona:", e)
    input("Presione ENTER para continuar")
    
def insertar_medico(cursor):
    os.system("cls")
    try:
        print("----- INSERTAR MÉDICO -----")
        nombre = input("Nombre: ")
        dni = input("DNI: ")
        especialidad = input("Especialidad: ")
        telefono = input("Teléfono: ")
        edad = int(input("Edad: "))
        centro_trabajo_opciones = ["consultorio", "policlínico", "hospital"]
        centro_trabajo = seleccionar_opcion("Centro de Trabajo", centro_trabajo_opciones)
        nombre_centro_trabajo = input("Nombre del Centro de Trabajo: ")
        municipio = input("Municipio: ")
        provincia = input("Provincia: ")

        cursor.execute("""
            INSERT INTO Medicos (nombre, dni, especialidad, telefono, edad, centro_trabajo, nombre_centro_trabajo, municipio, provincia)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, dni, especialidad, telefono, edad, centro_trabajo, nombre_centro_trabajo, municipio, provincia))
        cursor.connection.commit()
        print("Médico registrado correctamente.")
        
    except psycopg2.Error as e:
        print("Error al insertar el médico:", e)
    input("Presione ENTER para continuar")
def registrar_vacunacion(cursor):
    os.system("cls")
    try:
        print("----- REGISTRAR VACUNACIÓN -----")
        persona_id = int(input("ID de la Persona a vacunar: "))
        cursor.execute("SELECT edad FROM Personas WHERE id = %s", (persona_id,))
        edad = cursor.fetchone()[0]
        if edad < 19:
            print("Error: La persona debe ser mayor de 19 años para recibir la vacuna.")
            input("Presione ENTER para continuar")
            return

        vacuna_opciones = ["Soberana 02", "Soberana Plus"]
        vacuna = seleccionar_opcion("Vacuna", vacuna_opciones)

        dosis = int(input("Número de dosis: "))

        medico_id = int(input("ID del Médico que realizó la vacuna: "))
        colaboradores = input("¿Hubo colaboradores participando? (S/N): ").upper() == "S"

        fecha = input("Fecha de realización (YYYY-MM-DD): ")

        cursor.execute("""
            INSERT INTO Vacunas (nombre, dosis, persona_id, medico_id, colaboradores, fecha)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (vacuna, dosis, persona_id, medico_id, colaboradores, fecha))
        cursor.connection.commit()
        print("Vacunación registrada correctamente.")
    except psycopg2.Error as e:
        print("Error al registrar la vacunación:", e)
    input("Presione ENTER para continuar")
def mostrar_personas(cursor):
    os.system("cls")
    try:
        cursor.execute("SELECT * FROM Personas")
        personas = cursor.fetchall()
        if len(personas) > 0:
            print("----- LISTA DE PERSONAS -----")

            for persona in personas:
                print("ID:", persona[0])
                print("Nombre:", persona[1])
                print("DNI:", persona[2])
                print("Edad:", persona[3])
                print("Dirección:", persona[4])
                print("Teléfono:", persona[5])
                print("Municipio:", persona[6])
                print("Provincia:", persona[7])
                print("Enfermedades Agravantes:", persona[8])
                print("-------------------------")
        else:
            print("No hay personas registradas.")
    except psycopg2.Error as e:
        print("Error al mostrar las personas:", e)
    input("Presione ENTER para volver")
def mostrar_medicos(cursor):
    os.system("cls")
    try:
        cursor.execute("SELECT * FROM Medicos")
        medicos = cursor.fetchall()
        print("----- LISTA DE MÉDICOS -----")

        if len(medicos) > 0:
            for medico in medicos:
                print("ID:", medico[0])
                print("Nombre:", medico[1])
                print("DNI:", medico[2])
                print("Especialidad:", medico[3])
                print("Teléfono:", medico[4])
                print("Edad:", medico[5])
                print("Centro de Trabajo:", medico[6])
                print("Nombre del Centro de Trabajo:", medico[7])
                print("Municipio:", medico[8])
                print("Provincia:", medico[9])
                print("-------------------------")
        else:
            print("No hay médicos registrados.")
    except psycopg2.Error as e:
        print("Error al mostrar los médicos:", e)
    input("Presione ENTER para volver")
def mostrar_historial_vacunacion(cursor):
    os.system("cls")
    try:
        cursor.execute("""
            SELECT Vacunas.id, Personas.nombre, Medicos.nombre, Vacunas.nombre, Vacunas.dosis, Vacunas.colaboradores, Vacunas.fecha
            FROM Vacunas
            INNER JOIN Personas ON Vacunas.persona_id = Personas.id
            INNER JOIN Medicos ON Vacunas.medico_id = Medicos.id
        """)
        vacunas = cursor.fetchall()
        if len(vacunas) > 0:
            print("----- HISTORIAL DE VACUNACIÓN -----")

            for vacuna in vacunas:
                print("ID:", vacuna[0])
                print("Nombre de la Persona:", vacuna[1])
                print("Nombre del Médico:", vacuna[2])
                print("Vacuna:", vacuna[3])
                print("Número de dosis:", vacuna[4])
                print("Colaboradores Participando:", "Sí" if vacuna[5] else "No")
                print("Fecha de Realización:", vacuna[6])
                print("-------------------------")
        else:
            print("No hay registros de vacunación.")
    except psycopg2.Error as e:
        print("Error al mostrar el historial de vacunación:", e)
    input("Presione ENTER para volver")
def seleccionar_opcion(mensaje, opciones):
    opcion = None
    while opcion not in opciones:
        print(f"{mensaje}:")
        for i, opcion in enumerate(opciones, start=1):
            print(f"{i}. {opcion}")
        opcion_numero = input("Ingrese el número de opción: ")
        if opcion_numero.isdigit() and int(opcion_numero) <= len(opciones):
            opcion = opciones[int(opcion_numero)-1]
    return opcion

def menu_principal(conn, cursor):
    while True:
        os.system("cls")
        print("----- REGISTROS DE VACUNACIÓN -----")
        print("1. Insertar Persona")
        print("2. Insertar Médico")
        print("3. Registrar Vacunación")
        print("4. Mostrar Personas")
        print("5. Mostrar Médicos")
        print("6. Mostrar Historial de Vacunación")
        print("0. Salir")
        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            insertar_persona(cursor)
        elif opcion == "2":
            insertar_medico(cursor)
        elif opcion == "3":
            registrar_vacunacion(cursor)
        elif opcion == "4":
            mostrar_personas(cursor)
        elif opcion == "5":
            mostrar_medicos(cursor)
        elif opcion == "6":
            mostrar_historial_vacunacion(cursor)
        elif opcion == "0":
            break

    cursor.close()
    conn.close()

def main():
    conn = conectar()
    if conn is not None:
        cursor = conn.cursor()
        crear_tablas(cursor)
        menu_principal(conn, cursor)

if __name__ == "__main__":
    main()
