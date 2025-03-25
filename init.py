#Importamos las clases
from clases import Producto, Proveedor, Venta, Compra

#listas con datos predeterminados 
productos = [ 
    Producto("prod001", "shampo", "Belleza", 10.50, 50, "Shampoo de uso diario"),
    Producto("prod002", "computador", "Tecnología", 800, 10, "Computador portátil")
]

proveedores = [
    Proveedor("p01", "Luxe Supplies Corp.", "3204567890", "Avenida El Poblado #45-123 Medellín"),
    Proveedor("p02", "Elite Global Traders", "3106543210", "Calle 93A #12-45 Bogotá")
]

ventas = [
    Venta("v1", "prod001", "cliente01", "2025-03-20", 5),
    Venta("v2", "prod002", "cliente02", "2025-03-21", 2)
]

compras = [
    Compra("c1", "prod001", "p01", "2025-03-15", 50),
    Compra("c2", "prod002", "p02", "2025-03-16", 30)
]

productosFile = 'productos.csv'
proveFile = 'proveedores.csv'
ventasFile = 'ventas.csv'
comprasFile = 'compras.csv'

#Crea un archivo si necesita ser creado
def writeDataInit():
    global productos, proveedores, ventas, compras

    archivos = [productosFile, proveFile, ventasFile, comprasFile]
    objetos = [Producto, Proveedor, Venta, Compra] 
    datos = [productos, proveedores, ventas, compras]

    for i in range(0, len(archivos)-1):
        try:
            with open(archivos[i], 'x') as file:
                writeData(archivos[i], datos[i])
        except FileExistsError:
            generateData(archivos[i], datos[i], objetos[i])

#Genera un header según el archivo que se vaya a escribir
def createHeader(archivo):
    header = ""
    if archivo == productosFile:
        header = "ID del Producto, Nombre, Categoría, Precio, Stock, Descripción\n"
    elif archivo == proveFile:
        header = "ID del Proveedor, Nombre, Contacto, Dirección\n"
    elif archivo == ventasFile:
        header = "ID de Venta, ID del Producto, ID del Cliente, Fecha de Venta, Cantidad\n"
    else:
        header = "ID de Compra, ID de Producto, ID del Proveedor, Fecha de Compra, Cantidad\n"

    return header

#Escribe el archivo con header y los datos
def writeData(archivo, datos):
    with open(archivo, 'w') as file:
        file.write(createHeader(archivo))
        for dato in datos:
            file.write(f"{dato}\n")

#Si el archivo ya existe, vacía las listas y las actualiza.
def generateData(archivo, datos, tipo):
    datos.clear() #Vacía la lista de datos
    with open(archivo, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]: #Salta la primera línea
            line = line.strip().split(",") #Crea una lista que contiene toda la informacion del objeto
            obj = tipo(*line) #Crea un nuevo objeto usando la información
            datos.append(obj) #Añade este objeto a la lista de datos
            
writeDataInit() 