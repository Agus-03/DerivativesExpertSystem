import streamlit as st
from rules import DerivadorExperto
from analizer import analizar_funcion
import io
import sympy as sp
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
    - **División:** `(3*x)/(4+x)`
    - **Funciones:** `sin(x)`, `cos(x)`, `exp(x)`, `log(x, base)`, `ln(x)`, `tan(x)`
    - **Negativos:** `x*(-3)*x^2` 
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
            resultado_final = ""
            hubo_error = False

            # Procesamos línea por línea la salida del motor
            for linea in salida_pasos.split('\n'):
                if "ERROR:" in linea:
                    st.error(linea.replace("ERROR:", "❌"))
                    hubo_error = True
                    break
                elif "SOLUCION_FINAL:" in linea:
                    resultado_final = linea.split("SOLUCION_FINAL:")[-1].strip()
                elif "[RECURSIVA]" in linea:
                    st.warning(linea)
                elif "[ATÓMICA]" in linea:
                    st.success(linea)

            # 4. Renderizado del Resultado Final en LaTeX
            if resultado_final and not hubo_error:
                st.divider()
                st.subheader("✅ Resultado Final")
                try:
                    # Convertimos a formato LaTeX real de SymPy para que se vea pro
                    expr_sympy = sp.sympify(resultado_final)
                    st.latex(sp.latex(expr_sympy))
                except:
                    # Fallback si SymPy falla al parsear el resultado
                    st.code(resultado_final)
    else:
        st.warning("⚠️ Por favor, ingresa una función.")

# Pie de página
st.divider()
st.caption("Desarrollado con Python, SymPy y Experta.")