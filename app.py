import streamlit as st
from rules import DerivadorExperto
from analizer import analizar_funcion
import io
from contextlib import redirect_stdout

# Configuración estética de la página
st.set_page_config(page_title="Derivador Experto SBC", page_icon="🧮", layout="centered")

st.title("Sistema Experto: Derivación Simbólica")
st.markdown("""
Este sistema utiliza un **Motor de Inferencia (Experta)** para explicar el razonamiento 
detrás de cada derivada, aplicando reglas recursivas y atómicas.
""")

# Barra lateral informativa
with st.sidebar:
    st.header("Guía de Uso")
    st.markdown("""
    - **Multiplicación:** `3*x`
    - **División:** `(3x)/(4+x)`
    - **Funciones:** `sin(x)`, `cos(x)`, `exp(x)`, `log(x, base)`, `ln(x)`
    """)
    st.divider()
    st.caption("Proyecto de Sistemas Basados en Conocimiento")

# Campo de entrada
fun_input = st.text_input("Ingresa la función a derivar:", "log(x, 2) * cos(x^2)")

if st.button("Analizar y Derivar"):
    if fun_input:
        # --- LIMPIEZA DE ENTRADA ---
        # Reemplazamos el sombrerito ^ por el doble asterisco ** que entiende Python
        fun_limpia = fun_input.replace("^", "**")
        fun_limpia = fun_limpia.replace("ln","log")
        # ---------------------------

        engine = DerivadorExperto()
        engine.reset()
        
        st.subheader("🧠 Razonamiento del Motor")
        
        # Capturamos los prints que hace el motor de reglas
        f = io.StringIO()
        with redirect_stdout(f):
            analizar_funcion(engine, fun_limpia)
        
        salida_pasos = f.getvalue()
        
        # Procesamos la salida para mostrarla bonita
        if salida_pasos:
            pasos_visibles = []
            resultado_final = ""

            # Separamos la paja del trigo
            for linea in salida_pasos.split('\n'):
                if "SOLUCION_FINAL:" in linea:
                    resultado_final = linea.split("SOLUCION_FINAL:")[-1].strip()
                elif "[RECURSIVA]" in linea:
                    st.warning(linea)
                elif "[ATÓMICA]" in linea:
                    st.success(linea)

            # Si encontramos el resultado, lo mostramos grande y bonito
            if resultado_final:
                st.divider()
                st.subheader("✅ Resultado Final")
                # Limpiamos el formato para que LaTeX no se rompa con los asteriscos
                formato_latex = resultado_final.replace("**", "^").replace("*", " \cdot ")
                st.latex(formato_latex)
            else:
                st.error("❌ El motor procesó las reglas pero no devolvió un resultado final.")