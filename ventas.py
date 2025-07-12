import streamlit as st
import time
from unidecode import unidecode
from datetime import datetime
from modelo.clases import *
from init import generateData, productos, proveedores, ventas, compras

# Función para añadir una nueva venta
# Aplica layout ancho
st.set_page_config(page_title="📊 Ventas", layout="wide")



def addVenta(recargarVentas, recargarProductos):
    # Contenedor card
    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)

        # Encabezado
        st.markdown("### ➕ Nueva Venta")
        st.write("Busca el producto por nombre, completa los datos y guarda la venta.")

        # Live search + form agrupado
        search = st.text_input("Producto (busca por nombre)", key="venta_search")

        # Filtrado inmediato
        matches = [p for p in productos if search and search.lower() in p.nombre.lower()]

        # Formulario
        with st.form("form_add_venta", clear_on_submit=True):
            c1, c2, c3 = st.columns([3, 3, 1], gap="large")

            # Select dinamico
            if matches:
                options = [f"{p.nombre} ({p.idProducto})" for p in matches]
                sel = c1.selectbox("Elige producto", options, key="venta_sel")
                idProducto = sel.split("(")[-1].rstrip(")")
            else:
                c1.selectbox("Elige producto", ["—"], disabled=True, key="venta_sel")
                idProducto = None

            idCliente = c2.text_input("Nombre del cliente", key="venta_cliente")
            cantidad  = c3.number_input("Cantidad", min_value=1, step=1, key="venta_cant")

            # Botón centrado
            btn1, btn2, btn3 = st.columns([5,2,5])
            guardar = btn2.form_submit_button("💾 Guardar Venta")

        st.markdown('</div>', unsafe_allow_html=True)

    # Lógica tras submit
    if not guardar:
        return

    # Validaciones
    if not idProducto:
        st.error("❌ Selecciona un producto válido.")
        return
    if not idCliente.strip():
        st.error("❌ El nombre del cliente no puede quedar vacío.")
        return

    ok_or_stock = validarStock(idProducto, cantidad)
    if ok_or_stock is not True:
        st.error(f"❌ Stock insuficiente (solo hay {ok_or_stock}).")
        return

    # Guarda la venta
    new_id = buscarNextID(ventas, prefijo="v")
    fecha = datetime.now().strftime("%d-%m-%Y")
    with open("ventas.csv", "a", encoding="utf-8") as f:
        f.write(f"{new_id},{idProducto},{idCliente},{fecha},{cantidad}\n")

    # Actualiza stock y recarga tablas
    actualizarStock(idProducto, -cantidad, recargarProductos)
    generateData("ventas.csv", ventas, Venta)
    recargarVentas()

    st.success(f"✅ Venta registrada: {cantidad}× {search}")
    st.session_state.modo = "ver"
    time.sleep(0.5)
    st.rerun()
        
        
        
def actualizarStock(id, cantidad, recargar):
    with open('productos.csv', 'r') as file:
        lines = file.readlines()
    with open('productos.csv', 'w') as file:
        for line in lines:
            line_data = line.strip().split(',')
            if line_data[0] == id:
                line_data[4] = str(int(line_data[4]) + int(cantidad))
                file.write(",".join(line_data) + "\n")
            else:
                file.write(line)
    generateData('productos.csv', productos, Producto)
    recargar()

def validarStock(id, cantidad):
    for producto in productos:
        if producto.idProducto == id:
            if int(producto.stock) < cantidad:
                return int(producto.stock)
    return True

def buscarNextID(lista, prefijo):
    if not lista:  # Verifica si la lista está vacía
        return f"{prefijo}001"

    last = lista[-1]
    lastID = list(vars(last).values())[0] # Obtiene el atributo
    lastID = int(lastID.replace(prefijo, ""))  # Elimina el prefijo y convierte a entero
    nextID = f"{prefijo}{str(lastID + 1).zfill(3)}"  # Formatea con ceros a la izquierda
    return nextID

def actualizarV(id_venta: str, recargar):
    # 1) Busca la venta en memoria
    venta = next((v for v in ventas if v.idVenta == id_venta), None)
    if not venta:
        st.error(f"No encontré la venta con ID {id_venta}")
        return

    # 2) Contenedor card
    container = st.container()
    container.markdown('<div class="form-card">', unsafe_allow_html=True)
    container.markdown(f"## ✏️ Editando Venta `{venta.idVenta}`")
    container.write("Si un campo no cambia, déjalo como está.")

    # 3) Formulario
    form_key = f"form_update_venta_{id_venta}"
    with container.form(form_key, clear_on_submit=False):
        # Columnas: Producto (3), Cliente (3), Fecha (2), Cantidad (1)
        c1, c2, c4 = st.columns([3,3,1], gap="large")

        # 3a) Producto: mostramos nombres con IDs y pre-seleccionamos
        nombres = [p.nombre for p in productos]
        # encontrar índice del nombre actual
        current_name = next((p.nombre for p in productos if p.idProducto == venta.idProducto), "")
        idx = nombres.index(current_name) if current_name in nombres else 0
        sel = c1.selectbox(
            "Producto",
            options=nombres,
            index=idx,
            key=f"upd_venta_prod_{id_venta}"
        )
        # resolver ID del producto
        idProducto = next(p.idProducto for p in productos if p.nombre == sel)

        # 3b) Cliente pre-cargado
        idCliente = c2.text_input(
            "Cliente",
            value=venta.idCliente,
            key=f"upd_venta_cli_{id_venta}"
        )

        # 3d) Cantidad pre-cargada
        cantidad = c4.number_input(
            "Cantidad",
            min_value=1,
            step=1,
            value=int(venta.cantidad),
            key=f"upd_venta_cant_{id_venta}"
        )

        # Botón centrado
        b1, b2, b3 = st.columns([3,1,3])
        guardar = b2.form_submit_button("💾 Guardar Cambios")

    container.markdown("</div>", unsafe_allow_html=True)

    # 4) Si no envió, salimos
    if not guardar:
        return

    # 5) Validaciones
    if not idProducto:
        st.error("❌ Debes seleccionar un producto válido.")
        return
    if not idCliente.strip():
        st.error("❌ El nombre del cliente no puede estar vacío.")
        return
    ok_or_stock = validarStock(idProducto, cantidad)
    if ok_or_stock is not True:
        st.error(f"❌ Stock insuficiente (solo hay {ok_or_stock}).")
        return

    # 6) Reescribe el CSV con la línea editada
    archivo = "ventas.csv"
    with open(archivo, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(archivo, "w", encoding="utf-8") as f:
        for line in lines:
            cols = line.strip().split(",")
            if cols[0] == id_venta:
                cols[1] = idProducto
                cols[2] = idCliente
                cols[4] = str(cantidad)
                f.write(",".join(cols) + "\n")
            else:
                f.write(line)

    # 7) Feedback y recarga
    st.success("✅ Venta actualizada correctamente")
    generateData("ventas.csv", ventas, Venta)
    recargar()
    st.session_state["modo"] = "ver"
    time.sleep(0.5)
    st.rerun()


def eliminarV(id, recargar):
    st.write(f"¿Seguro que deseas eliminar la venta con ID {id}?")
    if st.button("Eliminar"):        
        with open('ventas.csv', 'r') as file:
            lines = file.readlines()
        
        encabezado = lines[0]
        ventasFiltradas = []

        for line in lines[1:]:
            line_data = line.strip().split(',')
            if line_data[0] != id:
                ventasFiltradas.append(line_data)
        
        contador_id = 1

        for venta in ventasFiltradas:
            nuevo_id = "c" + str(contador_id).zfill(3)
            venta[0] = nuevo_id
            contador_id += 1
        
        with open('ventas.csv', 'w') as file:
            file.write(encabezado)
            for venta in ventasFiltradas:
                file.write(",".join(venta) + "\n")
        
        st.success("✅ Venta eliminada e IDs actualizados")
        generateData('ventas.csv', ventas, Venta)
        recargar()  # Recarga las compras en la interfaz
        st.session_state.modo = 'ver'
        time.sleep(1)
        st.rerun()
    elif st.button("No"):
        st.session_state.modo = 'ver'
        st.rerun()
       