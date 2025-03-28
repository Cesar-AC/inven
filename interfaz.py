#Importamos la librería streamlit junto a los datos iniciales
import streamlit as st
from funciones import *

#Esta clase contiene/actúa como la interfaz
class dashboard:
    
    def __init__(self):
        #Le da un título a la pestaña
        st.set_page_config(page_title = "StockWise Dashboard", layout = "wide")
        
        #Guarda los datos importados en atributos propios de la clase
        if "productos" not in st.session_state:
            self.recargar_productos()
        if "proveedores" not in st.session_state:
            self.recargar_proveedores()
        if "ventas" not in st.session_state:
            self.recargar_ventas()
        if "compras" not in st.session_state:
            self.recargar_compras()
        
        self.sidebar()
        self.mostrar_contenido()

    def recargar_productos(self):
        from funciones import productos  # vuelve a cargar desde init
        st.session_state["productos"] = productos

    def recargar_proveedores(self):
        from funciones import proveedores  # vuelve a cargar desde init
        st.session_state["proveedores"] = proveedores

    def recargar_ventas(self):
        from funciones import ventas  # vuelve a cargar desde init
        st.session_state["ventas"] = ventas

    def recargar_compras(self):
        from funciones import compras  # vuelve a cargar desde init
        st.session_state["compras"] = compras
    
    #Crea el menú lateral con las respectivas opciones
    def sidebar(self):
        with st.sidebar:
            st.header("📊 StockWise Dashboard")
            self.opcion = st.radio("Ir a:", [
                "Home", "Productos", "Proveedores", "Ventas", "Compras",
                "Reportes"
            ])

    #la opción seleccionada en la interfaz
    def mostrar_contenido(self):
        if self.opcion == "Home":
            self.home()
        elif self.opcion == "Productos":
            self.showProductos()
        elif self.opcion == "Proveedores":
            self.showProveedores()
        elif self.opcion == "Ventas":
            self.showVentas()
        elif self.opcion == "Compras":
            self.showCompras()
        elif self.opcion == "Reportes":
            self.reportes()

    def home(self):
        st.title("🏠 Home")
        st.subheader("Bienvenido al Home")
    
    def showProductos(self):
        st.title("📦 Productos")
        if 'modo' not in st.session_state:
            st.session_state.modo = 'ver'  # Puede ser: 'ver', 'agregar', 'filtrar', 'editar' y 'eliminar'
        
        # Creamos contenedores vacíos para header y botones
        col1, col2 = st.columns(2)
        header_placeholder = col1.empty()
        buttons_placeholder = col2.empty()

        # Botones dinámicos
        with buttons_placeholder.container():
            col1b, col2b = st.columns(2)
            with col1b:
                if st.session_state.modo != 'ver':
                    if st.button("📋Ver Productos"):
                        st.session_state.modo = 'ver'
                        st.rerun()
                else:
                    if st.button("🛒Añadir Producto"):
                        st.session_state.modo = 'agregar'
                        st.rerun()
            with col2b:
                if st.session_state.modo != 'filtrar':
                    if st.button("🗂️Filtrar Productos"):
                        st.session_state.modo = 'filtrar'
                        st.rerun()
                else:
                    if st.button("🛒Añadir Producto"):
                        st.session_state.modo = 'agregar'
                        st.rerun()

        # Header dinámico
        with header_placeholder.container():
            if st.session_state.modo == 'ver':
                st.subheader("Estás viendo los productos")
            elif st.session_state.modo == 'agregar':
                st.subheader("Añadiendo Producto")
            elif st.session_state.modo == 'filtrar':
                st.subheader("Filtrando Productos")
            elif st.session_state.modo == 'editar':
                st.subheader("Editando Producto")
        
        # Contenido dinámico
        if st.session_state.modo == 'ver':
            mostrarDatos(
                productos, 
                ["ID del Producto", "Nombre", "Categoría", "Precio", "Stock", "Descripción", "Opciones"],
                ["idProducto", "nombre", "categoria", "precio", "stock", "descripcion"],
                "prod",
                actualizarP,
                eliminarP
            )
        elif st.session_state.modo == 'agregar':
            addProducto(self.recargar_productos)
        elif st.session_state.modo == 'filtrar':
            filtrarProductos(st.session_state["productos"])
        elif st.session_state.modo == 'editar':
            actualizarP(st.session_state.id_editando, self.recargar_productos)
        elif st.session_state.modo == 'eliminar':
            eliminarP(st.session_state.id_eliminando, self.recargar_productos)

    def showProveedores(self):
        st.title("🚚 Proveedores")
        if 'modo' not in st.session_state:
            st.session_state.modo = 'ver'  # Puede ser: 'ver', 'agregar'
        
        # Creamos contenedores vacíos para header y botones
        col1, col2 = st.columns(2)
        header_placeholder = col1.empty()
        buttons_placeholder = col2.empty()

        # Botones dinámicos
        with buttons_placeholder.container():
            col1b = st.columns(1)[0]
            with col1b:
                if st.session_state.modo != 'ver':
                    if st.button("📋Ver Proveedores"):
                        st.session_state.modo = 'ver'
                        st.rerun()
                else:
                    if st.button("🛒Añadir Proveedor"):
                        st.session_state.modo = 'agregar'
                        st.rerun()

        # Header dinámico
        with header_placeholder.container():
            if st.session_state.modo == 'ver':
                st.subheader("Estás viendo los proveedores")
            elif st.session_state.modo == 'agregar':
                st.subheader("Añadiendo proveedores")
        
        # Contenido dinámico
        if st.session_state.modo == 'ver':
            mostrarDatos(
                proveedores, 
                ["ID del Proveedor", "Nombre", "Contacto", "Dirección", "Opciones"],
                ["idProveedor", "nombre", "contacto", "direccion"],
                "p",
                actualizarPv,
                eliminarPv
            )
        elif st.session_state.modo == 'agregar':
            addProveedor(self.recargar_proveedores)
        elif st.session_state.modo == 'editar':
            actualizarPv(st.session_state.id_editando, self.recargar_proveedores)
        elif st.session_state.modo == 'eliminar':
            eliminarPv(st.session_state.id_eliminando, self.recargar_proveedores)

    def showVentas(self):
        st.title("💰 Ventas")
        if 'modo' not in st.session_state:
            st.session_state.modo = 'ver'  # Puede ser: 'ver', 'agregar', 'editar' o 'eliminar'
        
        # Creamos contenedores vacíos para header y botones
        col1, col2 = st.columns(2)
        header_placeholder = col1.empty()
        buttons_placeholder = col2.empty()

        # Botones dinámicos
        with buttons_placeholder.container():
            col1b = st.columns(1)[0]
            with col1b:
                if st.session_state.modo != 'ver':
                    if st.button("📋Ver Ventas"):
                        st.session_state.modo = 'ver'
                        st.rerun()
                else:
                    if st.button("🛒Añadir Venta"):
                        st.session_state.modo = 'agregar'
                        st.rerun()

        # Header dinámico
        with header_placeholder.container():
            if st.session_state.modo == 'ver':
                st.subheader("Estás viendo las ventas")
            elif st.session_state.modo == 'agregar':
                st.subheader("Añadiendo venta")
        
        # Contenido dinámico
        if st.session_state.modo == 'ver':
            mostrarDatos(
                ventas, 
                ["ID de Venta", "ID del Producto", "ID del Cliente", "Fecha de Venta", "Cantidad", "Opciones"],
                ["idVenta", "idProducto", "idCliente", "fechaDeVenta", "cantidad"],
                "v",
                actualizarV,
                eliminarV
            )
        elif st.session_state.modo == 'agregar':
            addVenta(self.recargar_ventas, self.recargar_productos)
        elif st.session_state.modo == 'editar':
            actualizarV(st.session_state.id_editando, self.recargar_ventas)
        elif st.session_state.modo == 'eliminar':
            eliminarV(st.session_state.id_eliminando, self.recargar_ventas)
            
    def showCompras(self):
        st.title("🛒 Compras")
        if 'modo' not in st.session_state:
            st.session_state.modo = 'ver'  # Puede ser: 'ver', 'agregar'
        
        # Creamos contenedores vacíos para header y botones
        col1, col2 = st.columns(2)
        header_placeholder = col1.empty()
        buttons_placeholder = col2.empty()

        # Botones dinámicos
        with buttons_placeholder.container():
            col1b = st.columns(1)[0]
            with col1b:
                if st.session_state.modo != 'ver':
                    if st.button("📋Ver Compras"):
                        st.session_state.modo = 'ver'
                        st.rerun()
                else:
                    if st.button("🛒Añadir Compra"):
                        st.session_state.modo = 'agregar'
                        st.rerun()

        # Header dinámico
        with header_placeholder.container():
            if st.session_state.modo == 'ver':
                st.subheader("Estás viendo las compras")
            elif st.session_state.modo == 'agregar':
                st.subheader("Añadiendo compra")
        
        # Contenido dinámico
        if st.session_state.modo == 'ver':
            mostrarDatos(
                compras, 
                ["ID de Compra", "ID del Producto", "ID del Proveedor", "Fecha de Compra", "Cantidad", "Opciones"],
                ["idCompra", "idProducto", "idProveedor", "fechaDeCompra", "cantidad"],
                "c",
                actualizarC,
                eliminarC
            )
        elif st.session_state.modo == 'agregar':
            addCompra(self.recargar_compras, self.recargar_productos)
        elif st.session_state.modo == 'editar':
            actualizarC(st.session_state.id_editando, self.recargar_compras)
        elif st.session_state.modo == 'eliminar':
            eliminarC(st.session_state.id_eliminando, self.recargar_compras)
                        
    def reportes(self):
        st.title("📑 Reportes")
        st.subheader("Estás viendo los reportes")

        opcion = st.selectbox("📌 Elige un reporte:", [
            "Seleccione una opción",
            "Productos con menor stock",
            "Proveedores más frecuentes",
            "Ventas por período de tiempo",
            "Productos más vendidos"
        ]) 

        if opcion == "Productos con menor stock":
            with open("productos.csv", "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()[1:]  # Omitir encabezado

            productos_bajo_stock = []

            for linea in lineas:
                datos = linea.strip().split(",")  # Separar los valores por coma
                id_producto, nombre, categoria, precio, stock, descripcion = datos
                stock = int(stock)  # Convertir el stock a número

                if stock <= 20:  # Filtrar productos con stock menor o igual a 20
                    productos_bajo_stock.append([id_producto, nombre, categoria, precio, stock, descripcion])

            st.write("📉 **Productos con stock menor o igual a 20:**")

            if productos_bajo_stock:
                # Crear columnas para los encabezados
                cols = st.columns(6)
                encabezados = ["ID Producto", "Nombre", "Categoría", "Precio", "Stock", "Descripción"]

                for col, titulo in zip(cols, encabezados):
                    col.write(f"**{titulo}**")  # Encabezados en negrita

                # Mostrar productos en filas
                for producto in productos_bajo_stock:
                    cols = st.columns(6)
                    for col, dato in zip(cols, producto):
                        col.write(dato)

            else:
                st.write("✅ Todos los productos tienen un stock mayor a 20.")

        
        elif opcion == "Proveedores más frecuentes":
            compras = st.session_state["compras"]  

            # Diccionarios para contar compras y unidades por proveedor
            compras_por_proveedor = {}
            unidades_por_proveedor = {}

            for compra in compras:
                proveedor = compra.idProveedor  
                cantidad = compra.cantidad  

                if proveedor in compras_por_proveedor:
                    compras_por_proveedor[proveedor] += 1
                    unidades_por_proveedor[proveedor] += cantidad
                else:
                    compras_por_proveedor[proveedor] = 1
                    unidades_por_proveedor[proveedor] = cantidad

            
            lista_proveedores = []
            for proveedor in compras_por_proveedor:
                lista_proveedores.append((proveedor, compras_por_proveedor[proveedor], unidades_por_proveedor[proveedor]))

            
            for i in range(len(lista_proveedores) - 1):
                for j in range(len(lista_proveedores) - i - 1):
                    if lista_proveedores[j][1] < lista_proveedores[j + 1][1]:
                        lista_proveedores[j], lista_proveedores[j + 1] = lista_proveedores[j + 1], lista_proveedores[j]
                    elif lista_proveedores[j][1] == lista_proveedores[j + 1][1]:  # Empate en compras
                        if lista_proveedores[j][2] < lista_proveedores[j + 1][2]:  # Comparar unidades
                            lista_proveedores[j], lista_proveedores[j + 1] = lista_proveedores[j + 1], lista_proveedores[j]

            
            top_proveedores = lista_proveedores[:3]

            
            st.write("🏢 **Proveedores más frecuentes:**")
            
            if top_proveedores:
                for proveedor in top_proveedores:
                    st.write(f"- Proveedor {proveedor[0]} :   {proveedor[1]} compras")
            else:
                st.write("❌ No hay suficientes datos")


        elif opcion == "Ventas por período de tiempo":
            fecha_inicio = st.date_input("📅 Fecha de inicio")
            fecha_fin = st.date_input("📅 Fecha de fin")
            ventas_filtradas = ventas_por_periodo(str(fecha_inicio), str(fecha_fin))

            if ventas_filtradas:
                st.write("🛒 **Ventas en el período seleccionado:**")

                cols = st.columns(5)
                encabezados = ["ID Venta", "ID Producto", "ID Cliente", "Fecha", "Cantidad"]

                for col, titulo in zip(cols, encabezados):
                    col.write(f"**{titulo}**")

                for venta in ventas_filtradas:
                    cols = st.columns(5)
                    datos = [venta.idVenta, venta.idProducto, venta.idCliente, venta.fechaDeVenta, venta.cantidad]

                    for col, dato in zip(cols, datos):
                        col.write(dato)

            else:
                st.write("❌ No hay ventas en el período seleccionado.")

        elif opcion == "Productos más vendidos":
            st.write("🔥 **Productos más vendidos (4+ unidades):**")

            conteo_ventas = {}

            # Leer el archivo línea por línea
            with open("ventas.csv", "r") as archivo:
                next(archivo) 
                for linea in archivo:
                    datos = linea.strip().split(",")  
                    producto_id = datos[1]  
                    cantidad = int(datos[4])  

                    
                    if producto_id in conteo_ventas:
                        conteo_ventas[producto_id] += cantidad
                    else:
                        conteo_ventas[producto_id] = cantidad

            productos_filtrados = [(producto, cantidad) for producto, cantidad in conteo_ventas.items() if cantidad >= 4]

           
            if productos_filtrados:
                for producto in productos_filtrados:
                    st.write(f"- Producto {producto[0]}: {producto[1]} unidades vendidas")
            else:
                st.write("❌ No hay productos con 4 o más unidades vendidas.")
