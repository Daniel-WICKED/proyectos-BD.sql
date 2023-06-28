import os
import psycopg2
from datetime import date

os.system("cls")

def conectar():
    try:
        conn = psycopg2.connect(
            database="almacen_med",
            user="postgres",
            password="password",
            host="localhost"
        )
        print("Conexión exitosa a la base de datos.")
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def crear_tablas(cursor):
    try:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Farmacias (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                direccion VARCHAR(200) NOT NULL,
                telefono VARCHAR(15) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Medicamentos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                codigo VARCHAR(100) NOT NULL,
                lote VARCHAR(100) NOT NULL,
                fecha_vencimiento DATE NOT NULL,
                modo_presentacion VARCHAR(100) NOT NULL,
                cantidad INTEGER NOT NULL,
                farmacia_id INTEGER REFERENCES Farmacias(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Trabajadores (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                CI VARCHAR(11) NOT NULL,
                farmacia_id INTEGER REFERENCES Farmacias(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ventas (
                id SERIAL PRIMARY KEY,
                medicamento_id INTEGER REFERENCES Medicamentos(id),
                farmacia_id INTEGER REFERENCES Farmacias(id),
                trabajadores_id INTEGER REFERENCES Trabajadores(id)
            )
        """)


        cursor.connection.commit()
        print("Tablas creadas correctamente.")
        input("Presione ENTER para continuar hacia el Menú Principal...")
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)
        input("Pulse Enter")
       
def insertar_farmacia(cursor):
    os.system("cls")
    try:
        print("----- INSERTAR Farmacia -----")
        nombre = input("Nombre de la farmacia: ")
        direccion = input("Direccion de la farmacia: ")
        telefono = input("Telefono de la farmacia: ")
        id = int(input("ID de la farmacia: "))

        cursor.execute("""
            INSERT INTO Farmacias (nombre, direccion, telefono, id)
            VALUES ( %s, %s, %s, %s)
        """, (nombre, direccion, telefono, id))
        cursor.connection.commit()
        print("Farmacia registrada correctamente.")
        
    except psycopg2.Error as e:
        print("Error al insertar la farmacia:", e)
    input("Presione ENTER para continuar")           

def insertar_medicamento(cursor):
    os.system("cls")
    try:
        print("----- INSERTAR MEDICAMENTO -----")
        nombre = input("Nombre del medicamento: ")
        codigo = input("Código del medicamento: ")
        lote = input("Lote del medicamento: ")
        fecha_vencimiento = input("Fecha de vencimiento del medicamento (YYYY-MM-DD): ")
        modo_presentacion = input("Modo de presentación del medicamento: ")
        cantidad = int(input("Cantidad del medicamento: "))
        farmacia_id = int(input("ID de la farmacia: "))

        cursor.execute("""
            INSERT INTO Medicamentos (nombre, codigo, lote, fecha_vencimiento, modo_presentacion, cantidad, farmacia_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, codigo, lote, fecha_vencimiento, modo_presentacion, cantidad, farmacia_id))
        cursor.connection.commit()
        print("Medicamento registrado correctamente.")
        
    except psycopg2.Error as e:
        print("Error al insertar el medicamento:", e)
    input("Presione ENTER para continuar")
    
def insertar_trabajador(cursor):
    os.system("cls")
    try:
        print("----- INSERTAR TRABAJADOR -----")
        nombre = input("Nombre del trabajador: ")
        CI = input("Carnet de Identidad: ")
        farmacia_id = input("ID de la farmacia: ")
        
        cursor.execute("""
            INSERT INTO Trabajadores (nombre,CI, farmacia_id)
            VALUES (%s, %s, %s)
        """, (nombre, CI, farmacia_id))
        cursor.connection.commit()
        print("Trabajador registrado correctamente.")
        
    except psycopg2.Error as e:
        print("Error al insertar el trabajador:", e)
    input("Presione ENTER para continuar")
        
    
    
def eliminar_farmacia(cursor):
    os.system("cls")
    try:
        print("----- ELIMINAR FARMACIA -----")
        id = int(input("ID de la a eliminar: "))

        cursor.execute("DELETE FROM FARMACIAS WHERE id = %s", (id,))
        cursor.connection.commit()
        print("Farmacia eliminada correctamente.")
        
    except psycopg2.Error as e:
        print("Error al eliminar la farmacia:", e)
    input("Presione ENTER para continuar")

def eliminar_medicamento(cursor):
    os.system("cls")
    try:
        print("----- ELIMINAR MEDICAMENTO -----")
        medicamento_id = int(input("ID del medicamento a eliminar: "))

        cursor.execute("DELETE FROM Medicamentos WHERE id = %s", (medicamento_id,))
        cursor.connection.commit()
        print("Medicamento eliminado correctamente.")
        
    except psycopg2.Error as e:
        print("Error al eliminar el medicamento:", e)
    input("Presione ENTER para continuar")
    
def buscar_farmacias(cursor):
    os.system("cls")
    try:
        print("----- BUSCAR FARMACIA -----")
        nombre = input("Nombre de la farmacia a buscar: ")
        
        cursor.execute("SELECT * FROM Farmacias WHERE nombre ILIKE %s", (f"%{nombre}%",))
        farmacias = cursor.fetchall()
        
        if farmacias:
            print("Farmacias encontrada:")
            for farmacia in farmacias:
                print("ID:", farmacia[0])
                print("Nombre:", farmacia[1])
                print("Direccion:", farmacia[2])
                print("Telefono:", farmacia[3])
                print("---------------------------")
        else:
            print("No se encontraron farmacias con el nombre especificado.")
        
    except psycopg2.Error as e:
        print("Error al buscar farmacias:", e)
    input("Presione ENTER para continuar")
    
def mostrar_farmacia(cursor):
    os.system("cls")
    try:
        # Mostrar farmacias
        print(" Farmacias:")
        cursor.execute("SELECT * FROM Farmacias")
        farmacias = cursor.fetchall()
        for farmacia in farmacias:
            print(farmacia)
        print()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    input("Presione Enter para continuar...")
    
def mostrar_medicamentos(cursor):
    os.system("cls")
    try:
        # Mostrar medicamentos
        print(" Medicamentos:")
        cursor.execute("SELECT * FROM Medicamentos")
        medicamentos = cursor.fetchall()
        for medicamento in medicamentos:
            print(medicamento)
        print()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    input("Presione Enter para continuar...")

def buscar_medicamentos(cursor):
    os.system("cls")
    try:
        print("----- BUSCAR MEDICAMENTOS EXISTENTES -----")
        nombre = input("Nombre del medicamento a buscar: ")
        
        cursor.execute("SELECT * FROM Medicamentos WHERE nombre ILIKE %s", (f"%{nombre}%",))
        medicamentos = cursor.fetchall()
        
        if medicamentos:
            print("Medicamentos encontrados:")
            for medicamento in medicamentos:
                print("ID:", medicamento[0])
                print("Nombre:", medicamento[1])
                print("Código:", medicamento[2])
                print("Lote:", medicamento[3])
                print("Fecha de vencimiento:", medicamento[4])
                print("Modo de presentación:", medicamento[5])
                print("Cantidad:", medicamento[6])
                print("ID de la farmacia:", medicamento[7])
                print("---------------------------")
        else:
            print("No se encontraron medicamentos con el nombre especificado.")
        
    except psycopg2.Error as e:
        print("Error al buscar medicamentos:", e)
    input("Presione ENTER para continuar")

def vender_medicamento(cursor):
    os.system("cls")
    try:
        print("----- VENDER MEDICAMENTO A FARMACIA -----")
        medicamento_id = int(input("ID del medicamento a vender: "))
        farmacia_id = int(input("ID de la farmacia que compra el medicamento: "))
        trabajadores_id = int(input("ID del trabajador: "))
       # fecha_venta = date.today("Fecha de la venta: ")
        

        cursor.execute("""
            INSERT INTO Ventas (medicamento_id, farmacia_id, trabajadores_id)
            VALUES (%s, %s, %s)
        """, (medicamento_id, farmacia_id, trabajadores_id))
        cursor.connection.commit()
        print("Venta realizada correctamente.")
        
    except psycopg2.Error as e:
        print("Error al realizar la venta:", e)
    input("Presione ENTER para continuar")

def menu_principal(cursor):
    while True:
        os.system("cls")
        print("----- MENÚ PRINCIPAL -----")
        print("1. Insertar farmacia")
        print("2. Insertar medicamento")
        print("3. Insertar trabajador")
        print("4. Eliminar farmacia")
        print("5. Eliminar medicamento")
        print("6. Buscar farmacias existentes")
        print("7. Buscar medicamentos existentes")
        print("8. Mostrar farmacias existentes")
        print("9. Mostrar medicamentos existentes")
        print("10. Vender medicamento a farmacia")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            insertar_farmacia(cursor)
        if opcion == "2":
            insertar_medicamento(cursor)
        elif opcion == "3":
            insertar_trabajador(cursor)
        elif opcion == "4":
            eliminar_farmacia(cursor)
        elif opcion == "5":
            eliminar_medicamento(cursor)
        elif opcion == "6":
            buscar_farmacias(cursor)
        elif opcion == "7":
             buscar_medicamentos(cursor)
        elif opcion == "8":
            mostrar_farmacia(cursor)
        elif opcion == "9":
            mostrar_medicamentos(cursor)
        elif opcion == "10":
            vender_medicamento(cursor)
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")
        os.system("cls")

def main():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        crear_tablas(cursor)
        menu_principal(cursor)
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    main()
