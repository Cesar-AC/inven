import streamlit as st
import time
import math
from unidecode import unidecode
from datetime import datetime
from modelo.clases import *
from productos import *
from proveedores import *
from ventas import *
from compras import *
from init import generateData, productos, proveedores, ventas, compras

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
    for compra in self:
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
def ventas_por_periodo(fecha_inicio, fecha_fin):
    resultado = []
    for venta in st.session_state["ventas"]:
        if fecha_inicio <= venta.fechaDeVenta and venta.fechaDeVenta <= fecha_fin:
            resultado.append(venta)
    return resultado

# Reporte 4: Productos más vendidos
def productos_mas_vendidos():
    conteo = {}
    for venta in st.session_state["ventas"]:
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

def mostrarDatos(lista, columnas, atributos, clave_prefijo, actualizar_fn, eliminar_fn):
    # —————————————————————————————————————————————
    # 1) Modo editar / eliminar 
    # —————————————————————————————————————————————
    if st.session_state.get("modo") == "editar":
        actualizar_fn(st.session_state["id_editando"])
        return
    if st.session_state.get("modo") == "eliminar":
        eliminar_fn(st.session_state["id_eliminando"])
        return

    # —————————————————————————————————————————————
    # 2) Configuración de paginación
    # —————————————————————————————————————————————
    total = len(lista)
    key_size = f"{clave_prefijo}_page_size"
    key_page = f"{clave_prefijo}_page"

    # Inicializar valores por defecto si no existen
    if key_size not in st.session_state:
        st.session_state[key_size] = 10
    if key_page not in st.session_state:
        st.session_state[key_page] = 1

    # Aclimatar page_size y page en rango válido
    page_size = st.session_state[key_size]
    page      = st.session_state[key_page]
    total_pages = max(1, math.ceil(total / page_size))
    page = max(1, min(page, total_pages))
    st.session_state[key_page] = page

    # Slice de la lista
    start  = (page - 1) * page_size
    end    = start + page_size
    subset = lista[start:end]

    # —————————————————————————————————————————————
    # 3) Encabezados
    # —————————————————————————————————————————————
    hdr_cols = st.columns(len(columnas))
    for col, h in zip(hdr_cols, columnas):
        col.write(f"**{h}**")

    # —————————————————————————————————————————————
    # 4) Filas + acciones
    # —————————————————————————————————————————————
    for item in subset:
        row_cols = st.columns(len(columnas))
        datos = [getattr(item, attr) for attr in atributos]

        # Mostrar valores
        for c, v in zip(row_cols[:-1], datos):
            c.write(v)

        # Select de acciones
        with row_cols[-1]:
            opcion = st.selectbox(
                "",
                ["Elija", "Actualizar", "Eliminar"],
                key=f"{clave_prefijo}_opt_{datos[0]}",
                label_visibility="collapsed"
            )
            if opcion == "Actualizar":
                st.session_state["modo"] = "editar"
                st.session_state["id_editando"] = datos[0]
                st.rerun()
            elif opcion == "Eliminar":
                st.session_state["modo"] = "eliminar"
                st.session_state["id_eliminando"] = datos[0]
                st.rerun()

    # —————————————————————————————————————————————
    # 5) Controles de paginación (inferior derecha)
    # —————————————————————————————————————————————
    pag_cols = st.columns([4, 1, 1])

    # 1) Selector de filas por página
    page_size = pag_cols[1].selectbox(
        "", [10, 20, 30, 50, 100],
        index=[10,20,30,50,100].index(st.session_state[key_size]),
        key=key_size,
        label_visibility="collapsed"
    )

    # 2) Selector de número de página
    page = pag_cols[2].number_input(
        "", min_value=1, max_value=total_pages,
        value=st.session_state[key_page],
        step=1,
        key=key_page,
        label_visibility="collapsed"
    )

    # Usa page_size y page para el slice (ya están en session_state)
    start  = (page - 1) * page_size
    end    = start + page_size
    subset = lista[start:end]

    # 3) Feedback minimalista
    st.markdown(
        f"<div style='text-align:right; font-size:0.8rem; color:gray;'>"
        f"Página {page}/{total_pages} — {total} registros"
        f"</div>",
        unsafe_allow_html=True
    )
