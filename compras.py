import streamlit as st
import time
from unidecode import unidecode
from datetime import datetime
from modelo.clases import *
from init import generateData, productos, proveedores, ventas, compras



#Función añadir compra
def addCompra(recargarCompras, recargarProductos):
    st.subheader("➕ Nueva Compra")

    # 1) Búsqueda en vivo por nombre de producto y proveedor
    # Búsquedas en una sola fila
    col_prod, col_prov = st.columns([1,1], gap="large")

    with col_prod:
        search_prod = st.text_input(
            "Producto (busca por nombre)",
            key="compra_search_prod"
        )
        prod_matches = [
            p for p in productos 
            if search_prod and search_prod.lower() in p.nombre.lower()
        ]

    with col_prov:
        search_prov = st.text_input(
            "Proveedor (busca por nombre)",
            key="compra_search_prov"
        )
        prov_matches = [
            p for p in proveedores 
            if search_prov and search_prov.lower() in p.nombre.lower()
        ]

    # 2) Formulario agrupado
    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown("### 🛒 Registrar Compra")
        st.write("Selecciona producto y proveedor, indica la cantidad y guarda la compra.")

        with st.form("form_add_compra", clear_on_submit=True):
            c1, c2, c3 = st.columns([3, 3, 1], gap="large")

            # Producto dinámico
            if prod_matches:
                opts = [f"{p.nombre} ({p.idProducto})" for p in prod_matches]
                sel_prod = c1.selectbox("Producto", opts, key="compra_sel_prod")
                idProducto = sel_prod.split("(")[-1].rstrip(")")
            else:
                c1.selectbox("Producto", ["—"], disabled=True, key="compra_sel_prod")
                idProducto = None

            # Proveedor dinámico
            if prov_matches:
                opts2 = [f"{p.nombre} ({p.idProveedor})" for p in prov_matches]
                sel_prov = c2.selectbox("Proveedor", opts2, key="compra_sel_prov")
                idProveedor = sel_prov.split("(")[-1].rstrip(")")
            else:
                c2.selectbox("Proveedor", ["—"], disabled=True, key="compra_sel_prov")
                idProveedor = None

            cantidad = c3.number_input("Cantidad", min_value=1, step=1, key="compra_cant")

            # Botón centrado
            b1, b2, b3 = st.columns([5,2,5])
            guardar = b2.form_submit_button("💾 Guardar Compra")

        st.markdown('</div>', unsafe_allow_html=True)

    # 3) Al guardar
    if not guardar:
        return

    # Validaciones
    if not idProducto:
        st.error("❌ Selecciona un producto válido.")
        return
    if not idProveedor:
        st.error("❌ Selecciona un proveedor válido.")
        return

    # Registrar en CSV
    new_id = buscarNextID(compras, prefijo="c")
    fecha = datetime.now().strftime("%d-%m-%Y")
    linea = f"{new_id},{idProducto},{idProveedor},{fecha},{cantidad}\n"
    with open("compras.csv", "a", encoding="utf-8") as f:
        f.write(linea)

    # Actualizar stock y recargar tablas
    actualizarStock(idProducto, cantidad, recargarProductos)
    generateData("compras.csv", compras, Compra)
    recargarCompras()

    st.success(f"✅ Compra registrada: {cantidad}× {search_prod} de {search_prov}")
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


def actualizarC(id_compra: str, recargar):
    # 1) Busca la compra en memoria
    compra = next((c for c in compras if c.idCompra == id_compra), None)
    if not compra:
        st.error(f"No encontré la compra con ID {id_compra}")
        return

    # 2) Prepara las listas "Nombre (ID)"
    prod_opts = [f"{p.nombre} ({p.idProducto})" for p in productos]
    prov_opts = [f"{p.nombre} ({p.idProveedor})" for p in proveedores]

    # 3) Identifica los índices actuales
    prod_idx = next(
        (i for i,p in enumerate(productos) if p.idProducto == compra.idProducto),
        0
    )
    prov_idx = next(
        (i for i,p in enumerate(proveedores) if p.idProveedor == compra.idProveedor),
        0
    )
    try:
        cant_def = int(compra.cantidad)
    except:
        cant_def = 1

    st.subheader(f"✏️ Editando Compra `{compra.idCompra}`")
    st.write("Si un campo no cambia, déjalo como está.")

    with st.form(f"form_update_compra_{id_compra}", clear_on_submit=False):
        c1, c2, c3 = st.columns([3,3,1], gap="large")

        # Selectbox de producto
        sel_prod = c1.selectbox(
            "Producto",
            options=prod_opts,
            index=prod_idx,
            key=f"upd_compra_prod_{id_compra}"
        )
        # Extraemos el ID
        idProducto = sel_prod.split("(")[-1].rstrip(")")

        # Selectbox de proveedor
        sel_prov = c2.selectbox(
            "Proveedor",
            options=prov_opts,
            index=prov_idx,
            key=f"upd_compra_prov_{id_compra}"
        )
        idProveedor = sel_prov.split("(")[-1].rstrip(")")

        # Cantidad pre-cargada
        cantidad = c3.number_input(
            "Cantidad",
            min_value=1,
            step=1,
            value=cant_def,
            key=f"upd_compra_cant_{id_compra}"
        )

        # Botón
        b1, b2, b3 = st.columns([5,2,5])
        guardar = b2.form_submit_button("💾 Guardar Cambios")

    if not guardar:
        return

    # 4) Reescribe el CSV
    lines = []
    with open("compras.csv", "r", encoding="utf-8") as f:
        for line in f:
            cols = line.strip().split(",")
            if cols[0] == id_compra:
                cols[1] = idProducto
                cols[2] = idProveedor
                cols[4] = str(cantidad)
                line = ",".join(cols) + "\n"
            lines.append(line)

    with open("compras.csv", "w", encoding="utf-8") as f:
        f.writelines(lines)

    st.success("✅ Compra actualizada correctamente")
    generateData("compras.csv", compras, Compra)
    recargar()
    st.session_state["modo"] = "ver"
    time.sleep(0.5)
    st.rerun()





def eliminarC(id, recargar):
    st.write(f"¿Seguro que deseas eliminar la compra con ID {id}?")
    if st.button("Eliminar"):        
        with open('compras.csv', 'r') as file:
            lines = file.readlines()
        
        encabezado = lines[0]
        compras_filtradas = []

        for line in lines[1:]:
            line_data = line.strip().split(',')
            if line_data[0] != id:
                compras_filtradas.append(line_data)
        
        contador_id = 1
        for compra in compras_filtradas:
            nuevo_id = "c" + str(contador_id).zfill(3)
            compra[0] = nuevo_id
            contador_id += 1
        
        with open('compras.csv', 'w') as file:
            file.write(encabezado)
            for compra in compras_filtradas:
                file.write(",".join(compra) + "\n")
        
        st.success("✅ Compra eliminada e IDs actualizados")
        generateData('compras.csv', compras, Compra)
        recargar()  # Recarga las compras en la interfaz
        st.session_state.modo = 'ver'
        time.sleep(1)
        st.rerun()
    elif st.button("No"):
        st.session_state.modo = 'ver'
        st.rerun()

