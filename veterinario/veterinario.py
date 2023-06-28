import os
import psycopg2


def establecer_conexion():
    os.system("cls")
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="veterinario",
            user="postgres",
            password="password"
        )
        return conn

    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        exit()


def crear_tablas(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Animales (
                id SERIAL PRIMARY KEY,
                habitat VARCHAR(255),
                nombre VARCHAR(255),
                sexo VARCHAR(1),
                edad INTEGER,
                motivo_ingreso VARCHAR(255),
                dureza VARCHAR(255),
                temperatura FLOAT,
                salinidad FLOAT,
                peso FLOAT,
                tipo_dieta VARCHAR(255),
                nacido_en_cautiverio BOOLEAN,
                longitud FLOAT,
                tipo_reptil VARCHAR(255)
            )
        """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS Veterinarios (
                    dni INTEGER PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    edad INTEGER,
                    telefono VARCHAR(20),
                    especialidad VARCHAR(100),
                    direccion VARCHAR(200)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Consultas (
                id SERIAL PRIMARY KEY,
                fecha DATE,
                veterinario_dni INTEGER REFERENCES Veterinarios(dni),
                animal_codigo INTEGER REFERENCES Animales(id),
                tipo_consulta TEXT,
                tratamiento TEXT
            )
        """)
        cursor.connection.commit()
        print("Programa iniciado correctamente")
        input("Pulse ENTER para continuar hacia el Menú Principal...")

    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)


def insertar_animal(cursor):
    os.system("cls")
    print("----- Registrar Animal -----")
    habitat = input("Ingrese el hábitat del animal: ")
    nombre = input("Ingrese el nombre del animal: ")
    sexo = input("Ingrese el sexo del animal: ")
    edad = int(input("Ingrese la edad del animal: "))
    motivo_ingreso = input("Ingrese el motivo de ingreso del animal: ")

    tipo_animal = input("Ingrese la inicial del tipo de animal (P para peces y anfibios, M para mamíferos, R para reptiles): ").upper()

    if tipo_animal == "P":
        dureza = input("Ingrese la dureza del caparazón o piel del animal: ")
        temperatura = float(input("Ingrese la temperatura preferida del animal (°C): "))
        salinidad = float(input("Ingrese la salinidad preferida del animal (%): "))

        peso = None
        tipo_dieta = None
        nacido_en_cautiverio = None
        longitud = None
        tipo_reptil = None

    elif tipo_animal == "M":
        dureza = None
        temperatura = None
        salinidad = None

        peso = float(input("Ingrese el peso del animal (Kg): "))
        tipo_dieta = input("Ingrese el tipo de dieta del animal: ")
        nacido_en_cautiverio = input("¿El animal nació en cautiverio? (S/N): ").upper() == "S"

        longitud = None
        tipo_reptil = None

    elif tipo_animal == "R":
        dureza = None
        temperatura = None
        salinidad = None
        peso = float(input("Ingrese el peso del animal(Kg): "))
        longitud = float(input("Ingrese la longitud del animal(cm): "))
        tipo_reptil = input("Ingrese el tipo de reptil: ")

        tipo_dieta = None
        nacido_en_cautiverio = None

    else:
        print("Tipo de animal no válido.")
        input("Pulse ENTER para volver...")
        return

    try:
        cursor.execute("""
            INSERT INTO Animales (habitat, nombre, sexo, edad, motivo_ingreso, dureza, temperatura, salinidad, peso,
            tipo_dieta, nacido_en_cautiverio, longitud, tipo_reptil)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (habitat, nombre, sexo, edad, motivo_ingreso, dureza, temperatura, salinidad, peso, tipo_dieta,
              nacido_en_cautiverio, longitud, tipo_reptil))
        codigo = cursor.fetchone()[0]

        cursor.connection.commit()
        print("El animal se ha registrado correctamente. Código asignado:", codigo)
        input("Pulse ENTER para continuar...")

    except psycopg2.Error as e:
        print("Error al insertar el animal:", e)
        input("Pulse ENTER para volver...")

def insertar_veterinario(cursor):
    os.system("cls")
    dni = int(input("Ingrese el DNI del veterinario: "))
    nombre = input("Ingrese el nombre del veterinario: ")
    edad = int(input("Ingrese la edad del veterinario: "))
    telefono = input("Ingrese el número de teléfono del veterinario: ")
    especialidad = input("Ingrese la especialidad del veterinario: ")
    direccion = input("Ingrese la dirección del veterinario: ")

    try:
        cursor.execute("""
            INSERT INTO Veterinarios (dni, nombre, edad, telefono, especialidad, direccion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (dni, nombre, edad, telefono, especialidad, direccion))
        cursor.connection.commit()
        print("El veterinario se ha registrado correctamente.")
        input("Pulse ENTER para continuar...")

    except psycopg2.Error as e:
        print("Error al insertar el veterinario:", e)
        input("Pulse ENTER para volver...")

def listar_veterinarios(cursor):
    os.system("cls")

    try:
        cursor.execute("""
            SELECT dni, nombre, edad, telefono, especialidad, direccion FROM Veterinarios
        """)
        veterinarios = cursor.fetchall()

        if len(veterinarios) > 0:
            print("Veterinarios registrados:")
            for veterinario in veterinarios:
                print("DNI:", veterinario[0])
                print("Nombre:", veterinario[1])
                print("Edad:", veterinario[2])
                print("Teléfono:", veterinario[3])
                print("Especialidad:", veterinario[4])
                print("Dirección:", veterinario[5])
                print("-------------------------")
        else:
            print("No se encontraron veterinarios registrados.")

        input("Pulse ENTER para volver...")

    except psycopg2.Error as e:
        print("Error al listar los veterinarios:", e)
        input("Pulse ENTER para volver...")

def dar_de_baja_animal(cursor):
    os.system("cls")
    codigo = int(input("Ingrese el código del animal a dar de baja: "))

    try:
        cursor.execute("""
            DELETE FROM Animales WHERE id = %s
        """, (codigo,))

        if cursor.rowcount == 0:
            print("No se encontró ningún animal con ese código.")
        else:
            cursor.connection.commit()
            print("El animal se ha dado de baja correctamente.")

        input("Pulse ENTER para continuar...")

    except psycopg2.Error as e:
        print("Error al dar de baja el animal:", e)
        input("Pulse ENTER para volver...")


def listar_animales(cursor):
    os.system("cls")
    opcion = input("Ingrese la inicial de la categoría a listar (P para peces y anfibios, M para mamíferos, R para reptiles): ").upper()

    try:
        if opcion == "P":
            os.system("cls")
            cursor.execute("""
                SELECT id, habitat, nombre, sexo, edad, motivo_ingreso, dureza, temperatura, salinidad FROM Animales WHERE tipo_reptil IS NULL AND dureza IS NOT NULL
            """)
            animales = cursor.fetchall()

            if len(animales) > 0:
                print("Animales registrados (Peces y anfibios):")
                for animal in animales:
                    print("Código:", animal[0])
                    print("Hábitat:", animal[1])
                    print("Nombre:", animal[2])
                    print("Sexo:", animal[3])
                    print("Edad:", animal[4])
                    print("Motivo de ingreso:", animal[5])
                    print("Dureza:", animal[6])
                    print("Temperatura (°C):", animal[7])
                    print("Salinidad (%):", animal[8])
                    print("-------------------------")
            else:
                print("No se encontraron animales registrados (Peces y anfibios).")

        elif opcion == "M":
            os.system("cls")
            cursor.execute("""
                SELECT id, habitat, nombre, sexo, edad, motivo_ingreso, peso, tipo_dieta, nacido_en_cautiverio FROM Animales WHERE dureza IS NULL AND tipo_reptil IS NULL AND peso IS NOT NULL
            """)
            animales = cursor.fetchall()

            if len(animales) > 0:
                print("Animales registrados (Mamíferos):")
                for animal in animales:
                    print("Código:", animal[0])
                    print("Hábitat:", animal[1])
                    print("Nombre:", animal[2])
                    print("Sexo:", animal[3])
                    print("Edad:", animal[4])
                    print("Motivo de ingreso:", animal[5])
                    print("Peso (Kg):", animal[6])
                    print("Tipo de dieta:", animal[7])
                    print("Nacido en cautiverio:", animal[8])
                    print("-------------------------")
            else:
                print("No se encontraron animales registrados (Mamíferos).")

        elif opcion == "R":
            os.system("cls")
            cursor.execute("""
                SELECT id, habitat, nombre, sexo, edad, motivo_ingreso, peso, longitud, tipo_reptil FROM Animales WHERE tipo_reptil IS NOT NULL
            """)
            animales = cursor.fetchall()

            if len(animales) > 0:
                print("Animales registrados (Reptiles):")
                for animal in animales:
                    print("Código:", animal[0])
                    print("Hábitat:", animal[1])
                    print("Nombre:", animal[2])
                    print("Sexo:", animal[3])
                    print("Edad:", animal[4])
                    print("Motivo de ingreso:", animal[5])
                    print("Peso (Kg):", animal[6])
                    print("Longitud (cm):", animal[7])
                    print("Tipo de reptil:", animal[8])
                    print("-------------------------")
            else:
                print("No se encontraron animales registrados (Reptiles).")

        else:
            print("Categoría no válida.")
            input("Pulse ENTER para continuar...")
            return

        input("Pulse ENTER para volver...")

    except psycopg2.Error as e:
        print("Error al listar los animales:", e)
        input("Pulse ENTER para volver...")


def atender_animal(cursor):
    os.system("cls")
    codigo = int(input("Ingrese el código del animal a atender: "))
    fecha = input("Ingrese la fecha de la consulta (YYYY-MM-DD): ")
    veterinario_dni = int(input("Ingrese el DNI del veterinario que atendió: "))
    tipo_consulta = input("Ingrese el tipo de consulta (rutinaria o por enfermedad): ")
    tratamiento = input("Ingrese la descripción del tratamiento (opcional): ")

    try:
        cursor.execute("""
            INSERT INTO Consultas (fecha, veterinario_dni, animal_codigo, tipo_consulta, tratamiento)
            VALUES
            (%s, %s, %s, %s, %s)
        """, (fecha, veterinario_dni, codigo, tipo_consulta, tratamiento))
        cursor.connection.commit()
        print("La consulta se ha registrado correctamente.")
        input("Pulse ENTER para continuar...")

    except psycopg2.Error as e:
        print("Error al atender el animal:", e)
        input("Pulse ENTER para volver...")

def mostrar_animales_por_veterinario(cursor):
    os.system("cls")
    veterinario_dni = int(input("Ingrese el DNI del veterinario: "))

    try:
        cursor.execute("""
            SELECT a.nombre, c.fecha, c.tipo_consulta, c.tratamiento
            FROM Animales a
            INNER JOIN Consultas c ON a.id = c.animal_codigo
            WHERE c.veterinario_dni = %s
            ORDER BY c.fecha
        """, (veterinario_dni,))

        animales = cursor.fetchall()

        if len(animales) > 0:
            print(f"Animales atendidos por el veterinario con DNI {veterinario_dni}:")
            for animal in animales:
                print(f"Nombre: {animal[0]}, Fecha: {animal[1]}, Tipo de consulta: {animal[2]}, Tratamiento: {animal[3]}")
        else:
            print(f"No se encontraron animales atendidos por el veterinario con DNI {veterinario_dni}.")

        input("Pulse ENTER para volver...")

    except psycopg2.Error as e:
        print("Error al mostrar los animales atendidos por el veterinario:", e)
        input("Pulse ENTER para volver...")


def mostrar_menu():
    os.system("cls")
    print("----- Menú Principal -----")
    print("1. Insertar animal")
    print("2. Dar de baja animal")
    print("3. Listar animales")
    print("4. Atender animal")
    print("5. Insertar veterinario")
    print("6. Mostrar animales atendidos por cada veterinario")
    print("7. Mostrar veterinarios registrados")
    print("8. Salir")


def main():
    conn = establecer_conexion()
    cursor = conn.cursor()

    crear_tablas(cursor)

    while True:
        mostrar_menu()
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            insertar_animal(cursor)
        elif opcion == "2":
            dar_de_baja_animal(cursor)
        elif opcion == "3":
            listar_animales(cursor)
        elif opcion == "4":
            atender_animal(cursor)
        elif opcion == "5":
            insertar_veterinario(cursor)
        elif opcion == "6":
            mostrar_animales_por_veterinario(cursor)
        elif opcion == "7":
            listar_veterinarios(cursor)
                
        elif opcion == "8":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
