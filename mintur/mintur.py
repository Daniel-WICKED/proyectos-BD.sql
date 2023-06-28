import os
import psycopg2

def establecer_conexion():
    os.system("cls")
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="mintur",
            user="postgres",
            password="password"
        )
        return conn
    except psycopg2.Error as e:
        print("Error al establecer la conexión a la base de datos:", e)

def crear_tablas(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MediosTransporte (
                id SERIAL PRIMARY KEY,
                tipo VARCHAR(1) NOT NULL,
                color VARCHAR(50) NOT NULL,
                marca VARCHAR(50) NOT NULL,
                tipo_combustible VARCHAR(50) NOT NULL,
                plazas_disponibles INTEGER NOT NULL,
                disponibilidad BOOLEAN NOT NULL,
                codigo_motor VARCHAR(50),
                chapa VARCHAR(50),
                tiene_maletero BOOLEAN,
                cubicaje_motor VARCHAR(50),
                tiene_parrilla BOOLEAN,
                tiene_caja_herramientas BOOLEAN,
                tipo_frenos VARCHAR(50),
                camaras_repuesto BOOLEAN,
                cantidad_camaras INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clientes (
                id SERIAL PRIMARY KEY,
                licencia_conduccion VARCHAR(50) UNIQUE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                telefono VARCHAR(50) NOT NULL,
                direccion VARCHAR(200) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rentas (
                id SERIAL PRIMARY KEY,
                cliente_id INTEGER REFERENCES Clientes(id),
                medio_transporte_id INTEGER REFERENCES MediosTransporte(id),
                fecha_inicio DATE,
                fecha_fin DATE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BajasVehiculos (
                id INTEGER REFERENCES MediosTransporte(id),
                codigo_motor VARCHAR(50),
                tipo VARCHAR(1),
                motivo INTEGER,
                tecnico_responsable VARCHAR(100),
                fecha DATE
            )
        """)


        cursor.connection.commit()

        print("Programa cargado exitosamente.")
        input("Presione ENTER para continuar...")
        
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)
        input("Presione ENTER para reintentar...")

def insertar_medio_transporte(cursor):
    os.system("cls")
    print("----- Insertar Nuevo Medio de Transporte -----")
    while True:
        tipo = input("Ingrese el tipo de medio de transporte (A: Auto, M: Moto, B: Bicicleta): ")
        color = input("Ingrese el color del medio de transporte: ")
        marca = input("Ingrese la marca del medio de transporte: ")
        tipo_combustible = input("Ingrese el tipo de combustible del medio de transporte: ")
        plazas_disponibles = int(input("Ingrese la cantidad de plazas disponibles: "))
        disponibilidad = True

        tipo = tipo.upper()

        if tipo == "A":
            codigo_motor = input("Ingrese el código del motor del auto: ")
            chapa = input("Ingrese la chapa del auto: ")
            tiene_maletero = input("¿El auto tiene maletero? (S/N): ").upper() == "S"
            cubicaje_motor = None
            tiene_parrilla = None
            tiene_caja_herramientas = None
            tipo_frenos = None
            camaras_repuesto = None
            cantidad_camaras = None
            break
        elif tipo == "M":
            codigo_motor = None
            chapa = None
            tiene_maletero = None
            cubicaje_motor = input("Ingrese el cubicaje del motor de la moto: ")
            tiene_parrilla = input("¿La moto tiene parrilla? (S/N): ").upper() == "S"
            tiene_caja_herramientas = input("¿La moto tiene caja de herramientas? (S/N): ").upper() == "S"
            tipo_frenos = None
            camaras_repuesto = None
            cantidad_camaras = None
            break
        elif tipo == "B":
            codigo_motor = None
            chapa = None
            tiene_maletero = None
            cubicaje_motor = None
            tiene_parrilla = None
            tiene_caja_herramientas = None
            tipo_frenos = input("Ingrese el tipo de frenos de la bicicleta: ")
            camaras_repuesto = input("¿Se proporcionaron cámaras de repuesto al cliente? (S/N): ").upper() == "S"
            cantidad_camaras = int(input("Ingrese la cantidad de cámaras de repuesto: "))
            break
        else:
            print("Tipo de medio de transporte no válido. Por favor, intente nuevamente.")

    try:
        cursor.execute("""
            INSERT INTO MediosTransporte
            (tipo, color, marca, tipo_combustible, plazas_disponibles, disponibilidad, codigo_motor, chapa,
             tiene_maletero, cubicaje_motor, tiene_parrilla, tiene_caja_herramientas, tipo_frenos, camaras_repuesto, cantidad_camaras)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (tipo, color, marca, tipo_combustible, plazas_disponibles, disponibilidad, codigo_motor, chapa,
              tiene_maletero, cubicaje_motor, tiene_parrilla, tiene_caja_herramientas, tipo_frenos, camaras_repuesto, cantidad_camaras))

        cursor.connection.commit()

        print("Medio de transporte insertado correctamente.")
    except psycopg2.Error as e:
        print("Error al insertar el medio de transporte:", e)

    input("Pulse ENTER para continuar hacia el Menú Principal...")

def listar_medios_transporte(cursor):
    os.system("cls")
    print("----- Listar Medios de Transporte por Categoría -----")
    categoria = input("Ingrese la inicial de la categoría (A: Auto, M: Moto, B: Bicicleta): ")

    if categoria.upper() not in ["A", "M", "B"]:
        print("Categoría no válida.")
        input("Pulse ENTER para continuar hacia el Menú Principal...")
        return

    try:
        cursor.execute("""
            SELECT id, tipo, color, marca, tipo_combustible, plazas_disponibles, codigo_motor, chapa,
                   tiene_maletero, cubicaje_motor, tiene_parrilla, tiene_caja_herramientas, tipo_frenos, camaras_repuesto, cantidad_camaras
            FROM MediosTransporte
            WHERE tipo = %s
        """, (categoria.upper(),))

        medios_transporte = cursor.fetchall()

        if len(medios_transporte) == 0:
            print("No se encontraron medios de transporte en la categoría especificada.")
        else:
            os.system("cls")
            print("--- LISTADO DE MEDIOS DE TRANSPORTE DE LA CATEGORÍA SELECCIONADA ---")
            print()
            
            for medio_transporte in medios_transporte:
                
                id = medio_transporte[0]
                tipo = medio_transporte[1]
                color = medio_transporte[2]
                marca = medio_transporte[3]
                tipo_combustible = medio_transporte[4]
                plazas_disponibles = medio_transporte[5]

                if tipo.upper() == "A":
                    #print("--- LISTADO DE AUTOS ---")
                    codigo_motor = medio_transporte[6]
                    chapa = medio_transporte[7]
                    tiene_maletero = medio_transporte[8]
                    
                    print(f"ID: {id}")
                    print(f"Chapa: {chapa}")
                    print(f"Color: {color}")
                    print(f"Marca: {marca}")
                    print(f"Combustible: {tipo_combustible}")
                    print(f"Plazas Disponibles: {plazas_disponibles}")
                    print(f"Código Motor: {codigo_motor}")
                    print(f"Tiene Maletero: {tiene_maletero}")
                    print("---------------------------------")

                elif tipo.upper() == "M":
                    cubicaje_motor = medio_transporte[9]
                    tiene_parrilla = medio_transporte[10]
                    tiene_caja_herramientas = medio_transporte[11]
                    #print("--- LISTADO DE MOTOS ---")
                    print(f"ID: {id}")
                    print(f"Color: {color}")
                    print(f"Marca: {marca}")
                    print(f"Tiene Parrilla: {tiene_parrilla}")
                    print(f"Combustible: {tipo_combustible}")
                    print(f"Plazas Disponibles: {plazas_disponibles}")
                    print(f"Cubicaje Motor: {cubicaje_motor}")
                    print(f"Tiene Caja de Herramientas: {tiene_caja_herramientas}")
                    print("------------------------------------")

                elif tipo.upper() == "B":
                    tipo_frenos = medio_transporte[12]
                    camaras_repuesto = medio_transporte[13]
                    cantidad_camaras = medio_transporte[14]
                    #print("--- LISTADO DE BICICLETAS ---")
                    print(f"ID: {id}")
                    print(f"Color: {color}")
                    print(f"Marca: {marca}")
                    print(f"Tipo de Frenos: {tipo_frenos}")
                    print(f"Cámaras de Repuesto: {'Sí' if camaras_repuesto else 'No'}")
                    print(f"Cantidad de Cámaras: {cantidad_camaras}")
                    print("----------------------------------")
                else:
                    print("Categoría no válida.")
    except psycopg2.Error as e:
        print("Error al listar los medios de transporte:", e)

    input("Pulse ENTER para continuar hacia el Menú Principal...")

def insertar_cliente(cursor):
    os.system("cls")
    print("----- Insertar Nuevo Cliente -----")
    licencia_conduccion = input("Ingrese la licencia de conducción del cliente: ")
    nombre = input("Ingrese el nombre del cliente: ")
    telefono = input("Ingrese el número de teléfono del cliente: ")
    direccion = input("Ingrese la dirección del cliente: ")

    try:
        cursor.execute("""
            INSERT INTO Clientes
            (licencia_conduccion, nombre, telefono, direccion)
            VALUES (%s, %s, %s, %s)
        """, (licencia_conduccion, nombre, telefono, direccion))

        cursor.connection.commit()

        print("Cliente insertado correctamente.")
    except psycopg2.Error as e:
        print("Error al insertar el cliente:", e)

    input("Pulse ENTER para continuar hacia el Menú Principal...")


def efectuar_baja_vehiculo(cursor):
    os.system("cls")
    print("----- Efectuar Baja de Vehículo -----")
    codigo = input("Ingrese el código del vehículo a dar de baja: ")

    try:
        cursor.execute("""
            SELECT codigo_motor, tipo
            FROM MediosTransporte
            WHERE id = %s
        """, (codigo,))
        vehiculo = cursor.fetchone()

        if vehiculo is None:
            print("No se encontró un vehículo con el código especificado.")
            input("Pulse ENTER para continuar hacia el Menú Principal...")
            return

        codigo_motor = vehiculo[0]
        tipo = vehiculo[1]

        cursor.execute("""
            SELECT COUNT(*) FROM Rentas
            WHERE medio_transporte_id = %s AND fecha_fin > CURRENT_DATE
        """, (codigo,))
        rentas_activas = cursor.fetchone()[0]

        if rentas_activas > 0:
            print("No se puede dar de baja un vehículo que está actualmente rentado.")
            input("Pulse ENTER para continuar hacia el Menú Principal...")
            return

        print("Motivos de baja:")
        print("1. Deterioro por uso prolongado")
        print("2. Siniestro total")
        print("3. Falta de piezas de repuesto")

        motivo = input("Ingrese el número del motivo adecuado: ")
        while motivo not in ["1", "2", "3"]:
            print("Motivo no válido.")
            motivo = input("Ingrese el número del motivo adecuado: ")

        tecnico_responsable = input("Ingrese el nombre del técnico responsable de la baja: ")
        fecha = input("Ingrese la fecha de la baja (formato: AAAA-MM-DD): ")

        try:
            cursor.execute("""
                UPDATE MediosTransporte
                SET disponibilidad = FALSE
                WHERE id = %s
            """, (codigo,))

            cursor.execute("""
                INSERT INTO BajasVehiculos
                (id, codigo_motor, tipo, motivo, tecnico_responsable, fecha)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (codigo, codigo_motor, tipo, motivo, tecnico_responsable, fecha))

            cursor.connection.commit()

            print("Baja de vehículo realizada correctamente.")

        except psycopg2.Error as e:
            print("Error al dar de baja el vehículo:", e)

    except psycopg2.Error as e:
        print("Error al obtener el vehículo:", e)

    input("Pulse ENTER para continuar hacia el Menú Principal...")


def listar_clientes_rentas(cursor):
    os.system("cls")
    print("----- Listar Clientes y Rentas -----")

    try:
        cursor.execute("""
            SELECT c.id, c.licencia_conduccion, c.nombre, c.telefono, c.direccion, r.fecha_inicio, r.fecha_fin, r.medio_transporte_id
            FROM Clientes c
            LEFT JOIN Rentas r ON c.id = r.cliente_id
            WHERE r.fecha_fin > CURRENT_DATE
            ORDER BY c.id
        """)

        clientes_rentas = cursor.fetchall()

        if len(clientes_rentas) == 0:
            print("No se encontraron clientes con rentas activas.")
        else:
            os.system("cls")
            print("--- LISTADO DE CLIENTES Y RENTAS ---")
            print()

            cliente_actual = None
            rentas_activas = []

            for cliente_renta in clientes_rentas:
                cliente_id = cliente_renta[0]
                licencia_conduccion = cliente_renta[1]
                nombre = cliente_renta[2]
                telefono = cliente_renta[3]
                direccion = cliente_renta[4]
                fecha_inicio = cliente_renta[5]
                fecha_fin = cliente_renta[6]
                medio_transporte_id = cliente_renta[7]

                if cliente_actual is None:
                    cliente_actual = cliente_id
                elif cliente_actual != cliente_id:
                    print(f"ID: {cliente_actual}")
                    print(f"Licencia de Conducción: {licencia_conduccion}")
                    print(f"Nombre: {nombre}")
                    print(f"Teléfono: {telefono}")
                    print(f"Dirección: {direccion}")
                    print("Rentas:")
                    for renta in rentas_activas:
                        print(f"ID del medio de transporte asignado: {renta[0]}")
                        print(f"Fecha de inicio: {renta[1]}")
                        print(f"Fecha de fin: {renta[2]}")
                    print("-----------------------------------")

                    rentas_activas = []
                    cliente_actual = cliente_id

                rentas_activas.append((medio_transporte_id, fecha_inicio, fecha_fin))

                print(f"ID: {cliente_actual}")
                print(f"Licencia de Conducción: {licencia_conduccion}")
                print(f"Nombre: {nombre}")
                print(f"Teléfono: {telefono}")
                print(f"Dirección: {direccion}")
                print("Rentas:")
                for renta in rentas_activas:
                    print(f"ID del medio de transporte asignado: {renta[0]}")
                    print(f"Fecha de inicio: {renta[1]}")
                    print(f"Fecha de fin: {renta[2]}")
                print("-----------------------------------")

    except psycopg2.Error as e:
        print("Error al listar los clientes y rentas:", e)

    input("Pulse ENTER para continuar hacia el Menú Principal...")

def rentar_medio_transporte(cursor):
    os.system("cls")
    print("----- Rentar Medio de Transporte -----")
    codigo = input("Ingrese el código del medio de transporte que desea rentar: ")

    try:
        cursor.execute("""
            SELECT disponibilidad FROM MediosTransporte WHERE id = %s
        """, (codigo,))
        
        disponibilidad = cursor.fetchone()

        if disponibilidad is None:
            print("El medio de transporte no existe.")
        elif not disponibilidad[0]:
            print("El medio de transporte no está disponible.")
        else:
            licencia_conduccion = input("Ingrese la licencia de conducción del cliente: ")
            fecha_inicio = input("Ingrese la fecha de inicio de la renta (YYYY-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de fin de la renta (YYYY-MM-DD): ")

            try:
                cursor.execute("""
                    INSERT INTO Rentas (cliente_id, medio_transporte_id, fecha_inicio, fecha_fin)
                    VALUES (
                        (SELECT id FROM Clientes WHERE licencia_conduccion = %s),
                        %s, %s, %s
                    )
                """, (licencia_conduccion, codigo, fecha_inicio, fecha_fin))

                cursor.execute("""
                    UPDATE MediosTransporte SET disponibilidad = FALSE WHERE id = %s
                """, (codigo,))

                cursor.connection.commit()

              
                cursor.execute("""
                    SELECT cliente_id FROM Rentas WHERE cliente_id = (SELECT id FROM Clientes WHERE licencia_conduccion = %s) AND medio_transporte_id = %s
                """, (licencia_conduccion, codigo))
                cliente_renta = cursor.fetchone()

                if cliente_renta is not None:
                    print("El medio de transporte se ha rentado exitosamente.")
                else:
                    print("Error al insertar la licencia de conducción del cliente.")

            except psycopg2.Error as e:
                print("Error al rentar el medio de transporte:", e)

    except psycopg2.Error as e:
        print("Error al verificar la disponibilidad del medio de transporte:", e)

    input("Pulse ENTER para continuar hacia el Menú Principal...")


def ejecutar_menu():
    conn = establecer_conexion()
    if conn is not None:
        cursor = conn.cursor()
        crear_tablas(cursor)

        while True:
            
            os.system("cls")
            print("==== RENTA DE VEHICULOS MINTUR ====")
            print("1. Insertar Medio de Transporte")
            print("2. Listar Medios de Transporte")
            print("3. Insertar Cliente")
            print("4. Mostrar Información de Clientes y Rentas")
            print("5. Rentar Medio de Transporte")
            print("6. Dar de Baja un Medio de Transporte")
            print("7. Salir")
            opcion = input("Ingrese el número de opción que desea ejecutar: ")

            if opcion == "1":
                insertar_medio_transporte(cursor)
            elif opcion == "2":
                listar_medios_transporte(cursor)
            elif opcion == "3":
                insertar_cliente(cursor)
            elif opcion == "4":
                listar_clientes_rentas(cursor)
            elif opcion == "5":
                rentar_medio_transporte(cursor)
            elif opcion == "6":
                efectuar_baja_vehiculo(cursor)
            elif opcion == "7":
                print("Saliendo del programa...")
                break
            else:
                input("Opción no válida, vuleva a intentarlo")

        cursor.close()
        conn.close()
    else:
        print("Error al ejecutar el programa.")

ejecutar_menu()
