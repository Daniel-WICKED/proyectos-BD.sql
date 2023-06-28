import psycopg2
import os

def establecer_conexion():
    os.system("cls")
    while True:
        try:
            conn = psycopg2.connect(
                host=("localhost"),
                database=("clinica"),
                user=("postgres"),
                password=("password")
            )
            
            return conn
        except psycopg2.Error as e:
            print("Error de conexión con la base de datos:", e)


def crear_tablas(cursor):
   
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pacientes (
                codigo SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                apellidos VARCHAR(100),
                direccion VARCHAR(100),
                poblacion VARCHAR(100),
                provincia VARCHAR(100),
                codigo_postal VARCHAR(10),
                telefono VARCHAR(20),
                fecha_nacimiento DATE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Medicos (
                codigo SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                apellidos VARCHAR(100),
                telefono VARCHAR(20),
                especialidad VARCHAR(100)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ingresos (
                codigo_ingreso SERIAL PRIMARY KEY,
                codigo_paciente INTEGER REFERENCES Pacientes(codigo),
                codigo_medico INTEGER REFERENCES Medicos(codigo),
                numero_habitacion INTEGER,
                numero_cama INTEGER,
                fecha_ingreso DATE
            )
        """)
        
        
        print("El programa ha iniciado con éxito.")       
        input("Pulse ENTER para acceder al Menú Principal")
       
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)
        os.system("pause")

def insertar_paciente(cursor):
    os.system("cls")
    try:
        nombre = input("Ingrese el nombre del paciente: ")
        apellidos = input("Ingrese los apellidos del paciente: ")
        direccion = input("Ingrese la dirección del paciente: ")
        poblacion = input("Ingrese la población del paciente: ")
        provincia = input("Ingrese la provincia del paciente: ")
        codigo_postal = input("Ingrese el código postal del paciente: ")
        telefono = input("Ingrese el teléfono del paciente: ")
        fecha_nacimiento = input("Ingrese la fecha de nacimiento del paciente (YYYY-MM-DD): ")
        cursor.execute("""
            INSERT INTO Pacientes (nombre, apellidos, direccion, poblacion, provincia, codigo_postal, telefono, fecha_nacimiento)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellidos, direccion, poblacion, provincia, codigo_postal, telefono, fecha_nacimiento))
        cursor.connection.commit()
        print("Paciente insertado correctamente.")
    except psycopg2.Error as e:
        print("Error:")
    input("pulse ENTER para continuar")     

def insertar_medico(cursor):
    os.system("cls")
    try:
        nombre = input("Ingrese el nombre del médico: ")
        apellido = input("Ingrese el apellido del médico: ")
        telefono = input("Ingrese el teléfono del médico: ")
        especialidad = input("Ingrese la especialidad del médico: ")
        cursor.execute("""
            INSERT INTO Medicos (nombre, apellidos, telefono, especialidad)
            VALUES (%s, %s, %s, %s)
        """, (nombre, apellido, telefono, especialidad))
        cursor.connection.commit()
        print("Médico insertado correctamente.")
        
    except psycopg2.Error as e:
        print("Error:")
    input("pulse ENTER para continuar")   

def insertar_ingreso(cursor):
    os.system("cls")
    try:
        codigo_paciente = input("Ingrese el código del paciente: ")
        codigo_medico = input("Ingrese el código del médico: ")
        numero_habitacion = input("Ingrese el número de habitación: ")
        numero_cama = input("Ingrese el número de cama: ")
        fecha_ingreso = input("Ingrese la fecha de ingreso (YYYY-MM-DD): ")
        cursor.execute("""
            INSERT INTO Ingresos (codigo_paciente, codigo_medico, numero_habitacion, numero_cama, fecha_ingreso)
            VALUES (%s, %s, %s, %s, %s)
        """, (codigo_paciente, codigo_medico, numero_habitacion, numero_cama, fecha_ingreso))
        cursor.connection.commit()
        print("Ingreso registrado correctamente.")
    except psycopg2.Error as e:
        print("Error:")
    input("pulse ENTER para continuar")

def mostrar_pacientes(cursor):
    os.system("cls")
    cursor.execute("SELECT * FROM Pacientes")
    pacientes = cursor.fetchall()

    if len(pacientes) == 0:
        print("No hay pacientes registrados.")
    else:
        print("Lista de pacientes:")
        for paciente in pacientes:
            print("Código:", paciente[0])
            print("Nombre:", paciente[1])
            print("Apellidos:", paciente[2])
            print("Dirección:", paciente[3])
            print("Población:", paciente[4])
            print("Provincia:", paciente[5])
            print("Código Postal:", paciente[6])
            print("Teléfono:", paciente[7])
            print("Fecha de Nacimiento:", paciente[8])
            print("---------------------------")
    input ("Presione Enter para volver...")

def mostrar_medicos(cursor):
    os.system("cls")
    cursor.execute("SELECT * FROM Medicos")
    medicos = cursor.fetchall()

    if len(medicos) == 0:
        print("No hay médicos registrados.")
    else:
        print("Lista de médicos:")
        for medico in medicos:
            print("Código:", medico[0])
            print("Nombre:", medico[1])
            print("Apellido:", medico[2])
            print("Teléfono:", medico[3])
            print("Especialidad:", medico[4])
            print("---------------------------")
    input ("Presione Enter para volver...")

def mostrar_ingresos(cursor):
    os.system("cls")
    cursor.execute("SELECT * FROM Ingresos")
    ingresos = cursor.fetchall()

    if len(ingresos) == 0:
        print("No hay ingresos registrados.")
    else:
        print("Lista de ingresos:")
        for ingreso in ingresos:
            print("Código de ingreso:", ingreso[0])
            print("Código de paciente:", ingreso[1])
            print("Código de médico:", ingreso[2])
            print("Número de habitación:", ingreso[3])
            print("Número de cama:", ingreso[4])
            print("Fecha de ingreso:", ingreso[5])
            print("---------------------------")
    input ("Presione Enter para volver...")

def buscar_paciente(cursor):
    os.system("cls")
    codigo = input("Ingrese el código del paciente a buscar: ")
    cursor.execute("SELECT * FROM Pacientes WHERE codigo = %s", (codigo,))
    paciente = cursor.fetchone()

    if paciente is None:
        print("No se encontró ningún paciente con ese código.")
    else:
        print("Información del paciente:")
        print("Código:", paciente[0])
        print("Nombre:", paciente[1])
        print("Apellidos:", paciente[2])
        print("Dirección:", paciente[3])
        print("Población:", paciente[4])
        print("Provincia:", paciente[5])
        print("Código Postal:", paciente[6])
        print("Teléfono:", paciente[7])
        print("Fecha de Nacimiento:", paciente[8])
    input ("Presione Enter para volver...")

def buscar_medico(cursor):
    os.system("cls")
    codigo = input("Ingrese el código del médico a buscar: ")
    cursor.execute("SELECT * FROM Medicos WHERE codigo = %s", (codigo,))
    medico = cursor.fetchone()

    if medico is None:
        print("No se encontró ningún médico con ese código.")
    else:
        print("Información del médico:")
        print("Código:", medico[0])
        print("Nombre:", medico[1])
        print("Apellido:", medico[2])
        print("Teléfono:", medico[3])
        print("Especialidad:", medico[4])
    input ("Presione Enter para volver...")

def buscar_ingreso(cursor):
    os.system("cls")
    codigo = input("Ingrese el código del ingreso a buscar: ")
    cursor.execute("SELECT * FROM Ingresos WHERE codigo_ingreso = %s", (codigo,))
    ingreso = cursor.fetchone()

    if ingreso is None:
        print("No se encontró ningún ingreso con ese código.")
    else:
        print("Información del ingreso:")
        print("Código de ingreso:", ingreso[0])
        print("Código de paciente:", ingreso[1])
        print("Código de médico:", ingreso[2])
        print("Número de habitación:", ingreso[3])
        print("Número de cama:", ingreso[4])
        print("Fecha de ingreso:", ingreso[5])
    input ("Presione Enter para volver...")

def eliminar_paciente(cursor):
    os.system("cls")
    codigo_paciente = input("Ingrese el código del paciente que desea eliminar: ")
    cursor.execute("DELETE FROM Pacientes WHERE codigo = %s", (codigo_paciente,))
    cursor.connection.commit()
    print("Paciente eliminado correctamente.")
    input ("Presione Enter para volver...")
    
def eliminar_medico(cursor):
    os.system("cls")
    codigo_medico = input("Ingrese el código del médico que desea eliminar: ")
    cursor.execute("DELETE FROM Medicos WHERE codigo = %s", (codigo_medico,))
    cursor.connection.commit()
    print("Médico eliminado correctamente.")
    input ("Presione Enter para volver...")
    
def eliminar_ingreso(cursor):
    os.system("cls")
    codigo_ingreso = input("Ingrese el código del ingreso que desea eliminar: ")
    cursor.execute("DELETE FROM Ingresos WHERE codigo_ingreso = %s", (codigo_ingreso,))
    cursor.connection.commit()
    print("Ingreso eliminado correctamente.")
    input ("Presione Enter para volver...")
def eliminar_todo(cursor):
    os.system("cls")
    confirmacion = input("Esta acción eliminará todos los datos de la base de datos. ¿Está seguro? (S/N): ")

    if confirmacion.upper() == "S":
        cursor.execute("DELETE FROM Ingresos")
        cursor.execute("DELETE FROM Pacientes")
        cursor.execute("DELETE FROM Medicos")
        cursor.connection.commit()
        print("Todos los datos han sido eliminados correctamente.")
    else:
        print("La eliminación de datos ha sido cancelada.")
    input ("Presione Enter para volver...")
    
def mostrar_menu_principal():
    os.system("cls")
    print("       ======================== Clínica San Patrás ======================")
    print(" _________________________________________________________________________________")
    print("|                                 MENÚ PRINCIPAL                                  |")
    print("|_________________________________________________________________________________|")
    print("|1. Pacientes                                                                     |")
    print("|2. Médicos                                                                       |")
    print("|3. Ingresos                                                                      |")
    print("|4. Eliminar todos los datos almacenados                                          |")
    print("|                                                                                 |")
    print("|0. Salir del programa                                                            |")
    print("|_________________________________________________________________________________|")
    print()

def mostrar_menu_pacientes():
    os.system("cls")
    print("       ======================== Clínica San Patrás ======================")
    print(" __________________________________________________________________________________")
    print("|                                 MENÚ PACIENTES                                   |")
    print("|__________________________________________________________________________________|")
    print("|1. Insertar paciente                                                              |")
    print("|2. Mostrar pacientes                                                              |")
    print("|3. Buscar paciente                                                                |")
    print("|4. Eliminar paciente                                                              |")
    print("|                                                                                  |")
    print("|0. Volver al menú principal                                                       |")
    print("|__________________________________________________________________________________|")
    print()

def mostrar_menu_medicos():
    os.system("cls")
    print("       ======================== Clínica San Patrás ======================")
    print(" __________________________________________________________________________________")
    print("|                                   MENÚ MÉDICOS                                   |")
    print("|__________________________________________________________________________________|")
    print("|1. Insertar médico                                                                |")
    print("|2. Mostrar médicos                                                                |")
    print("|3. Buscar médico                                                                  |")
    print("|4. Eliminar médico                                                                |")
    print("|                                                                                  |")
    print("|0. Volver al menú principal                                                       |")
    print("|__________________________________________________________________________________|")
    print()

def mostrar_menu_ingresos():
    os.system("cls")
    print("       ======================== Clínica San Patrás ======================")
    print(" __________________________________________________________________________________")
    print("|                                 MENÚ INGRESOS                                    |")
    print("|__________________________________________________________________________________|")
    print("|1. Insertar ingreso                                                               |")
    print("|2. Mostrar ingresos                                                               |")
    print("|3. Buscar ingreso                                                                 |")
    print("|4. Eliminar ingreso                                                               |")
    print("|                                                                                  |")
    print("|0. Volver al menú principal                                                       |")
    print("|__________________________________________________________________________________|")
    print()

def main():
    conexion = establecer_conexion()

    if conexion is None:
        print("No se pudo establecer conexión con la base de datos.")
        return

    cursor = conexion.cursor()
    crear_tablas(cursor)

    while True:
        mostrar_menu_principal()
        opcion_principal = input("Ingrese una opción: ")

        if opcion_principal == "1":
            while True:
                mostrar_menu_pacientes()
                opcion_pacientes = input("Ingrese una opción: ")

                if opcion_pacientes == "1":
                    insertar_paciente(cursor)
                elif opcion_pacientes == "2":
                    mostrar_pacientes(cursor)
                elif opcion_pacientes == "3":
                    buscar_paciente(cursor)
                elif opcion_pacientes == "4":
                    eliminar_paciente(cursor)
                elif opcion_pacientes == "0":
                    break
                else:
                    print("Opción inválida. Por favor, ingrese una opción válida.")

        elif opcion_principal == "2":
            while True:
                mostrar_menu_medicos()
                opcion_medicos = input("Ingrese una opción: ")

                if opcion_medicos == "1":
                    insertar_medico(cursor)
                elif opcion_medicos == "2":
                    mostrar_medicos(cursor)
                elif opcion_medicos == "3":
                    buscar_medico(cursor)
                elif opcion_medicos == "4":
                    eliminar_medico(cursor)
                elif opcion_medicos == "0":
                    break
                else:
                    print("Opción inválida. Por favor, ingrese una opción válida.")

        elif opcion_principal == "3":
            while True:
                mostrar_menu_ingresos()
                opcion_ingresos = input("Ingrese una opción: ")

                if opcion_ingresos == "1":
                    insertar_ingreso(cursor)
                elif opcion_ingresos == "2":
                    mostrar_ingresos(cursor)
                elif opcion_ingresos == "3":
                    buscar_ingreso(cursor)
                elif opcion_ingresos == "4":
                    eliminar_ingreso(cursor)
                elif opcion_ingresos == "0":
                    break
                else:
                    print("Opción inválida. Por favor, ingrese una opción válida.")

        elif opcion_principal == "4":
            eliminar_todo(cursor)

        elif opcion_principal == "0":
            break

        else:
            print("Opción inválida. Por favor, ingrese una opción válida.")

    cursor.close()
    conexion.close()
    print("Saliendo del programa...")


if __name__ == '__main__':
    main()

