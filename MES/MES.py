import os
import psycopg2

os.system("cls")

def conectar_bd():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="MES",
            user="postgres",
            password="password"
        )
        print("Base de datos conectada")
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def crear_tablas(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Profesores (
                id SERIAL PRIMARY KEY,
                carnet_identidad INTEGER,
                nombre TEXT,
                fecha_nacimiento DATE,
                sexo VARCHAR(1),
                direccion_particular TEXT,
                anios_experiencia INTEGER,
                asignatura TEXT,
                categoria_docente TEXT,
                tiene_categoria_cientifica BOOLEAN
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Estudiantes (
                id SERIAL PRIMARY KEY,
                carnet_identidad INTEGER,
                nombre TEXT,
                fecha_nacimiento DATE,
                sexo VARCHAR(1),
                direccion VARCHAR(100),
                facultad VARCHAR(100),
                especialidad VARCHAR(100),
                anio_curso INTEGER,
                grupo INTEGER,
                provincia VARCHAR(100),
                num_cuarto INTEGER,
                becado BOOLEAN,
                profesor_id INTEGER,
                FOREIGN KEY (profesor_id) REFERENCES Profesores(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EstudiantesGraduados (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER,
                indice_academico FLOAT,
                nombre_rector TEXT,
                FOREIGN KEY (estudiante_id) REFERENCES Estudiantes(id)
            )
        """)

        cursor.connection.commit()
        print("Tablas creadas o verificadas correctamente.")
        input("Pulse ENTER para continuar hacia el programa...")
        
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)
        input("Pulse ENTER para continuar...")

def insertar_profesor(cursor):
    while True:
        os.system("cls")
        try:
            print("Ingrese los siguientes datos del profesor:")
            carnet_identidad = input("Carnet de identidad: ")
            nombre = input("Nombre: ")
            fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
            sexo = input("Sexo: ")
            direccion_particular = input("Dirección particular: ")
            anios_experiencia = int(input("Años de experiencia en la docencia: "))
            asignatura = input("Asignatura que imparte: ")
            categoria_docente = input("Categoría docente: ")
            tiene_categoria_cientifica = input("¿Tiene alguna categoría científica? (S/N): ").upper() == "S"

            cursor.execute("""
                INSERT INTO Profesores (carnet_identidad, nombre, fecha_nacimiento, sexo, direccion_particular,
                anios_experiencia, asignatura, categoria_docente, tiene_categoria_cientifica)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (carnet_identidad, nombre, fecha_nacimiento, sexo, direccion_particular, anios_experiencia,
                  asignatura, categoria_docente, tiene_categoria_cientifica))
            cursor.connection.commit()
            print("Datos del profesor guardados correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al insertar los datos:", e)
            opcion = input("¿Reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def insertar_estudiante(cursor):
    os.system("cls")
    while True:
        try:
            print("Ingrese los siguientes datos del estudiante:")
            carnet_identidad = input("Carnet de identidad del estudiante: ")
            nombre = input("Nombre: ")
            fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
            sexo = input("Sexo: ")
            direccion = input("Dirección particular: ")
            facultad = input("Facultad: ")
            especialidad = input("Especialidad: ")
            anio_curso = int(input("Año de estudio: "))
            grupo = input("Grupo: ")
            profesor_id = int(input("ID del profesor que le imparte clases: "))
            provincia = input("Provincia: ")
            becado = input("¿Está becado? (S/N): ").upper() == "S"
            num_cuarto = None

            if becado:
                num_cuarto = int(input("Número de cuarto: "))

            cursor.execute("""
                INSERT INTO Estudiantes (carnet_identidad, nombre, fecha_nacimiento, sexo, direccion, facultad,
                especialidad, anio_curso, grupo, provincia, num_cuarto, becado, profesor_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (carnet_identidad, nombre, fecha_nacimiento, sexo, direccion, facultad, especialidad, anio_curso,
                  grupo, provincia, num_cuarto, becado, profesor_id))
            
            cursor.connection.commit()
            print("Datos del estudiante guardados correctamente.")
            input("Presione ENTER para continuar")
            break
        except psycopg2.Error as e:
            print("Error al insertar los datos:", e)
            opcion = input("¿Reintentar? (S/N): ")
            if opcion.upper() != "S":
                break

def obtener_matricula_estudiantes(cursor):
    os.system("cls")
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM Estudiantes
        """)
        matricula = cursor.fetchone()[0]
        print("La matrícula total de estudiantes del centro es:", matricula)
    except psycopg2.Error as e:
        print("Error al obtener la matrícula de estudiantes:", e)
    input("Pulse ENTER para volver al menu anterior...")

def obtener_total_profesores(cursor):
    os.system("cls")
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM Profesores
        """)
        total_profesores = cursor.fetchone()[0]
        print("El total de profesores del claustro es:", total_profesores)
    except psycopg2.Error as e:
        print("Error al obtener el total de profesores:", e)
    input("Pulse ENTER para volver al menu anterior...")
        
def listar_profesores(cursor):
    os.system("cls")
    try:
        cursor.execute("""
            SELECT * FROM Profesores
        """)
        profesores = cursor.fetchall()

        if len(profesores) > 0:
            print("Listado de profesores:")
            for profesor in profesores:
                id_profesor = profesor[0]
                carnet_identidad = profesor[1]
                nombre = profesor[2]
                fecha_nacimiento = profesor[3]
                sexo = profesor[4]
                direccion_particular = profesor[5]
                anios_experiencia = profesor[6]
                asignatura = profesor[7]
                categoria_docente = profesor[8]
                tiene_categoria_cientifica = profesor[9]

                print("ID:", id_profesor)
                print("Carnet de identidad:", carnet_identidad)
                print("Nombre:", nombre)
                print("Fecha de nacimiento:", fecha_nacimiento)
                print("Sexo:", sexo)
                print("Dirección particular:", direccion_particular)
                print("Años de experiencia en la docencia:", anios_experiencia)
                print("Asignatura que imparte:", asignatura)
                print("Categoría docente:", categoria_docente)
                if tiene_categoria_cientifica:
                    print("Tiene categoría científica: Sí")
                else:
                    print("Tiene categoría científica: No")
                print("----------------------------------")
        else:
            print("No se encontraron profesores registrados.")
    except psycopg2.Error as e:
        print("Error al obtener el listado de profesores:", e)

    input("Pulse ENTER para volver al menu anterior...")

def promover_a_graduado(cursor):
    os.system("cls")
    try:
        cursor.execute("""
            SELECT id, carnet_identidad, nombre
            FROM Estudiantes
        """)

        estudiantes = cursor.fetchall()

        if estudiantes:
            print("Estudiantes activos:")
            for estudiante in estudiantes:
                print("ID:", estudiante[0])
                print("Carnet de Identidad:", estudiante[1])
                print("Nombre:", estudiante[2])
                print("")

            estudiante_id = input("Ingrese el ID del estudiante que desea promover a graduado: ")

            estudiante_id = int(estudiante_id)

            estudiante_promover = None

            for estudiante in estudiantes:
                if estudiante[0] == estudiante_id:
                    estudiante_promover = estudiante
                    break

            if estudiante_promover:
                indice_academico = float(input("Ingrese el índice académico del estudiante: "))
                nombre_rector = input("Ingrese el nombre del rector: ")

                cursor.execute("""
                    INSERT INTO EstudiantesGraduados (estudiante_id, indice_academico, nombre_rector)
                    VALUES (%s, %s, %s)
                """, (estudiante_id, indice_academico, nombre_rector))

                cursor.connection.commit()
                print("El estudiante ha sido promovido a graduado correctamente.")
            else:
                print("No se encontró un estudiante con el ID ingresado.")

        else:
            print("No hay estudiantes activos para promover.")

    except ValueError:
        print("El ID del estudiante ingresado no es válido.")
    except Exception as e:
        print("Error al promover al estudiante a graduado:", e)

    input("Pulse ENTER para continuar...")

def listar_estudiantes_graduados(cursor):
    os.system("cls")
    try:
        cursor.execute("""
            SELECT eg.id, e.carnet_identidad, e.nombre, eg.indice_academico, eg.nombre_rector,
                    e.facultad, e.especialidad, e.anio_curso                 
            FROM EstudiantesGraduados eg
            JOIN Estudiantes e ON eg.estudiante_id = e.id
        """)

        estudiantes_graduados = cursor.fetchall()

        if not estudiantes_graduados:
            print("No hay estudiantes graduados.")
        else:
            print("Estudiantes Graduados:")
            print("======================")
            for estudiante in estudiantes_graduados:
                print("ID:", estudiante[0])
                print("Carnet de Identidad:", estudiante[1])
                print("Nombre:", estudiante[2])
                print("Índice Académico:", estudiante[3])
                print("Nombre del Rector:", estudiante[4])
                print("Facultad:", estudiante[5])
                print("Especialidad:", estudiante[6])
                print("------------------------------")

    except Exception as e:
        print("Error al mostrar estudiantes graduados:", e)

    input("Pulse ENTER para volver al menú anterior...")

def listar_estudiantes(cursor):
    os.system("cls")
    try:
        cursor.execute("""
            SELECT * FROM Estudiantes
        """)
        estudiantes = cursor.fetchall()

        if len(estudiantes) > 0:
            print("Listado de estudiantes:")
            print("=======================")
            for estudiante in estudiantes:
                carnet_identidad = estudiante[1]
                nombre = estudiante[2]
                fecha_nacimiento = estudiante[3]
                sexo = estudiante[4]
                direccion = estudiante[5]
                facultad = estudiante[6]
                especialidad = estudiante[7]
                anio_curso = estudiante[8]
                grupo = estudiante[9]
                provincia = estudiante[10]
                num_cuarto = estudiante[11]
                becado = estudiante[12]
                profesor = estudiante[13]
                
                print("Carnet de identidad:", carnet_identidad)
                print("Nombre:", nombre)
                print("Fecha de nacimiento:", fecha_nacimiento)
                print("Sexo:", sexo)
                print("Dirección:", direccion)
                print("Facultad:", facultad)
                print("Especialidad:", especialidad)
                print("Año escolar:", anio_curso)
                print("Grupo:", grupo)
                print("Profesor:", profesor)
                print("Provincia:", provincia)
                if becado:
                    print("Número de cuarto:", num_cuarto)
                    print("Becado: Sí")
                else:
                    print("Becado: No")
                print("----------------------------------")
        else:
            print("No se encontraron estudiantes registrados.")
    except psycopg2.Error as e:
        print("Error al obtener el listado de estudiantes:", e)
    input("Pulse ENTER para volver al menu anterior...")
    
def menu_principal():
    conn = conectar_bd()
    if conn is None:
        return

    cursor = conn.cursor()

    crear_tablas(cursor)

    while True:
        os.system("cls")
        print("===== ADMINISTRACIÓN DE LOS DATOS DEL CENTRO =====")
        print("1. Insertar profesor")
        print("2. Insertar estudiante")
        print("3. Obtener matrícula total de estudiantes")
        print("4. Obtener total de profesores")
        print("5. Listar profesores")
        print("6. Listar estudiantes")
        print("7. Promover estudiante a graduado")
        print("8. Mostrar estudiantes promovidos a graduado")
        print("9. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            insertar_profesor(cursor)
        elif opcion == "2":
            insertar_estudiante(cursor)
        elif opcion == "3":
            obtener_matricula_estudiantes(cursor)
        elif opcion == "4":
            obtener_total_profesores(cursor)
        elif opcion == "5":
            listar_profesores(cursor)
        elif opcion == "6":
            listar_estudiantes(cursor)
        elif opcion == "7":
            promover_a_graduado(cursor)
        elif opcion == "8":
            listar_estudiantes_graduados(cursor)
        elif opcion == "9":
            os.system("cls")
            print("Saliendo del programa...")
            break
        else:
            os.system("cls")
            input("Opción inválida, pulse ENTER e intente nuevamente.")
        
    cursor.close()
    conn.close()

if __name__ == "__main__":
    menu_principal()
