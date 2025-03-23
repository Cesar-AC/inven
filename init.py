from clases import producto, proveedor, venta, compra

productos = [producto("shampo"), producto("computador")]
proveedores = [proveedor("d1"), proveedor("ara")]
ventas = [venta("venta1"), venta("venta2")]
compras = [compra("compra1"), compra("compra2")]

productosFile = 'productos.csv'
proveFile = 'proveedores.csv'
ventasFile = 'ventas.csv'
comprasFile = 'compras.csv'


def writeDataInit():
    global productos, proveedores, ventas, compras

    archivos = [productosFile, proveFile, ventasFile, comprasFile]
    datos = [productos, proveedores, ventas, compras]
    objectos = [producto, proveedor, venta, compra]

    for i in range(0, len(archivos)-1):
        try:
            with open(archivos[i], 'x') as file:
                writeData(archivos[i], datos[i])
        except FileExistsError:
            generateData(archivos[i], datos[i], objectos[i])

def createHeader(archivo):
    header = ""
    if archivo == productosFile:
        header = "ID_Producto, Nombre, Categoría, Precio, Stock, Descripción\n"
    elif archivo == proveFile:
        header = "ID_Proveedor, Nombre, Contacto, Dirección\n"
    elif archivo == ventasFile:
        header = "ID_Venta, ID_Producto, ID_Cliente, Fecha_Venta, Cantidad\n"
    else:
        header = "ID_Compra, ID_Producto, ID_Proveedor, Fecha_Compra, Cantidad\n"

    return header

def writeData(archivo, datos):
    with open(archivo, 'w') as file:
        file.write(createHeader(archivo))
        for dato in datos:
            file.write(f"{dato}\n")

def generateData(archivo, datos, tipo):
    datos.clear()
    with open(archivo, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            line = line.split()
            tipo(line)
            datos.append(tipo)

    return datos

writeDataInit()
print("ejecuto")