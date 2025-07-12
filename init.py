#Importamos las clases
from modelo.clases import *

#listas con datos predeterminados 
productos = [ 
    Producto("prod001","Shampoo","Belleza","10.5","50","Shampoo de uso diario"),
    Producto("prod002","Crema Facial","Belleza","25","40","Hidratante para todo tipo de piel"),
    Producto("prod003","Computador","Tecnología","800","10","Computador portátil"),
    Producto("prod004","Mouse","Tecnología","20","30","Mouse óptico ergonómico"),
    Producto("prod005","Nevado de Galleta","Alimentos","14.5","129381","Bebida de café con galleta Oreo y crema chantilly"),
    Producto("prod006","Pan Integral","Alimentos","4","100","Pan de harina integral y semillas"),
    Producto("prod007","Zapatillas Deportivas","Ropa y Calzado","60","30","Zapatillas cómodas para correr"),
    Producto("prod008","Chaqueta de Cuero","Ropa y Calzado","120","10","Chaqueta clásica de cuero genuino"),
    Producto("prod009","Cámara DSLR","Electrónica","1200","5","Cámara profesional con lente intercambiable"),
    Producto("prod010","Smartwatch","Electrónica","150","12","Reloj inteligente con múltiples funciones"),
    Producto("prod011","Set de Ollas","Hogar","80","15","Ollas de acero inoxidable con antiadherente"),
    Producto("prod012","Sofá de Cuero","Hogar","700","5","Sofá de 3 plazas en cuero negro"),
    Producto("prod013","Bicicleta Montaña","Deportes","500","7","Bicicleta resistente para todo terreno"),
    Producto("prod014","Pesa Rusa 10kg","Deportes","40","15","Ideal para entrenamiento funcional"),
    Producto("prod015","Juguete Educativo","Juguetes","20","50","Juego didáctico para niños"),
    Producto("prod016","Carro de Control Remoto","Juguetes","50","20","Alcance de hasta 20 metros")
]

proveedores = [
    Proveedor("p001","Luxe Supplies Corp.","3204567890","Avenida El Poblado #45-123 Medellín"),
    Proveedor("p002","Elite Global Traders","3106543210","Calle 93A #12-45 Bogotá"),
    Proveedor("p003","Distribuidora Andes","3157896543","Carrera 50 #30-20 Cali"),
    Proveedor("p004","Innovatech Solutions","3229874561","Calle 100 #25-30 Barranquilla"),
    Proveedor("p005","Alimentos del Valle","3112345678","Avenida Central #5-67 Bucaramanga"),
    Proveedor("p006","Hogar y Estilo S.A.","3187654321","Calle 45 #10-15 Cartagena")
]

ventas = [
    Venta("v001","prod001","cliente01","20-03-2025","5"),
    Venta("v002","prod002","cliente02","21-03-2025","2"),
    Venta("v003","prod005","cliente03","22-03-2025","3"),
    Venta("v004","prod007","cliente04","23-03-2025","1"),
    Venta("v005","prod008","cliente10","23-03-2025","2"),
    Venta("v006","prod003","cliente09","24-03-2025","1"),
    Venta("v007","prod010","cliente05","24-03-2025","4"),
    Venta("v008","prod012","cliente06","25-03-2025","2"),
    Venta("v009","prod016","cliente08","25-03-2025","3"),
    Venta("v010","prod014","cliente07","26-03-2025","6")
]

compras = [
    Compra("c001","prod001","p001","15-03-2025","50"),
    Compra("c002","prod002","p002","16-03-2025","30"),
    Compra("c003","prod005","p005","10-02-2025","100"),
    Compra("c004","prod007","p003","25-01-2025","20"),
    Compra("c005","prod008","p004","05-03-2025","15"),
    Compra("c006","prod003","p002","18-02-2025","10"),
    Compra("c007","prod010","p006","30-01-2025","40"),
    Compra("c008","prod012","p005","22-02-2025","5"),
    Compra("c009","prod016","p001","12-03-2025","25"),
    Compra("c010","prod014","p003","15-01-2025","35")
]


productosFile = 'productos.csv'
proveFile = 'proveedores.csv'
ventasFile = 'ventas.csv'
comprasFile = 'compras.csv'


# Crea un archivo si no existe, con codificación utf-8 y BOM
def writeDataInit():
    global productos, proveedores, ventas, compras

    archivos = [productosFile, proveFile, ventasFile, comprasFile]
    objetos  = [Producto,   Proveedor,   Venta,      Compra] 
    datos    = [productos,  proveedores, ventas,     compras]

    for archivo, tipo, lista in zip(archivos, objetos, datos):
        try:
            # 'x' + encoding utf-8-sig (pone BOM al inicio)
            with open(archivo, 'x', encoding='utf-8-sig') as f:
                writeData(archivo, lista)
        except FileExistsError:
            generateData(archivo, lista, tipo)

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
    header = createHeader(archivo)
    with open(archivo, 'w', encoding='utf-8-sig') as f: 
        f.write(header)
        for dato in datos:
            f.write(f"{dato}\n")

# generateData lee siempre con utf-8
def generateData(archivo, datos, tipo):
    datos.clear()
    with open(archivo, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()[1:]  # salto header
    for line in lines:
        parts = line.strip().split(",")
        datos.append(tipo(*parts))

writeDataInit() #Ejecuta la función para crear los archivos si no existen