import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Registro de Vehículos", page_icon="🚗", layout="centered")

st.title("📋 Registro de Vehículos por Voz")

# Archivo Excel en memoria
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Placa", "Marca", "Comentarios"])

# Interfaz con dictado por voz (Web Speech API)
st.markdown("""
<script>
function startDictation() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "es-ES";
        recognition.start();
        recognition.onresult = function(e) {
            var texto = e.results[0][0].transcript;
            document.getElementById('inputvoz').value = texto;
            recognition.stop();
        };
    }
}
</script>
<input id="inputvoz" type="text" placeholder="Dicta aquí" style="width: 100%; padding:8px" />
<button onclick="startDictation()">🎤 Grabar</button>
""", unsafe_allow_html=True)

# Caja para mostrar el texto dictado
entrada = st.text_input("Texto reconocido", "")

# Botón para guardar
if st.button("Guardar en Excel"):
    palabras = entrada.split(" ", 2)
    placa = palabras[0] if len(palabras) > 0 else ""
    marca = palabras[1] if len(palabras) > 1 else ""
    comentario = palabras[2] if len(palabras) > 2 else ""
    
    st.session_state.data.loc[len(st.session_state.data)] = [placa, marca, comentario]
    st.success("✅ Guardado en la tabla")

# Mostrar tabla
st.dataframe(st.session_state.data)

# Botón para descargar Excel
output = io.BytesIO()
st.session_state.data.to_excel(output, index=False)
st.download_button(
    label="📂 Descargar Excel",
    data=output.getvalue(),
    file_name="vehiculos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
