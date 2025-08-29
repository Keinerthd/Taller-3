import csv
import os

CLIENTES_FILE = "clientes.csv"
PEDIDOS_FILE = "pedidos.csv"


# ---------------- UTILIDADES ----------------
def inicializar_archivos():
    
    if not os.path.exists(CLIENTES_FILE):
        with open(CLIENTES_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id_cliente", "nombre", "apellido", "telefono", "activo"])
    if not os.path.exists(PEDIDOS_FILE):
        with open(PEDIDOS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id_pedido", "id_cliente", "producto", "precio", "cantidad", "activo"])


def leer_csv(nombre_archivo):
   
    with open(nombre_archivo, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def escribir_csv(nombre_archivo, lista, fieldnames):
    
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lista)


def generar_id(lista, campo_id):
    
    if not lista:
        return 1
    return max(int(item[campo_id]) for item in lista) + 1


# ---------------- CLIENTES ----------------
def registrar_cliente():
    clientes = leer_csv(CLIENTES_FILE)
    id_cliente = generar_id(clientes, "id_cliente")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    telefono = input("Teléfono: ")
    clientes.append({
        "id_cliente": id_cliente,
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "activo": "1"
    })
    escribir_csv(CLIENTES_FILE, clientes, clientes[0].keys())
    print(" Cliente registrado.")


def listar_clientes():
    clientes = leer_csv(CLIENTES_FILE)
    print("\n--- LISTA DE CLIENTES ---")
    for c in clientes:
        estado = "Activo" if c["activo"] == "1" else "Inactivo"
        print(f"{c['id_cliente']} - {c['nombre']} {c['apellido']} ({c['telefono']}) [{estado}]")


def eliminar_cliente():
    clientes = leer_csv(CLIENTES_FILE)
    id_cliente = input("Ingrese ID del cliente a eliminar: ")
    encontrado = False
    for c in clientes:
        if c["id_cliente"] == id_cliente and c["activo"] == "1":
            c["activo"] = "0"
            encontrado = True
            break
    if encontrado:
        escribir_csv(CLIENTES_FILE, clientes, clientes[0].keys())
        print("Cliente eliminado lógicamente.")
    else:
        print(" Cliente no encontrado o ya estaba inactivo.")


# ---------------- PEDIDOS ----------------
def registrar_pedido():
    clientes = leer_csv(CLIENTES_FILE)
    pedidos = leer_csv(PEDIDOS_FILE)

    id_cliente = input("Ingrese ID del cliente: ")
    if not any(c["id_cliente"] == id_cliente and c["activo"] == "1" for c in clientes):
        print("Cliente no existe o está inactivo.")
        return

    id_pedido = generar_id(pedidos, "id_pedido")
    producto = input("Producto: ")
    precio = input("Precio (opcional, ENTER si no aplica): ") or "0"
    cantidad = input("Cantidad (opcional, ENTER si no aplica): ") or "1"

    pedidos.append({
        "id_pedido": id_pedido,
        "id_cliente": id_cliente,
        "producto": producto,
        "precio": precio,
        "cantidad": cantidad,
        "activo": "1"
    })
    escribir_csv(PEDIDOS_FILE, pedidos, pedidos[0].keys())
    print("Pedido registrado.")


def listar_pedidos_cliente():
    pedidos = leer_csv(PEDIDOS_FILE)
    id_cliente = input("Ingrese ID del cliente: ")
    print(f"\n--- PEDIDOS DEL CLIENTE {id_cliente} ---")
    for p in pedidos:
        if p["id_cliente"] == id_cliente and p["activo"] == "1":
            print(f"{p['id_pedido']} - {p['producto']} x{p['cantidad']} (${p['precio']})")


# ---------------- VENTAS ----------------
def guardar_venta():
    pedidos = leer_csv(PEDIDOS_FILE)
    clientes = leer_csv(CLIENTES_FILE)

    id_cliente = input("ID del cliente: ")
    if not any(c["id_cliente"] == id_cliente and c["activo"] == "1" for c in clientes):
        print("Cliente no válido.")
        return

    producto = input("Producto: ")
    precio = float(input("Precio: "))
    cantidad = int(input("Cantidad: "))

    id_pedido = generar_id(pedidos, "id_pedido")
    pedidos.append({
        "id_pedido": id_pedido,
        "id_cliente": id_cliente,
        "producto": producto,
        "precio": str(precio),
        "cantidad": str(cantidad),
        "activo": "1"
    })
    escribir_csv(PEDIDOS_FILE, pedidos, pedidos[0].keys())
    print(" Venta registrada.")


def listar_ventas_cliente():
    pedidos = leer_csv(PEDIDOS_FILE)
    nombre_cliente = input("Nombre del cliente: ")

    # Buscar cliente por nombre
    clientes = leer_csv(CLIENTES_FILE)
    cliente = next((c for c in clientes if c["nombre"] == nombre_cliente and c["activo"] == "1"), None)
    if not cliente:
        print("Cliente no encontrado.")
        return

    id_cliente = cliente["id_cliente"]
    ventas = [p for p in pedidos if p["id_cliente"] == id_cliente and p["activo"] == "1"]

    print(f"\n--- VENTAS DEL CLIENTE {nombre_cliente} ---")
    total = 0
    for v in ventas:
        precio = float(v["precio"])
        cantidad = int(v["cantidad"])
        subtotal = precio * cantidad
        total += subtotal
        print(f"{v['producto']} x{cantidad} = ${subtotal:.2f}")

    print(f"TOTAL: ${total:.2f}")


# ---------------- MENÚ ----------------
def menu():
    inicializar_archivos()
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Eliminar cliente")
        print("4. Registrar pedido")
        print("5. Listar pedidos de un cliente")
        print("6. Guardar una venta")
        print("7. Listar ventas de un cliente")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1": registrar_cliente()
        elif opcion == "2": listar_clientes()
        elif opcion == "3": eliminar_cliente()
        elif opcion == "4": registrar_pedido()
        elif opcion == "5": listar_pedidos_cliente()
        elif opcion == "6": guardar_venta()
        elif opcion == "7": listar_ventas_cliente()
        elif opcion == "8":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
