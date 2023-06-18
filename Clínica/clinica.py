#La clínica "San Patrás" necesita llevar el control informatizado de su gestión de pacientes y médicos. 
#De cada paciente se desea guardar el código, nombre, apellidos, dirección, población, provincia, código postal, teléfono, fecha de nacimiento 
#De cada médico se desea guardar código, nombre, apellido, teléfono y especialidad. 
#Se desea llevar el control de cada uno de los ingresos que el paciente hace en el hospital. 
#Cada ingreso que realiza el paciente queda registrado en la base de datos.
#De cada ingreso se guarda el código de ingreso( que se encontrará automáticamente cada vez que el paciente realice un ingreso) el número de habitación y cama en la que el paciente realiza el ingreso y fecha de ingreso
#Un médico puede atender varios ingresos,  pero el ingreso de un paciente solo puede ser atendido por un médico 
#Un paciente puede realizar varios ingresos en el hospital


import psycopg2
import os
import time

def conectar_bd():
    borrar_consola()
    while True:
        try:
            conn = psycopg2.connect(
                host=("localhost"),
                database=("clinica"),
                user=("postgres"),
                password=("password")
            )

            print("Conexión exitosa a la base de datos.")
            time.sleep(0.5)
            return conn
        except psycopg2.Error as e:
            print("Error al conectar a la base de datos:", e)


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
        
        
        print("Tablas creadas correctamente.")
        time.sleep(0.5)
        print("Inciando el programa...")
        time.sleep(2)
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)
        

    


def borrar_consola():
    os.system("cls")


def insertar_paciente(cursor):
    borrar_consola()
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


def insertar_medico(cursor):
    borrar_consola()
    nombre = input("Ingrese el nombre del médico: ")
    apellido = input("Ingrese el apellido del médico: ")
    telefono = input("Ingrese el teléfono del médico: ")
    especialidad = input("Ingrese la especialidad del médico: ")
    cursor.execute("""
        INSERT INTO Medicos (nombre, apellido, telefono, especialidad)
        VALUES (%s, %s, %s, %s)
    """, (nombre, apellido, telefono, especialidad))
    cursor.connection.commit()
    print("Médico insertado correctamente.")


def insertar_ingreso(cursor):
    borrar_consola()
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


def mostrar_pacientes(cursor):
    borrar_consola()
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
    borrar_consola()
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
    borrar_consola()
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
    borrar_consola()
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
    borrar_consola()
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
    borrar_consola()
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
    borrar_consola()
    codigo_paciente = input("Ingrese el código del paciente que desea eliminar: ")
    cursor.execute("DELETE FROM Pacientes WHERE codigo = %s", (codigo_paciente,))
    cursor.connection.commit()
    print("Paciente eliminado correctamente.")
    input ("Presione Enter para volver...")
    
def eliminar_medico(cursor):
    borrar_consola()
    codigo_medico = input("Ingrese el código del médico que desea eliminar: ")
    cursor.execute("DELETE FROM Medicos WHERE codigo = %s", (codigo_medico,))
    cursor.connection.commit()
    print("Médico eliminado correctamente.")
    input ("Presione Enter para volver...")
    
def eliminar_ingreso(cursor):
    borrar_consola()
    codigo_ingreso = input("Ingrese el código del ingreso que desea eliminar: ")
    cursor.execute("DELETE FROM Ingresos WHERE codigo_ingreso = %s", (codigo_ingreso,))
    cursor.connection.commit()
    print("Ingreso eliminado correctamente.")
    input ("Presione Enter para volver...")
def eliminar_todo(cursor):
    borrar_consola()
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
    
def mostrar_menu():
    borrar_consola()
    print(" =====Administración Clínica San Patrás=====")
    print(" ____________________________________________")
    print("|INSERTAR DATOS |MOSTRAR DATOS |BUSCAR DATOS |")
    print("|---------------|--------------|-------------|")
    print("|1. paciente    |4. pacientes  |7. paciente  |")
    print("|2. médico      |5. médicos    |8. médico    |")
    print("|3. ingreso     |6. ingresos   |9. ingreso   |")
    print("|_______________|______________|_____________|")
    print()
    print("ELIMINAR DATOS:")
    print("---------------")
    print("10. paciente")
    print("11. médico")
    print("12. ingreso")
    print("13. borrar todos los datos almacenados")
    print("0. Salir")

def main():
    conexion = conectar_bd()

    if conexion is None:
        print("No se pudo establecer conexión con la base de datos.")
        return

    cursor = conexion.cursor()
    crear_tablas(cursor)

    while True:
        mostrar_menu()
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            insertar_paciente(cursor)
        elif opcion == "2":
            insertar_medico(cursor)
        elif opcion == "3":
            insertar_ingreso(cursor)
        elif opcion == "4":
            mostrar_pacientes(cursor)
        elif opcion == "5":
            mostrar_medicos(cursor)
        elif opcion == "6":
            mostrar_ingresos(cursor)
        elif opcion == "7":
            buscar_paciente(cursor)
        elif opcion == "8":
            buscar_medico(cursor)
        elif opcion == "9":
            buscar_ingreso(cursor)
        elif opcion == "10":
            eliminar_paciente(cursor)
        elif opcion == "11":
            eliminar_medico(cursor)
        elif opcion == "12":
            eliminar_ingreso(cursor)
        elif opcion == "13":
            eliminar_todo(cursor)
        elif opcion == "0":
            break
        else:
            print("Opción inválida. Por favor, ingrese una opción válida.")

    cursor.close()
    conexion.close()
    borrar_consola()
    print("Saliendo del programa...")


if __name__ == '__main__':
    main()

