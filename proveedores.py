import streamlit as st
import time
from unidecode import unidecode
from datetime import datetime
from modelo.clases import *
from init import generateData, productos, proveedores, ventas, compras



def validarTexto(input, mensaje):
    if input.strip() == "":
        st.error(f"❌ {mensaje} no puede estar vacío")
        return False
    return True

def validarContacto(input):
    if not input.isdigit() and not("@" in input):
        st.error(f"❌ Contacto debe ser un número o un email")
        return False
    return True

#Funcion añadir proveedor
def addProveedor(recargar):
    # Inyectamos el mismo CSS para tarjetas de formulario


    # Contenedor estilizado
    container = st.container()

    container.subheader("➕ Nuevo Proveedor")

    # Formulario con columnas proporcionales
    form_key = "form_add_proveedor"
    with container.form(form_key, clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 3, 4])
        nombre    = c1.text_input("Nombre del Proveedor", key="prov_nombre")
        contacto  = c2.text_input("Contacto (teléfono)", key="prov_contacto")
        direccion = c3.text_input("Dirección", key="prov_direccion")

        guardar = st.form_submit_button("💾 Guardar")

    container.markdown('</div>', unsafe_allow_html=True)

    if not guardar:
        return

    # Validaciones
    if not validarTexto(nombre, "El nombre"):
        return
    if not validarContacto(contacto):
        return
    if not validarTexto(direccion, "La dirección"):
        return

    # Persistimos en CSV
    new_id = buscarNextID(proveedores, prefijo="p")
    linea = f"{new_id},{nombre},{contacto},{direccion}\n"
    with open("proveedores.csv", "a", encoding="utf-8") as f:
        f.write(linea)

    # Refrescamos el listado en memoria y la UI
    generateData("proveedores.csv", proveedores, Proveedor)
    recargar()

    st.success(f"✅ Proveedor **{nombre}** guardado con ID `{new_id}`")
    st.session_state["modo"] = "ver"
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



def actualizarPv(id, recargar):
    # Inyecta CSS para tarjetas de formulario
    st.markdown("""
    <style>
      .form-card {
        background-color: #252526;
        padding: 1.2rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
      }
      .form-card label {
        color: #eee;
        font-weight: 600;
      }
      .form-card .stTextInput>div>input,
      .form-card .stTextArea>div>textarea {
        background-color: #1e1e1e;
        color: #fff;
      }
      .form-card .stButton>button {
        background-color: #0063af;
        color: #fff;
      }
    </style>
    """, unsafe_allow_html=True)

    # 1) Busca el proveedor
    prov = next((p for p in proveedores if p.idProveedor == id), None)
    if not prov:
        st.error(f"No encontré proveedor con ID {id}")
        return

    # 2) Encabezado
    container = st.container()
    container.subheader(f"✏️ Editando Proveedor {prov.idProveedor}")

    # 3) Form dentro del contenedor
    form_key = f"form_update_prov_{id}"
    with container.form(form_key, clear_on_submit=False):
        c1, c2, c3 = st.columns([3, 3, 4])
        # Prefill de los campos
        nombre    = c1.text_input("Nombre", value=prov.nombre, key=f"upd_prov_nombre_{id}")
        contacto  = c2.text_input("Contacto", value=prov.contacto, key=f"upd_prov_contacto_{id}")
        direccion = c3.text_input("Dirección", value=prov.direccion, key=f"upd_prov_direccion_{id}")

        # Botón centrado
        b1, b2, b3 = st.columns([3,1,3])
        guardar = b2.form_submit_button("💾 Guardar Cambios")

    container.markdown('</div>', unsafe_allow_html=True)

    # 4) Si no enviaron el form, salimos
    if not guardar:
        return

    # 5) Validaciones
    if not validarTexto(nombre, "El nombre"):
        return
    if not validarContacto(contacto):
        return
    if not validarTexto(direccion, "La dirección"):
        return

    # 6) Reescribe el CSV
    lines = []
    with open("proveedores.csv", "r", encoding="utf-8") as f:
        for line in f:
            cols = line.strip().split(",")
            if cols[0] == id:
                cols[1] = nombre or cols[1]
                cols[2] = contacto or cols[2]
                cols[3] = direccion or cols[3]
                lines.append(",".join(cols) + "\n")
            else:
                lines.append(line)
    with open("proveedores.csv", "w", encoding="utf-8") as f:
        f.writelines(lines)

    # 7) Feedback y recarga
    st.success("✅ Proveedor actualizado")
    generateData("proveedores.csv", proveedores, Proveedor)
    recargar()
    st.session_state["modo"] = "ver"
    time.sleep(0.5)
    st.rerun()

def eliminarPv(id, recargar):
    st.write(f"¿Seguro que deseas eliminar el proveedor con ID {id}?")
    if st.button("Eliminar"):        
        with open('proveedores.csv', 'r') as file:
            lines = file.readlines()
        
        encabezado = lines[0]
        proveedoresFiltrados = []

        for line in lines [1:]:
            line_data = line.strip().split(',')
            if line_data[0] != id:
                proveedoresFiltrados.append(line_data)
        
        contador_id = 1
        for proveedor in proveedoresFiltrados:
            nuevo_id = "p" + str(contador_id).zfill(3)
            proveedor[0] = nuevo_id
            contador_id += 1
        
        with open('proveedores.csv', 'w') as file:
            file.write(encabezado)
            for proveedor in proveedoresFiltrados:
                file.write(",".join(proveedor) + "\n")
        
        st.success("✅ Proveedor eliminado e IDs actualizados")
        generateData('proveedores.csv', proveedores, Proveedor)
        recargar()  # Recarga los proveedores en la interfaz
        st.session_state.modo = 'ver'
        time.sleep(1)
        st.rerun()
    elif st.button("No"):
        st.session_state.modo = 'ver'
        st.rerun()