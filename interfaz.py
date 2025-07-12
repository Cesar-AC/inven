#Importamos la librería streamlit junto a los datos iniciales
import streamlit as st
from funciones import *

#Esta clase contiene/actúa como la interfaz
class dashboard:
    
    def __init__(self):
        #Le da un título a la pestaña
        st.set_page_config(page_title = "Inven Dashboard", layout = "wide")
        
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
            st.header("📊 Inven Dashboard")
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
        st.title("🏠 INVEN STORE")
        st.subheader("Bienvenido")
        st.write("Esta es la interfaz principal de Inven Store, donde puedes gestionar productos, proveedores, ventas y compras.")
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
            elif st.session_state.modo == 'editar':
                st.subheader("Actualizando proveedores")
        
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
                # 1) Inyectar nombreProducto en cada Venta
                for v in ventas:
                    prod = next((p for p in productos if p.idProducto == v.idProducto), None)
                    v.nombreProducto = prod.nombre if prod else v.idProducto

                # 2) Definir columnas y atributos (nombreProducto en lugar de idProducto)
                columnas = [
                    "ID de Venta",
                    "Producto",
                    "Nombre del Cliente",
                    "Fecha de Venta",
                    "Cantidad",
                    "Opciones"
                ]
                atributos = [
                    "idVenta",
                    "nombreProducto",
                    "idCliente",
                    "fechaDeVenta",
                    "cantidad"
                ]

                # 3) Llamada a mostrarDatos
                mostrarDatos(
                    lista=ventas,
                    columnas=columnas,
                    atributos=atributos,
                    clave_prefijo="v",
                    actualizar_fn=actualizarV,
                    eliminar_fn=eliminarV
                )

            elif st.session_state.modo == 'agregar':
                addVenta(self.recargar_ventas, self.recargar_productos)
            elif st.session_state.modo == 'editar':
                actualizarV(st.session_state.id_editando, self.recargar_ventas)
            elif st.session_state.modo == 'eliminar':
                eliminarV(st.session_state.id_eliminando, self.recargar_ventas)
                
        
    def showCompras(self):
        st.title("🛒 Compras")

        # Inicializa el modo si aún no existe
        if 'modo' not in st.session_state:
            st.session_state.modo = 'ver'

        # Contenedores para header y botones
        col1, col2 = st.columns(2)
        header_placeholder  = col1.empty()
        buttons_placeholder = col2.empty()

        # Botones dinámicos
        with buttons_placeholder.container():
            btn_col = st.columns(1)[0]
            with btn_col:
                if st.session_state.modo != 'ver':
                    if st.button("📋 Ver Compras"):
                        st.session_state.modo = 'ver'
                        st.rerun()
                else:
                    if st.button("🛒 Añadir Compra"):
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
            # 1) Inyecta nombreProducto y nombreProveedor en cada Compra
            for c in compras:
                prod = next((p for p in productos   if p.idProducto  == c.idProducto),   None)
                prov = next((p for p in proveedores if p.idProveedor == c.idProveedor), None)
                c.nombreProducto  = prod.nombre   if prod else c.idProducto
                c.nombreProveedor = prov.nombre   if prov else c.idProveedor

            # 2) Columnas y atributos actualizados
            columnas = [
                "ID de Compra",
                "Producto",
                "Proveedor",
                "Fecha de Compra",
                "Cantidad",
                "Opciones"
            ]
            atributos = [
                "idCompra",
                "nombreProducto",
                "nombreProveedor",
                "fechaDeCompra",
                "cantidad"
            ]

            # 3) Mostrar con tu función de paginación/edición
            mostrarDatos(
                lista=compras,
                columnas=columnas,
                atributos=atributos,
                clave_prefijo="c",
                actualizar_fn=actualizarC,
                eliminar_fn=eliminarC
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

            for producto in productos_bajo_stock:
                stock = productos_bajo_stock[0][4]
                for i, producto in enumerate(productos_bajo_stock):
                    stockc = int(producto[4])
                    if i == 0:
                        continue
                    if stockc < stock:
                        productom = productos_bajo_stock[i-1]
                        productos_bajo_stock[i-1] = producto
                        productos_bajo_stock[i] = productom
                    stock = stockc

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

            compras_por_proveedor = {}
            unidades_por_proveedor = {}

            for compra in compras:
                pid = compra.idProveedor
                qty = int(compra.cantidad)   # <- Aquí convertimos a int

                compras_por_proveedor[pid] = compras_por_proveedor.get(pid, 0) + 1
                unidades_por_proveedor[pid] = unidades_por_proveedor.get(pid, 0) + qty

            lista_proveedores = [
                (pid, compras_por_proveedor[pid], unidades_por_proveedor[pid])
                for pid in compras_por_proveedor
            ]
            lista_proveedores.sort(key=lambda x: (x[1], x[2]), reverse=True)
            top_proveedores = lista_proveedores[:3]

            prov_map = {p.idProveedor: p.nombre for p in proveedores}

            st.write("🏢 **Proveedores más frecuentes:**")
            if top_proveedores:
                for pid, num_compras, total_unidades in top_proveedores:
                    nombre = prov_map.get(pid, "– Desconocido –")
                    st.write(f"- **{nombre}** ({pid}): {num_compras} compras, {total_unidades} unidades")
            else:
                st.write("❌ No hay suficientes datos")



        elif opcion == "Ventas por período de tiempo":
            fecha_inicio = st.date_input("📅 Fecha de inicio")
            fecha_fin    = st.date_input("📅 Fecha de fin")
            fi = fecha_inicio.strftime("%d-%m-%Y")
            ff = fecha_fin.strftime("%d-%m-%Y")
            ventas_filtradas = ventas_por_periodo(fi, ff)

            if ventas_filtradas:
                st.write("🛒 **Ventas en el período seleccionado:**")

                # 1) Cabeceras ahora con “Producto” en lugar de “ID Producto”
                encabezados = ["ID Venta", "Producto", "ID Cliente", "Fecha", "Cantidad"]
                cols = st.columns(len(encabezados))
                for col, titulo in zip(cols, encabezados):
                    col.write(f"**{titulo}**")

                # 2) Para cada venta, resolvemos el nombre del producto
                for venta in ventas_filtradas:
                    cols = st.columns(len(encabezados))
                    # buscamos el objeto Producto
                    prod = next((p for p in productos if p.idProducto == venta.idProducto), None)
                    nombre_prod = prod.nombre if prod else venta.idProducto

                    datos = [
                        venta.idVenta,
                        nombre_prod,               # <-- aquí el nombre en lugar de la ID
                        venta.idCliente,
                        venta.fechaDeVenta,
                        venta.cantidad
                    ]

                    for col, dato in zip(cols, datos):
                        col.write(dato)

            else:
                st.write("❌ No hay ventas en el período seleccionado.")


        elif opcion == "Productos más vendidos":
            st.write("🔥 **Productos más vendidos (4+ unidades):**")

            conteo_ventas = {}

            # Leer el archivo línea por línea
            with open("ventas.csv", "r", encoding="utf-8") as archivo:
                next(archivo) 
                for linea in archivo:
                    datos = linea.strip().split(",")
                    pid  = datos[1]
                    qty  = int(datos[4])
                    conteo_ventas[pid] = conteo_ventas.get(pid, 0) + qty

            # Filtramos los que vendieron >=4 unidades
            productos_filtrados = [(pid, qty) 
                                for pid, qty in conteo_ventas.items() 
                                if qty >= 4]

            if productos_filtrados:
                # Creamos mapa ID→Nombre
                prod_map = {p.idProducto: p.nombre for p in productos}

                for pid, qty in productos_filtrados:
                    nombre = prod_map.get(pid, pid)
                    st.write(f"- **{nombre}** ({pid}): {qty} unidades vendidas")
            else:
                st.write("❌ No hay productos con 4 o más unidades vendidas.")
