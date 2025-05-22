import sqlite3

conexion = sqlite3.connect("uninpahu.db")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL,
        apellido VARCHAR(50) NOT NULL,
        celular VARCHAR(15) NOT NULL,
        correo VARCHAR(100) NOT NULL
    )
""")
conexion.commit()


def usuarioExiste(idUsuario):
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (idUsuario,))
    return cursor.fetchone() is not None


def validarEntrada(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("Este campo no puede estar vacio.")


def insertarUsuario():
    idUsuario = validarEntrada("Ingrese el numero de documento: ")
    
    if usuarioExiste(idUsuario):
        print("Error: Este usuario ya existe.")
        return
    
    nombre = validarEntrada("Ingrese el nombre: ")
    apellido = validarEntrada("Ingrese el apellido: ")
    celular = validarEntrada("Ingrese el celular: ")
    correo = validarEntrada("Ingrese el correo: ")

    cursor.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?, ?)", (idUsuario, nombre, apellido, celular, correo))
    conexion.commit()
    print("Usuario agregado correctamente.")

def mostrarUsuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    if usuarios:
        print("\nLista de Usuarios:")
        print("ID\t|Nombre\tApellido\tCelular\t\tCorreo")
        print("-" * 60) 

        for usuario in usuarios:
            print(f"{usuario[0]}\t|{usuario[1]}\t{usuario[2]}\t{usuario[3]}\t{usuario[4]}")
    else:
        print("No hay usuarios registrados.")


def buscarUsuario():
    idUsuario = validarEntrada("Ingrese el numero de documento a buscar: ")
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (idUsuario,))
    usuario = cursor.fetchone()
    if usuario:
        print(f"Usuario encontrado: ID: {usuario[0]} - Nombre: {usuario[1]} {usuario[2]} - Celular: {usuario[3]} - Correo: {usuario[4]}")
    else:
        print("Usuario no encontrado.")


def actualizarUsuario():
    idUsuario = validarEntrada("Ingrese el numero de documento del usuario a actualizar: ")
    
    if not usuarioExiste(idUsuario):
        print("Error: Usuario no encontrado.")
        return
    
    print("\n¿Qué desea actualizar?")
    print("1. Nombre")
    print("2. Apellido")
    print("3. Celular")
    print("4. Correo")
    
    opcion = input("Seleccione una opcion: ")
    campos = {"1": "nombre", "2": "apellido", "3": "celular", "4": "correo"}

    if opcion in campos:
        nuevoValor = validarEntrada(f"Ingrese el nuevo {campos[opcion]}: ")
        cursor.execute(f"UPDATE usuarios SET {campos[opcion]} = ? WHERE id = ?", (nuevoValor, idUsuario))
        conexion.commit()
        print("Usuario actualizado correctamente.")
    else:
        print("Opcion no valida.")

def eliminarUsuario():
    idUsuario = validarEntrada("Ingrese el numero de documento del usuario a eliminar: ")
    
    if not usuarioExiste(idUsuario):
        print("Error: Usuario no encontrado.")
        return

    confirmacion = input("¿Esta seguro de eliminar este usuario? (s/n): ").strip().lower()
    
    if confirmacion == "s":
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (idUsuario,))
        conexion.commit()
        print("Usuario eliminado correctamente.")
    else:
        print("Operacion cancelada.")

# Menu principal
def menu():
    while True:
        print("-" * 60) 
        print("=== Menu CRUD ===")
        print("1. Insertar Usuario")
        print("2. Mostrar Usuarios")
        print("3. Buscar Usuario")
        print("4. Actualizar Usuario")
        print("5. Eliminar Usuario")
        print("6. Salir")
        print("-" * 60) 

        opcion = input("Seleccione una opcion: ")
        match opcion:
            case "1":
                insertarUsuario()
            case "2": 
                mostrarUsuarios()
            case "3": 
                buscarUsuario()
            case "4": 
                actualizarUsuario()
            case "5": 
                eliminarUsuario()
            case "6":
                print("Saliendo del programa...")
                break
            case _:
                print("Opcion no valida, intente nuevamente.")

menu()
conexion.close()
