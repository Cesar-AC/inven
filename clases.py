#Dentro de este archivo se encuentran cuatro clases, cada una contiene un como constructor y un 'def __str__'
#para devolver sus atributos separados por comas (útil al momento de trabajar con archivos csv)
class Producto:
    def __init__(self, idProducto, nombre, categoria, precio, stock, descripcion):
        self.idProducto = idProducto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.descripcion = descripcion
    def __str__(self):
        return f"{self.idProducto},{self.nombre},{self.categoria},{self.precio},{self.stock},{self.descripcion}"

class Proveedor:
    def __init__(self, idProveedor, nombre, contacto, direccion):
        self.idProveedor = idProveedor
        self.nombre = nombre
        self.contacto = contacto
        self.direccion = direccion
    def __str__(self):
        return f"{self.idProveedor},{self.nombre},{self.contacto},{self.direccion}"

class Venta:
    def __init__(self, idVenta, idProducto, idCliente, fechaDeVenta, cantidad):
        self.idVenta = idVenta
        self.idProducto = idProducto
        self.idCliente = idCliente
        self.fechaDeVenta = fechaDeVenta
        self.cantidad = cantidad
    def __str__(self):
        return f"{self.idVenta},{self.idProducto},{self.idCliente},{self.fechaDeVenta},{self.cantidad}"

class Compra:
    def __init__(self, idCompra, idProducto, idProveedor, fechaDeCompra, cantidad):
        self.idCompra = idCompra
        self.idProducto = idProducto
        self.idProveedor = idProveedor
        self.fechaDeCompra = fechaDeCompra
        self.cantidad = cantidad
    def __str__(self):
        return f"{self.idCompra},{self.idProducto},{self.idProveedor},{self.fechaDeCompra},{self.cantidad}"