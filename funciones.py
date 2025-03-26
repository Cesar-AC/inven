import streamlit as st
from unidecode import unidecode
from datetime import datetime
from clases import Producto, Proveedor, Venta
from init import generateData, productos, proveedores, ventas

# Reporte 1: Producto con menor stock
def producto_menor_stock(self):
    if "productos" not in st.session_state:
        return "No hay productos"

    menor = st.session_state["productos"][0]
    for producto in st.session_state["productos"]:
        if producto.stock < menor.stock:
            menor = producto
    return menor

# Reporte 2: Proveedores más frecuentes
def proveedores_mas_frecuentes(self):
    conteo = {}
    for compra in self.compras:
        id_proveedor = compra.idProveedor
        if id_proveedor in conteo:
            conteo[id_proveedor] += 1
        else:
            conteo[id_proveedor] = 1

    # Ordenar de mayor a menor
    lista_ordenada = []
    for proveedor in conteo:
        lista_ordenada.append((proveedor, conteo[proveedor]))

    for i in range(len(lista_ordenada)):
        for j in range(i + 1, len(lista_ordenada)):
            if lista_ordenada[i][1] < lista_ordenada[j][1]:
                lista_ordenada[i], lista_ordenada[j] = lista_ordenada[j], lista_ordenada[i]

    return lista_ordenada

# Reporte 3: Ventas por período de tiempo
def ventas_por_periodo(self, fecha_inicio, fecha_fin):
    resultado = []
    for venta in self.ventas:
        if fecha_inicio <= venta.fechaDeVenta <= fecha_fin:
            resultado.append(venta)
    return resultado

# Reporte 4: Productos más vendidos
def productos_mas_vendidos(self):
    conteo = {}
    for venta in self.ventas:
        id_producto = venta.idProducto
        if id_producto in conteo:
            conteo[id_producto] += 1
        else:
            conteo[id_producto] = 1

    # Ordenar de mayor a menor
    lista_ordenada = []
    for producto in conteo:
        lista_ordenada.append((producto, conteo[producto]))

    for i in range(len(lista_ordenada)):
        for j in range(i + 1, len(lista_ordenada)):
            if lista_ordenada[i][1] < lista_ordenada[j][1]:
                lista_ordenada[i], lista_ordenada[j] = lista_ordenada[j], lista_ordenada[i]

    return lista_ordenada

#Funcion añadir producto
def addProducto(recargar):
    st.write("Ingrese los datos del nuevo producto:")
    cols = st.columns(3)
    nombre = cols[0].text_input("Nombre")
    categoria = cols[1].text_input("Categoría")
    precio = cols[2].text_input("Precio")

    cols = st.columns(2)
    stock = cols[0].text_input("Stock")
    desc = cols[1].text_input("Descripción")

    if st.button("Guardar"):
        id = buscarNextID()  # o como estés generando los IDs
        with open('productos.csv', 'a') as file:
            file.write(f"{id},{nombre},{categoria},{precio},{stock},{desc}\n")
        st.success("✅ Datos guardados")
        generateData('productos.csv', productos, Producto)
        recargar()  # recarga el array de productos en la interfaz
        st.session_state.modo = 'ver'
        st.rerun()

#Funcion añadir proveedor
def addProveedor(recargar):
    st.write("Ingrese los datos del nuevo proveedor:")
    cols = st.columns(3)
    nombre = cols[0].text_input("Nombre")
    contacto = cols[1].text_input("Contacto")
    direccion = cols[2].text_input("Dirección")

    if st.button("Guardar"):
        id = buscarNextIDProv()  # o como estés generando los IDs
        with open('proveedores.csv', 'a') as file:
            file.write(f"{id},{nombre},{contacto},{direccion}\n")
        st.success("✅ Datos guardados")
        generateData('proveedores.csv', proveedores, Proveedor)
        recargar()  # recarga el array de los proveedores en la interfaz
        st.session_state.modo = 'ver'
        st.rerun()

#Funcion añadir venta
def addVenta(recargar):
    st.write("Ingrese los datos de la venta:")
    cols = st.columns(3)
    idCliente = cols[0].text_input("ID del cliente")
    idProducto = cols[1].text_input("ID del Producto")
    cantidad = cols[2].text_input("Cantidad")
    fecha = datetime.now().strftime("%d-%m-%Y")

    if st.button("Guardar"):
        id = buscarNextIDV()  # o como estés generando los IDs
        with open('ventas.csv', 'a') as file:
            file.write(f"{id},{idCliente},{idProducto},{fecha},{cantidad}\n")
        st.success("✅ Datos guardados")
        generateData('ventas.csv', ventas, Venta)
        recargar()  # recarga el array de las ventas en la interfaz
        st.session_state.modo = 'ver'
        st.rerun()
    

def buscarNextID():
    last = productos[-1]
    lastID = last.idProducto
    lastID = int(lastID.replace('prod',''))
    nextID = f"prod00{lastID+1}"
    return nextID

def buscarNextIDProv():
    last = proveedores[-1]
    lastID = last.idProveedor
    lastID = int(lastID.replace('p',''))
    nextID = f"p0{lastID+1}"
    return nextID

def buscarNextIDV():
    last = ventas[-1]
    lastID = last.idVenta
    lastID = int(lastID.replace('v',''))
    nextID = f"v{lastID+1}"
    return nextID
    
def mostrarP(xproductos):
    cols = st.columns(6)
    valores = ["ID del Producto", "Nombre", "Categoría", "Precio", "Stock", "Descripción"]
    #Recorre cada par columna-valor y escribe en la columna 
    for col, val in zip(cols, valores): 
        with col:
            st.write(val)

    for producto in xproductos:
        with st.container(): #Agrupa las columnas dentro de un contenedor
            cols = st.columns(6)
            #Toma los atributos de cada producto y los guarda en valores
            valores = [
                producto.idProducto, producto.nombre, producto.categoria, producto.precio,                     
                producto.stock,producto.descripcion]
            #Escribe cada atributo del producto en su respectiva columna
            for col, val in zip(cols, valores):
                with col:
                    st.write(val)

def mostrarPv(xproveedores):
    cols = st.columns(4)
    valores = ["ID del Proveedor", "Nombre", "Contacto", "Dirección"]
    for col, val in zip(cols, valores):
        with col:
            st.write(val) 
    for proveedor in xproveedores:
        with st.container():
            cols = st.columns(4)
            valores = [proveedor.idProveedor, proveedor.nombre, proveedor.contacto, proveedor.direccion]
            for col, val in zip(cols, valores):
                with col:
                    st.write(val)

def mostrarV(xventas):
    cols = st.columns(5)    
    valores = ["ID de Venta", "ID del Producto", "ID del Cliente", "Fecha de Venta", "Cantidad"]
    for col, val in zip(cols, valores):
        with col:
            st.write(val)

    for venta in xventas:
        with st.container():
            cols = st.columns(5)
            valores = [venta.idVenta, venta.idProducto, venta.idCliente, venta.fechaDeVenta, venta.cantidad]
            for col, val in zip(cols, valores):
                with col:
                    st.write(val)

def filtrarProductos(xproductos):
    opcion = st.selectbox("🔎 Buscar productos por:", [
            "📄 Nombre",
            "📑 Categoría",
        ])
    
    if opcion == "📄 Nombre":
        cols = st.columns(1)
        nombre = cols[0].text_input("Nombre a buscar:")
        for producto in xproductos:
            if unidecode(producto.nombre.casefold()) == unidecode(nombre.casefold()):
                with st.container(): #Agrupa las columnas dentro de un contenedor
                    cols = st.columns(6)
                    #Toma los atributos de cada producto y los guarda en valores
                    valores = [
                        producto.idProducto, producto.nombre, producto.categoria, producto.precio,                     
                        producto.stock,producto.descripcion]
                    #Escribe cada atributo del producto en su respectiva columna
                    for col, val in zip(cols, valores):
                        with col:
                            st.write(val)

    elif opcion == "📑 Categoría":
        cols = st.columns(1)
        cat = cols[0].text_input("Categoría a buscar:")
        for producto in xproductos:
            if unidecode(producto.categoria.casefold()) == unidecode(cat.casefold()):
                with st.container(): #Agrupa las columnas dentro de un contenedor
                    cols = st.columns(6)
                    #Toma los atributos de cada producto y los guarda en valores
                    valores = [
                        producto.idProducto, producto.nombre, producto.categoria, producto.precio,                     
                        producto.stock,producto.descripcion]
                    #Escribe cada atributo del producto en su respectiva columna
                    for col, val in zip(cols, valores):
                        with col:
                            st.write(val)