import streamlit as st
import time
from unidecode import unidecode
from datetime import datetime
from modelo.clases import *
from init import generateData, productos, proveedores, ventas, compras


#Funcion añadir producto
def addProducto(recargar):
    st.subheader("➕ Nuevo Producto")

    # Formulario para agrupar todos los inputs
    with st.form("form_add_producto", clear_on_submit=True):
        # Primera fila: Nombre, Categoría, Precio
        col1, col2, col3 = st.columns([3, 3, 1])
        nombre    = col1.text_input("Nombre")
        categorias = [
            "Seleccione una categoría",
            "Belleza", "Tecnología", "Alimentos",
            "Ropa y Calzado", "Electrónica", "Hogar",
            "Deportes", "Juguetes"
        ]
        categoria = col2.selectbox("Categoría", categorias)
        precio    = col3.number_input("Precio (S/)", min_value=0.01, format="%.2f")

        # Segunda fila: Stock, Descripción
        col4, col5 = st.columns([1, 3])
        stock     = col4.number_input("Stock", min_value=0, step=1)
        desc      = col5.text_area("Descripción", height=80)

        enviar = st.form_submit_button("💾 Guardar")

    # Si no presionaron “Guardar”, salimos
    if not enviar:
        return

    # Nombre y descripción no vacíos
    if not validarTexto(nombre, "El nombre"):
        return
    if not validarTexto(desc, "La descripción"):
        return

    # Categoría seleccionada distinta del placeholder
    if categoria == categorias[0]:
        st.error("❌ Debes seleccionar una categoría válida.")
        return

    # Precio y stock ya validados por number_input (mayor que 0)
    # pero añadimos un chequeo extra por si acaso:
    if precio <= 0:
        st.error("❌ El precio debe ser mayor que 0.")
        return
    if stock < 0:
        st.error("❌ El stock no puede ser negativo.")
        return

    new_id = buscarNextID(productos, prefijo="prod")
    linea = f"{new_id},{nombre},{categoria},{precio},{stock},{desc}\n"
    with open("productos.csv", "a", encoding="utf-8") as f:
        f.write(linea)

    # Recargar datos en memoria y refrescar UI
    generateData("productos.csv", productos, Producto)
    recargar()

    st.success(f"✅ Producto `{nombre}` guardado con ID **{new_id}**")
    st.session_state.modo = "ver"
    time.sleep(0.5)
    st.rerun()
        
        
        
def buscarNextID(lista, prefijo):
    if not lista:  # Verifica si la lista está vacía
        return f"{prefijo}001"

    last = lista[-1]
    lastID = list(vars(last).values())[0] # Obtiene el atributo
    lastID = int(lastID.replace(prefijo, ""))  # Elimina el prefijo y convierte a entero
    nextID = f"{prefijo}{str(lastID + 1).zfill(3)}"  # Formatea con ceros a la izquierda
    return nextID

def validarTexto(input, mensaje):
    if input.strip() == "":
        st.error(f"❌ {mensaje} no puede estar vacío")
        return False
    return True



def filtrarProductos(xproductos):
    opcion = st.selectbox("🔎 Buscar productos por:", [
            "📄 Nombre",
            "📑 Categoría",
        ])
    
    if opcion == "📄 Nombre":
        cols = st.columns(1)
        nombre = cols[0].selectbox(
            "",
            options=["Nombre a buscar"] + [producto.nombre for producto in productos]
        )
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
        categorias = ["Belleza", "Tecnología", "Alimentos", "Ropa y Calzado", "Electrónica", "Hogar", "Deportes", "Juguetes"]
        cat = cols[0].selectbox(
            "",
            options=["Categoria a buscar"] + [categoria for categoria in categorias]
        )
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
                            


def actualizarP(id, recargar):
    # —————————————————————————————————————————————————
    # Inyecta un poco de CSS «in-line» para un contenedor con fondo oscuro
    # —————————————————————————————————————————————————

    prod = next((p for p in productos if p.idProducto == id), None)
    if not prod:
        st.error(f"No encontré producto con ID {id}")
        return

    container = st.container()
    container.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    form_key = f"form_update_{id}"
    with container.form(form_key, clear_on_submit=False):
        # Fila 1: Nombre (3), Categoría (3), Precio (2)
        c1, c2, c3 = st.columns([3,3,2])
        nombre = c1.text_input("Nombre", value=prod.nombre, key=f"upd_nombre_{id}")
        
        categorias = [
            "Seleccione una categoría",
            "Belleza", "Tecnología", "Alimentos",
            "Ropa y Calzado", "Electrónica", "Hogar",
            "Deportes", "Juguetes"
        ]
        default_idx = categorias.index(prod.categoria) if prod.categoria in categorias else 0
        categoria = c2.selectbox("Categoría", categorias, index=default_idx, key=f"upd_categoria_{id}")
        
        # Convertimos a float sin error
        try:
            precio_default = float(prod.precio)
        except:
            precio_default = 0.0
        precio = c3.number_input(
            "Precio (S/)", min_value=0.01, format="%.2f",
            value=precio_default, key=f"upd_precio_{id}"
        )

        st.markdown("---")  # separador visual

        # Fila 2: Stock (1), Descripción (7)
        c4, c5 = st.columns([1,7])
        try:
            stock_def = int(prod.stock)
        except:
            stock_def = 0
        stock = c4.number_input(
            "Stock", min_value=0, step=1,
            value=stock_def, key=f"upd_stock_{id}"
        )
        descripcion = c5.text_area(
            "Descripción", value=prod.descripcion,
            height=100, key=f"upd_desc_{id}"
        )

        # Centrar botón: tres columnas, botón en la del medio
        b1, b2, b3 = st.columns([3,1,3])
        guardar = b2.form_submit_button("💾 Guardar Cambios")

    # Cierra el contenedor
    container.markdown("</div>", unsafe_allow_html=True)

    if not guardar:
        return

    # Reescribe el CSV sólo con la línea editada
    lines = []
    with open("productos.csv", "r", encoding="utf-8") as f:
        for line in f:
            cols = line.strip().split(",")
            if cols[0] == id:
                cols[1] = nombre or cols[1]
                if categoria != categorias[0]:
                    cols[2] = categoria
                cols[3] = f"{precio:.2f}"
                cols[4] = str(stock)
                cols[5] = descripcion or cols[5]
                lines.append(",".join(cols) + "\n")
            else:
                lines.append(line)
    with open("productos.csv", "w", encoding="utf-8") as f:
        f.writelines(lines)

    st.success("✅ Producto actualizado")
    generateData("productos.csv", productos, Producto)
    recargar()
    st.session_state["modo"] = "ver"
    time.sleep(0.5)
    st.rerun()


        
def eliminarP(id, recargar):
    st.write(f"¿Seguro que deseas eliminar el producto con ID {id}?")
    if st.button("Eliminar"):        
            with open('productos.csv', 'r') as file:
                lines = file.readlines()
            
            encabezado = lines[0]
            productos_filtrados = []

            for line in lines [1:]:
                line_data = line.strip().split(',')
                if line_data[0] != id:
                    productos_filtrados.append(line_data)
            
            contador_id = 1
            for producto in productos_filtrados:
                nuevo_id = "prod" + str(contador_id).zfill(3)  # Formato prod001, prod002...
                producto[0] = nuevo_id
                contador_id += 1
            
            with open('productos.csv', 'w') as file:
                file.write(encabezado)
                for producto in productos_filtrados:
                    file.write(",".join(producto) + "\n")
            
            st.success("✅ Producto eliminado e IDs actualizados")
            generateData('productos.csv', productos, Producto)
            recargar()  # Recarga los productos en la interfaz
            st.session_state.modo = 'ver'
            time.sleep(1)
            st.rerun()
    elif st.button("No"):
        st.session_state.modo = 'ver'
        st.rerun()