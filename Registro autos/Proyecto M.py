import psycopg2
import os
import time

def establecer_conexion():
    limpiar_consola()
    while True:
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="reg_autos",
                user="postgres",
                password="password"
            )

            print("Base de datos conectada..")
            time.sleep(1)    
            return conn
            
        except psycopg2.Error as e:
            print("Error de conexión con la base de datos:", e)

def crear_tablas(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Personas (
                dni VARCHAR(10) PRIMARY KEY,
                nombre VARCHAR(100),
                apellidos VARCHAR(100),
                direccion VARCHAR(100),
                poblacion VARCHAR(100),
                telefono VARCHAR(20)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Vehiculos (
                matricula VARCHAR(10) PRIMARY KEY,
                marca VARCHAR(100),
                modelo VARCHAR(100)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Accidentes (
                referencia SERIAL PRIMARY KEY,
                fecha DATE,
                lugar VARCHAR(100),
                hora TIME
            )
        """)


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Accidentes_Personas_Vehiculos (
                accidente_referencia INTEGER REFERENCES Accidentes(referencia),
                persona_dni VARCHAR(10) REFERENCES Personas(dni),
                vehiculo_matricula VARCHAR(10) REFERENCES Vehiculos(matricula),
                PRIMARY KEY (accidente_referencia, persona_dni, vehiculo_matricula)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Multas (
                referencia SERIAL PRIMARY KEY,
                fecha DATE,
                hora TIME,
                lugar_infraccion VARCHAR(100),
                importe DECIMAL(10, 2),
                persona_dni VARCHAR(10) REFERENCES Personas(dni),
                vehiculo_matricula VARCHAR(10) REFERENCES Vehiculos(matricula)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Personas_Vehiculos (
                persona_dni VARCHAR(10) REFERENCES Personas(dni),
                vehiculo_matricula VARCHAR(10) REFERENCES Vehiculos(matricula),
                propietario BOOLEAN,
                PRIMARY KEY (persona_dni, vehiculo_matricula)
            )
        """)

        print("Tablas comprobadas correctamente. El programa se iniciará en breve...")
        time.sleep(2)

    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)

def limpiar_consola():
    os.system("cls")

def insertar_persona(cursor):
    limpiar_consola()
    while True:
        try:
            dni = input("Ingrese el DNI de la persona: ")
            nombre = input("Ingrese el nombre de la persona: ")
            apellidos = input("Ingrese los apellidos de la persona: ")
            direccion = input("Ingrese la dirección de la persona: ")
            poblacion = input("Ingrese la población de la persona: ")
            telefono = input("Ingrese el teléfono de la persona: ")

            cursor.execute("""
                INSERT INTO Personas (dni, nombre, apellidos, direccion, poblacion, telefono)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (dni, nombre, apellidos, direccion, poblacion, telefono))
            cursor.connection.commit()
            print("Persona insertada correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al insertar la persona:", e)
            opcion = input("¿Desea reintentar (S/N)? ")
            if opcion.upper() != "S":
                break

def insertar_vehiculo(cursor):
    limpiar_consola()
    while True:
        try:
            matricula = input("Ingrese la matrícula del vehículo: ")
            marca = input("Ingrese la marca del vehículo: ")
            modelo = input("Ingrese el modelo del vehículo: ")

            cursor.execute("""
                INSERT INTO Vehiculos (matricula, marca, modelo)
                VALUES (%s, %s, %s)
            """, (matricula, marca, modelo))
            cursor.connection.commit()
            print("Vehículo insertado correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al insertar el vehículo:", e)
            opcion = input("¿Desea reintentar (S/N)? ")
            if opcion.upper() != "S":
                break

def asignar_propietarios(cursor):
    limpiar_consola()
    while True:
        try:
            dni = input("Ingrese el DNI de la persona: ")
            matricula = input("Ingrese la matrícula del vehículo: ")

            cursor.execute("""
                INSERT INTO Personas_Vehiculos (persona_dni, vehiculo_matricula)
                VALUES (%s, %s)
            """, (dni, matricula))
            cursor.connection.commit()
            print("Propietario asignado correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al asignar el propietario:", e)
            opcion = input("¿Desea reintentar (S/N)? ")
            if opcion.upper() != "S":
                break

def registrar_accidente(cursor):
    limpiar_consola()
    while True:
        try:
            fecha = input("Ingrese la fecha del accidente (YYYY-MM-DD): ")
            lugar = input("Ingrese el lugar del accidente: ")
            hora = input("Ingrese la hora del accidente (HH:MM): ")

            cursor.execute("""
                INSERT INTO Accidentes (fecha, lugar, hora)
                VALUES (%s, %s, %s)
            """, (fecha, lugar, hora))
            cursor.connection.commit()
            print("Accidente registrado correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al registrar el accidente:", e)
            opcion = input("¿Desea reintentar (S/N)? ")
            if opcion.upper() != "S":
                break

def registrar_accidente_personas_vehiculos(cursor):
    limpiar_consola()
    while True:
        try:
            accidente_referencia = int(input("Ingrese la referencia del accidente: "))
            dni = input("Ingrese el DNI de la persona involucrada: ")
            matricula = input("Ingrese la matrícula del vehículo involucrado: ")

            cursor.execute("""
                INSERT INTO Accidentes_Personas_Vehiculos (accidente_referencia, persona_dni, vehiculo_matricula)
                VALUES (%s, %s, %s)
            """, (accidente_referencia, dni, matricula))
            cursor.connection.commit()
            print("Registro de persona y vehículo en accidente completado correctamente.")

            break
        except (psycopg2.Error, ValueError) as e:
            print("Error al registrar persona y vehículo en accidente:", e)
            opcion = input("¿Desea reintentar (S/N)? ")
            if opcion.upper() != "S":
                break
        input("Presione ENTER para continuar")

def emitir_multa(cursor):
    limpiar_consola()
    while True:
        try:
            fecha = input("Ingrese la fecha de la multa (YYYY-MM-DD): ")
            hora = input("Ingrese la hora de la multa (HH:MM): ")
            lugar_infraccion = input("Ingrese el lugar de la infracción: ")
            importe = float(input("Ingrese el importe de la multa (CUP): "))
            dni = input("Ingrese el DNI del conductor infractor: ")
            matricula = input("Ingrese la matrícula del vehículo involucrado: ")

            cursor.execute("""
                INSERT INTO Multas (fecha, hora, lugar_infraccion, importe, persona_dni, vehiculo_matricula)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (fecha, hora, lugar_infraccion, importe, dni, matricula))
            cursor.connection.commit()
            print("Multa emitida correctamente.")
            input("Presione ENTER para continuar")
            break
        except (psycopg2.Error, ValueError) as e:
            print("Error al emitir la multa:", e)
            opcion = input("¿Desea reintentar (S/N)? ")            
            if opcion.upper() != "S":
                break

def consultar_multas(cursor):
    limpiar_consola()
    try:
        dni = input("Ingrese el DNI del conductor para consultar sus multas: ")

        cursor.execute("""
            SELECT referencia, fecha, hora, lugar_infraccion, importe
            FROM Multas
            WHERE persona_dni = %s
        """, (dni,))
        multas = cursor.fetchall()

        if len(multas) > 0:
            print("Multas encontradas:")
            for multa in multas:
                print("Referencia:", multa[0])
                print("Fecha:", multa[1])
                print("Hora:", multa[2])
                print("Lugar de infracción:", multa[3])
                print("Importe:", multa[4])
                print("---------------------------")
        else:
            print("No se encontraron multas para el conductor con DNI", dni)

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al consultar las multas:", e)
        
def visualizar_datos(cursor):
    limpiar_consola()
    while True:
        limpiar_consola()
        print("----- VISUALIZAR DATOS -----")
        print("1. Visualizar personas")
        print("2. Visualizar vehículos")
        print("3. Visualizar accidentes")
        print("0. Volver al menú principal")

        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            visualizar_personas(cursor)
        elif opcion == "2":
            visualizar_vehiculos(cursor)
        elif opcion == "3":
            visualizar_accidentes(cursor)
        elif opcion == "0":
            break
        else:
            input("Opción inválida. Presione ENTER para reintentar")

def visualizar_personas(cursor):
    limpiar_consola()
    try:
        cursor.execute("""
            SELECT p.dni, p.nombre, p.apellidos, p.direccion, p.poblacion, p.telefono, v.matricula
            FROM Personas p
            LEFT JOIN Personas_Vehiculos pv ON p.dni = pv.persona_dni
            LEFT JOIN Vehiculos v ON pv.vehiculo_matricula = v.matricula
            ORDER BY p.dni
        """)

        personas = cursor.fetchall()

        for persona in personas:
            dni = persona[0]
            nombre = persona[1]
            apellidos = persona[2]
            direccion = persona[3]
            poblacion = persona[4]
            telefono = persona[5]
            matricula = persona[6]

            print("DNI:", dni)
            print("Nombre:", nombre)
            print("Apellidos:", apellidos)
            print("Dirección:", direccion)
            print("Población:", poblacion)
            print("Teléfono:", telefono)
            print("Vehículo(s) propietario(s):")

            if matricula is not None:
                print("- Matrícula:", matricula)
            else:
                print("Ningún vehículo registrado")

            print()

    except psycopg2.Error as e:
        print("Error al visualizar las personas:", e)
    
    input("Presione Enter para volver...")
    
def visualizar_vehiculos(cursor):
    limpiar_consola()
    try:
        cursor.execute("""
            SELECT v.matricula, v.marca, v.modelo, p.dni, p.nombre
            FROM Vehiculos v
            LEFT JOIN Personas_Vehiculos pv ON v.matricula = pv.vehiculo_matricula
            LEFT JOIN Personas p ON pv.persona_dni = p.dni
            ORDER BY v.matricula
        """)

        vehiculos = cursor.fetchall()
        vehiculo_actual = None

        for vehiculo in vehiculos:
            if vehiculo_actual is None or vehiculo_actual[0] != vehiculo[0]:
                if vehiculo_actual is not None:
                    print() 
                matricula = vehiculo[0]
                marca = vehiculo[1]
                modelo = vehiculo[2]
                print("Matrícula:", matricula)
                print("Marca:", marca)
                print("Modelo:", modelo)
                print("Propietario(s):")
                vehiculo_actual = vehiculo

            dni = vehiculo[3]
            nombre = vehiculo[4]

            if dni is not None:
                print("- DNI:", dni)
                print("  Nombre:", nombre)
            else:
                print("Ningún propietario registrado")

        if vehiculo_actual is None:
            print("No hay vehículos registrados")

    except psycopg2.Error as e:
        print("Error al visualizar los vehículos:", e)
    
    input("Presione Enter para volver...")


def visualizar_accidentes(cursor):
    limpiar_consola()
    try:
        cursor.execute("""
            SELECT a.referencia, a.fecha, a.lugar, a.hora, p.dni, p.nombre, v.matricula, v.marca, v.modelo
            FROM Accidentes a
            LEFT JOIN Accidentes_Personas_Vehiculos apv ON a.referencia = apv.accidente_referencia
            LEFT JOIN Personas p ON apv.persona_dni = p.dni
            LEFT JOIN Vehiculos v ON apv.vehiculo_matricula = v.matricula
            ORDER BY a.referencia
        """)

        accidentes = cursor.fetchall()
        accidente_actual = None

        if len(accidentes) > 0:
            print("Accidentes registrados:")
            for accidente in accidentes:
                if accidente_actual is None or accidente_actual[0] != accidente[0]:
                    if accidente_actual is not None:
                        print()  # Línea en blanco entre accidentes
                    referencia = accidente[0]
                    fecha = accidente[1]
                    lugar = accidente[2]
                    hora = accidente[3]
                    print("Referencia:", referencia)
                    print("Fecha:", fecha)
                    print("Lugar:", lugar)
                    print("Hora:", hora)
                    print("Personas y vehículos involucrados:")
                    print("---------------------------")
                    accidente_actual = accidente

                dni = accidente[4]
                nombre = accidente[5]
                matricula = accidente[6]
                marca = accidente[7]
                modelo = accidente[8]

                print("- DNI:", dni)
                print("  Nombre:", nombre)
                print("- Vehículo:")
                print("  Matrícula:", matricula)
                print("  Marca:", marca)
                print("  Modelo:", modelo)

        else:
            print("No se encontraron accidentes registrados")

    except psycopg2.Error as e:
        print("Error al consultar los accidentes:", e)

    input("Presione ENTER para volver")


def borrar_dato_individual(cursor):
    limpiar_consola()
    while True:
        limpiar_consola()
        print("----- BORRAR DATO INDIVIDUAL -----")
        print("1. Borrar persona por DNI")
        print("2. Borrar vehículo por matrícula")
        print("3. Eliminar propietario(s)")
        print("4. Borrar accidente por referencia")
        print("5. Borrar multa por referencia")
        print("0. Volver al menú principal")

        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            borrar_persona(cursor)
        elif opcion == "2":
            borrar_vehiculo(cursor)
        elif opcion == "3":
           eliminar_propietarios(cursor)
        elif opcion == "4":
            borrar_accidente(cursor)
        elif opcion == "5":
            borrar_multa(cursor)
        elif opcion == "0":
            break
        else:
            input("Opción inválida. Presione ENTER para reintentar")

def borrar_persona(cursor):
    limpiar_consola()
    try:
        dni = input("Ingrese el DNI de la persona que desea borrar: ")
        cursor.execute("DELETE FROM Personas WHERE dni = %s", (dni,))
        cursor.connection.commit()
        print("Persona borrada correctamente.")
        input("Presione ENTER para volver")
    except psycopg2.Error as e:
        print("Error al borrar la persona:", e)

def borrar_vehiculo(cursor):
    limpiar_consola()
    try:
        matricula = input("Ingrese la matrícula del vehículo que desea borrar: ")
        cursor.execute("DELETE FROM Vehiculos WHERE matricula = %s", (matricula,))
        cursor.connection.commit()
        print("Vehículo borrado correctamente.")        
    except psycopg2.Error as e:
        print("Error al borrar el vehículo:", e)
    
    input("Presione ENTER para volver")
 
def eliminar_propietarios(cursor):
    limpiar_consola()
    matricula = input("Ingrese la matrícula del vehículo: ")
    try:    
        cursor.execute("SELECT * FROM Vehiculos WHERE matricula = %s", (matricula,))
        vehiculo = cursor.fetchone()
        if vehiculo is None:
            print("El vehículo con matrícula", matricula, "no existe.")
            return
        cursor.execute("DELETE FROM Personas_Vehiculos WHERE vehiculo_matricula = %s", (matricula,))

        print("Los propietarios asignados al vehículo con matrícula", matricula, "han sido eliminados exitosamente.")

    except psycopg2.Error as e:
        print("Error al eliminar los propietarios asignados:", e)
        
    input("Presione ENTER para volver")
  

def borrar_accidente(cursor):
    limpiar_consola()
    try:
        referencia = input("Ingrese la referencia del accidente que desea borrar: ")
        cursor.execute("DELETE FROM Accidentes WHERE referencia = %s", (referencia,))
        cursor.connection.commit()
        print("Accidente borrado correctamente.")

    except psycopg2.Error as e:
        print("Error al borrar el accidente:", e)
    
    input("Presione ENTER para volver")

def borrar_multa(cursor):
    limpiar_consola()
    try:
        referencia = input("Ingrese la referencia de la multa que desea borrar: ")
        cursor.execute("DELETE FROM Multas WHERE referencia = %s", (referencia,))
        cursor.connection.commit()
        print("Multa borrada correctamente.")

    except psycopg2.Error as e:
        print("Error al borrar la multa:", e)
        
    input("Presione ENTER para volver")
        
        
def menu_principal():
    conn = establecer_conexion()
    cursor = conn.cursor()

    crear_tablas(cursor)

    while True:
        limpiar_consola()
        print("Cargando menu principal...")
        time.sleep(1)
        limpiar_consola()
        print("----- REGISTRO DE VEHÍCULOS -----")
        print("1. Registrar persona")
        print("2. Registrar vehículo")
        print("3. Asignar Propietario(s)")
        print("4. Registrar accidente")
        print("5. Registrar persona y vehículo en accidente")
        print("6. Emitir multa")
        print("7. Consultar multas")
        print("8. Visualizar datos")
        print("9. Borrar dato individual")
        print("0. Salir")

        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            insertar_persona(cursor)
        elif opcion == "2":
            insertar_vehiculo(cursor)
        elif opcion == "3":
            asignar_propietarios(cursor)
        elif opcion == "4":
            registrar_accidente(cursor)
        elif opcion == "5":
            registrar_accidente_personas_vehiculos(cursor)
        elif opcion == "6":
            emitir_multa(cursor)
        elif opcion == "7":
            consultar_multas(cursor)
        elif opcion == "8":
            visualizar_datos(cursor)
        elif opcion == "9":
            borrar_dato_individual(cursor)
        elif opcion == "0":
            break
        else:
            input("Opción inválida. Presione ENTER para reintentar")

    cursor.close()
    conn.close()
    print("Programa finalizado.")

if __name__ == "__main__":
    menu_principal()
