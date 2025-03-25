#Importamos la librería streamlit junto a los datos iniciales
import streamlit as st
from init import proveedores, ventas, compras
from funciones import producto_menor_stock, proveedores_mas_frecuentes, ventas_por_periodo, productos_mas_vendidos, addProducto, mostrarP, filtrarProductos

#Esta clase contiene/actúa como la interfaz
class dashboard:
    
    def __init__(self):

        #Le da un título a la pestaña
        st.set_page_config(page_title = "StockWise Dashboard", layout = "wide")
        
        #Guarda los datos importados en atributos propios de la clase
        if "productos" not in st.session_state:
            self.recargar_productos()
            
        self.proveedores = proveedores
        self.ventas = ventas
        self.compras = compras
        self.sidebar()
        self.mostrar_contenido()

    def recargar_productos(self):
        from funciones import productos  # vuelve a cargar desde init
        st.session_state["productos"] = productos
    
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
            st.session_state.modo = 'ver'  # Puede ser: 'ver', 'agregar', 'filtrar'
        
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
        
        # Contenido dinámico
        if st.session_state.modo == 'ver':
            mostrarP(st.session_state["productos"])
        elif st.session_state.modo == 'agregar':
            addProducto(self.recargar_productos)
        elif st.session_state.modo == 'filtrar':
            filtrarProductos()

    def showProveedores(self):
        st.title("🚚 Proveedores")
        st.subheader("Estás viendo los proveedores")
        cols = st.columns(4)
        valores = ["ID del Proveedor", "Nombre", "Contacto", "Dirección"]
        for col, val in zip(cols, valores):
            with col:
                st.write(val) 
        for proveedor in self.proveedores:
            with st.container():
                cols = st.columns(4)
                valores = [proveedor.idProveedor, proveedor.nombre, proveedor.contacto, proveedor.direccion]
                for col, val in zip(cols, valores):
                    with col:
                        st.write(val)

    def showVentas(self):
        st.title("💰 Ventas")
        st.subheader("Estás viendo las ventas")
        
        cols = st.columns(5)    
        valores = ["ID de Venta", "ID del Producto", "ID del Cliente", "Fecha de Venta", "Cantidad"]
        for col, val in zip(cols, valores):
            with col:
                st.write(val)

        
        for venta in self.ventas:
            with st.container():
                cols = st.columns(5)
                valores = [venta.idVenta, venta.idProducto, venta.idCliente, venta.fechaDeVenta, venta.cantidad]
                for col, val in zip(cols, valores):
                    with col:
                        st.write(val)
            
    def showCompras(self):
        st.title("🛒 Compras")
        st.subheader("Estás viendo las compras")
        
        cols = st.columns(5)
        valores = ["ID de Compra", "ID del Producto", "ID del Proveedor", "Fecha de Compra", "Cantidad"]
        for col, val in zip(cols, valores):
            with col:
                st.write(val)
                
        for compra in self.compras:
            with st.container():
                cols = st.columns(5)
                valores = [compra.idCompra, compra.idProducto, compra.idProveedor, compra.fechaDeCompra, compra.cantidad]
                for col, val in zip(cols, valores):
                    with col:
                        st.write(val)
                        
    def reportes(self):
        st.title("📑 Reportes")
        st.subheader("Estás viendo los reportes")

        opcion = st.selectbox("📌 Elige un reporte:", [
            "Productos con menor stock",
            "Proveedores más frecuentes",
            "Ventas por período de tiempo",
            "Productos más vendidos"
        ])
        if opcion == "Productos con menor stock":
            menor_stock = producto_menor_stock(self)
            st.write("📉 **Producto con menor stock:**", menor_stock)

        elif opcion == "Proveedores más frecuentes":
            proveedores = proveedores_mas_frecuentes(self)
            st.write("🏢 **Proveedores más frecuentes:**")
            for proveedor in proveedores:
                st.write(f"- Proveedor {proveedor[0]}: {proveedor[1]} compras")

        elif opcion == "Ventas por período de tiempo":
            fecha_inicio = st.date_input("📅 Fecha de inicio")
            fecha_fin = st.date_input("📅 Fecha de fin")
            ventas_filtradas = ventas_por_periodo(self, str(fecha_inicio), str(fecha_fin))
            st.write("🛒 **Ventas en el período seleccionado:**", ventas_filtradas)

        elif opcion == "Productos más vendidos":
            mas_vendidos = productos_mas_vendidos(self)
            st.write("🔥 **Productos más vendidos:**")
            for producto in mas_vendidos:
               st.write(f"- Producto {producto[0]}: {producto[1]} unidades vendidas")