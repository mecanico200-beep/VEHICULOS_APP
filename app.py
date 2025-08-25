import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# Inicializar datos en sesión como lista
if "data" not in st.session_state:
    st.session_state["data"] = []

st.title("📋 Registro de Vehículos Taller")

st.write("Introduce los datos dictados o escritos para guardar en Excel.")

# Formulario de ingreso de datos
with st.form("vehiculo_form", clear_on_submit=True):
    placa = st.text_input("🚗 Placa")
    marca = st.text_input("🏷️ Marca")
    tecnico = st.text_input("👨‍🔧 Técnico (cualquier nombre)")
    comentario = st.text_area("📝 Comentarios")
    repuesto = st.text_input("⚙️ Repuesto necesario (si aplica)")
    submitted = st.form_submit_button("Agregar registro")

    if submitted:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nuevo_registro = {
            "Placa": placa.upper(),
            "Marca": marca.capitalize(),
            "Técnico": tecnico.capitalize(),
            "Fecha de dictado": fecha,
            "Comentarios": comentario,
            "Repuesto": repuesto.capitalize() if repuesto else "-"
        }
        # Guardar como lista de diccionarios
        registros = st.session_state["data"]
        registros.append(nuevo_registro)
        st.session_state["data"] = registros
        st.success(f"✅ Registro agregado: {placa}")

# Mostrar tabla si hay datos
if st.session_state["data"]:
    df = pd.DataFrame(st.session_state["data"])
    st.subheader("📊 Registros actuales")
    st.dataframe(df, use_container_width=True)

    # Función para exportar a Excel
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Vehículos")
        return output.getvalue()

    st.download_button(
        label="⬇️ Descargar Excel",
        data=to_excel(df),
        file_name="vehiculos_taller.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("👉 Aún no hay registros agregados.")
# --- Sección para editar registros ---
if st.session_state["data"]:
    st.subheader("✏️ Editar o eliminar registro")

    df = pd.DataFrame(st.session_state["data"])
    placas = df["Placa"].tolist()
    placa_sel = st.selectbox("Selecciona la placa a editar", placas)

    if placa_sel:
        # Buscar registro seleccionado
        idx = df[df["Placa"] == placa_sel].index[0]
        registro = st.session_state["data"][idx]

        with st.form("editar_form"):
            nueva_marca = st.text_input("Marca", registro["Marca"])
            nuevo_tecnico = st.text_input("Técnico", registro["Técnico"])
            nuevo_comentario = st.text_area("Comentarios", registro["Comentarios"])
            nuevo_repuesto = st.text_input("Repuesto", registro["Repuesto"])

            editar = st.form_submit_button("Guardar cambios")
            eliminar = st.form_submit_button("❌ Eliminar registro")

            if editar:
                st.session_state["data"][idx].update({
                    "Marca": nueva_marca,
                    "Técnico": nuevo_tecnico,
                    "Comentarios": nuevo_comentario,
                    "Repuesto": nuevo_repuesto
                })
                st.success("✅ Registro actualizado")

            if eliminar:
                st.session_state["data"].pop(idx)
                st.warning("🗑️ Registro eliminado")

