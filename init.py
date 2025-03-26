#Importamos las clases
from clases import Producto, Proveedor, Venta, Compra

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
    Proveedor("p01","Luxe Supplies Corp.","3204567890","Avenida El Poblado #45-123 Medellín"),
    Proveedor("p02","Elite Global Traders","3106543210","Calle 93A #12-45 Bogotá"),
    Proveedor("p03","Distribuidora Andes","3157896543","Carrera 50 #30-20 Cali"),
    Proveedor("p04","Innovatech Solutions","3229874561","Calle 100 #25-30 Barranquilla"),
    Proveedor("p05","Alimentos del Valle","3112345678","Avenida Central #5-67 Bucaramanga"),
    Proveedor("p06","Hogar y Estilo S.A.","3187654321","Calle 45 #10-15 Cartagena")

]

ventas = [
    Venta("v01","prod001","cliente01","2025-03-20","5"),
    Venta("v02","prod002","cliente02","2025-03-21","2"),
    Venta("v03","prod005","cliente03","2025-03-22","3"),
    Venta("v04","prod007","cliente04","2025-03-23","1"),
    Venta("v05","prod008","cliente10","2025-03-23","2"),
    Venta("v06","prod003","cliente09","2025-03-24","1"),
    Venta("v07","prod010","cliente05","2025-03-24","4"),
    Venta("v08","prod012","cliente06","2025-03-25","2"),
    Venta("v09","prod016","cliente08","2025-03-25","3"),
    Venta("v10","prod014","cliente07","2025-03-26","6"),

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
    print("Creando archivos...")
    global productos, proveedores, ventas, compras

    archivos = [productosFile, proveFile, ventasFile, comprasFile]
    objetos = [Producto, Proveedor, Venta, Compra] 
    datos = [productos, proveedores, ventas, compras]

    for i in range(0, len(archivos)):
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