import os
import psycopg2
import datetime

os.system("cls")

def conectar():
    try:
        conn = psycopg2.connect(
            database="tienda_inf",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        print("Conexión exitosa con la base de datos")
        return conn
    
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos, revise los parámetros de conexión.", e)
        return None

def crear_tablas(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Productos (
                codigo SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion VARCHAR(200) NOT NULL,
                precio DECIMAL(10, 2) NOT NULL,
                existencias INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clientes (
                codigo SERIAL PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                apellidos VARCHAR(50) NOT NULL,
                direccion VARCHAR(100) NOT NULL,
                telefono VARCHAR(20) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Proveedores (
                codigo SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                apellidos VARCHAR(255) NOT NULL,
                direccion VARCHAR(255) NOT NULL,
                provincia VARCHAR(255) NOT NULL,
                telefono VARCHAR(20) NOT NULL,
                producto_id INTEGER REFERENCES Productos(codigo)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Compras (
                codigo SERIAL PRIMARY KEY,
                cliente_id INTEGER REFERENCES Clientes (codigo) NOT NULL,
                producto_id INTEGER REFERENCES Productos (codigo) NOT NULL,
                fecha_compra DATE NOT NULL
            )
        """)
        cursor.connection.commit()
        print("Tablas comprobadas con éxito")
        
        
    except psycopg2.Error as e:
        print("Error al crear las tablas:", e)
    input("Presione ENTER para continuar...")

def insertar_producto(cursor):
    os.system("cls")
    try:
        print("=== Insertar Producto ===")
        nombre = input("Nombre del producto: ")
        descripcion = input("Descripción del producto: ")
        precio = float(input("Precio del producto (CUP): "))
        existencias = int(input("Existencias del producto: "))

        cursor.execute("""
            INSERT INTO Productos (nombre, descripcion, precio, existencias)
            VALUES (%s, %s, %s, %s)
        """, (nombre, descripcion, precio, existencias))
        cursor.connection.commit()
        print("Producto guardado correctamente.")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al insertar los datos:", e)

def insertar_cliente(cursor):
    os.system("cls")
    try:
        print("=== Insertar Cliente ===")
        nombre = input("Nombre: ")
        apellidos = input("Apellidos: ")
        direccion = input("Dirección: ")
        telefono = input("Teléfono: ")

        cursor.execute("""
            INSERT INTO Clientes (nombre, apellidos, direccion, telefono)
            VALUES (%s, %s, %s, %s)
        """, (nombre, apellidos, direccion, telefono))
        cursor.connection.commit()
        print("Cliente guardado correctamente.")

        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al insertar los datos:", e)

def mostrar_historial_compras(cursor):
    os.system("cls")
    try:
        print("=== Historial de Compras ===")
        cursor.execute("""
            SELECT CL.nombre AS nombre_cliente, P.nombre AS nombre_producto, C.fecha_compra
            FROM Compras C
            INNER JOIN Clientes CL ON C.cliente_id = CL.codigo
            INNER JOIN Productos P ON C.producto_id = P.codigo
        """)
        historial_compras = cursor.fetchall()

        if len(historial_compras) == 0:
            print("No hay compras registradas.")
        else:
            for compra in historial_compras:
                nombre_cliente = compra[0]
                nombre_producto = compra[1]
                fecha_compra = compra[2]

                print(f"Nombre del Cliente: {nombre_cliente}")
                print(f"Nombre del Producto: {nombre_producto}")
                print(f"Fecha de Compra: {fecha_compra}")
                print("--------------------------------")
        
    except psycopg2.Error as e:
        print("Error al mostrar el historial de compras:", e)

    input("Presione ENTER para volver")
                    
def insertar_proveedor(cursor):
    os.system("cls")
    try:
        print("=== Insertar Proveedor ===")
        nombre = input("Nombre: ")
        apellidos = input("Apellidos: ")
        direccion = input("Dirección: ")
        provincia = input("Provincia: ")
        telefono = input("Teléfono: ")

        cursor.execute("SELECT codigo, descripcion FROM Productos")
        productos = cursor.fetchall()

        if len(productos) > 0:
            print("Seleccione el código del producto suministrado por el proveedor:")
            for producto in productos:
                print(f"Código: {producto[0]}, Descripción: {producto[1]}")
            codigo_producto = int(input("Código del producto: "))
            cursor.execute("""
                INSERT INTO Proveedores (nombre, apellidos, direccion, provincia, telefono, producto_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, apellidos, direccion, provincia, telefono, codigo_producto))
            cursor.connection.commit()
            print("Proveedor guardado correctamente.")
            
        else:
            print("No hay productos registrados.")

        
    except psycopg2.Error as e:
        print("Error al insertar los datos:", e)

def realizar_compra(cursor):
    os.system("cls")
    try:
        codigo_cliente = int(input("Ingrese el código del cliente: "))
        codigo_producto = int(input("Ingrese el código del producto: "))
        fecha_compra = datetime.date.today()

        cursor.execute("""
            INSERT INTO Compras (cliente_id, producto_id, fecha_compra)
            VALUES (%s, %s, %s)
        """, (codigo_cliente, codigo_producto, fecha_compra))

        print("Compra registrada exitosamente.")
        cursor.connection.commit()
    except (psycopg2.Error, ValueError) as e:
        print("Error al registrar la compra:", e)

    input("Presione ENTER para continuar")
    
def mostrar_productos(cursor):
    os.system("cls")
    try:
        
        cursor.execute("""
            SELECT p.codigo, p.nombre, p.descripcion, p.precio, p.existencias, 
                   STRING_AGG(pr.nombre, ', ') AS proveedores
            FROM Productos p
            LEFT JOIN Proveedores pr ON p.codigo = pr.producto_id
            GROUP BY p.codigo, p.nombre, p.descripcion, p.precio, p.existencias
        """)
        productos = cursor.fetchall()

        if len(productos) == 0:
            print("No hay productos registrados.")
        else:
            print("=== Productos Registrados ===")
            for producto in productos:
                codigo = producto[0]
                nombre = producto[1]
                descripcion = producto[2]
                precio = producto[3]
                existencias = producto[4]
                proveedores = producto[5]

                print(f"Código: {codigo}")
                print(f"Nombre: {nombre}")
                print(f"Descripción: {descripcion}")
                print(f"Precio: {precio}")
                print(f"Existencias: {existencias}")
                print(f"Proveedores: {proveedores}")
                print("--------------------------------")
        input("Presione ENTER para volver")

    except psycopg2.Error as e:
        print("Error al mostrar los productos:", e)


        
def mostrar_proveedores_productos(cursor):
    os.system("cls")
    try:
        cursor.execute("""
            SELECT PR.codigo, PR.nombre, PR.apellidos, PR.direccion, PR.provincia,
                   PR.telefono, P.codigo, P.descripcion
            FROM Proveedores PR
            LEFT JOIN Productos P ON PR.producto_id = P.codigo
        """)

        proveedores_productos = cursor.fetchall()

        if len(proveedores_productos) > 0:
            print("=== Proveedores y Productos ===")
            for proveedor in proveedores_productos:
                print(f"Código Proveedor: {proveedor[0]}")
                print(f"Nombre: {proveedor[1]} {proveedor[2]}")
                print(f"Dirección: {proveedor[3]}")
                print(f"Provincia: {proveedor[4]}")
                print(f"Teléfono: {proveedor[5]}")
                print(f"Código Producto: {proveedor[6]}")
                print(f"Descripción Producto: {proveedor[7]}")
                print("===============================")
        else:
            print("No hay proveedores registrados.")
        
        input("Presione ENTER para continuar")
    except psycopg2.Error as e:
        print("Error al mostrar los datos:", e)

def menu_principal():
    conn = conectar()
    if conn is None:
        return

    cursor = conn.cursor()

    crear_tablas(cursor)

    while True:
        os.system("cls")
        print("=== Tienda de Informática ===")
        print("1. Insertar Producto")
        print("2. Insertar Cliente")
        print("3. Insertar Proveedor")
        print("4. Realizar Compra")
        print("5. Mostrar Productos")
        print("6. Mostrar Proveedores")
        print("7. Historial de Compras")
        print("0. Salir")
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            insertar_producto(cursor)
        elif opcion == "2":
            insertar_cliente(cursor)
        elif opcion == "3":
            insertar_proveedor(cursor)
        elif opcion == "4":
            realizar_compra(cursor)
        elif opcion == "5":
            mostrar_productos(cursor)
        elif opcion == "6":
            mostrar_proveedores_productos(cursor)
        elif opcion == "7":
            mostrar_historial_compras(cursor)        
        elif opcion == "0":
            break

    cursor.close()
    conn.close()

if __name__ == "__main__":
    menu_principal()