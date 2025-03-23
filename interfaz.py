import streamlit as st
from clases import x

class dashboard:

    def __init__(self):
        st.set_page_config(page_title="StockWise Dashboard", layout="wide")
        self.productos = x
        self.proveedores = x
        self.ventas = x
        self.compras = x
        self.titulo()
        self.sidebar()
        self.mostrar_contenido()

    def titulo(self):
        st.title("📊 StockWise Dashboard")

    def sidebar(self):
        with st.sidebar:
            st.header("📁 Navegación")
            self.opcion = st.radio("Ir a:", [
                "Home", "Productos", "Proveedores", "Ventas", "Compras",
                "Reportes"
            ])

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
        st.subheader("🏠 Home")
        st.write("Bienvenido al Home")

    def showProductos(self):
        st.subheader("📦 Productos")
        st.write("Estás viendo los productos")

    def showProveedores(self):
        st.subheader("🚚 Proveedores")
        st.write("Estás viendo los proveedores")

    def showVentas(self):
        st.subheader("💰 Ventas")
        st.write("Estás viendo las ventas")

    def showCompras(self):
        st.subheader("🛒 Compras")
        st.write("Estás viendo las compras")

    def reportes(self):
        st.subheader("📑 Reportes")
        st.write("Estás viendo los reportes")