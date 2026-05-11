import streamlit as st
from rules import DerivadorExperto
from analizer import analizar_funcion
import io
import sympy as sp
from contextlib import redirect_stdout

# 1. Configuración estética de la página
st.set_page_config(page_title="Derivador Experto SBC", page_icon="🧮", layout="centered")

st.title("Sistema Experto: Derivación Simbólica")
st.markdown("""
Este sistema utiliza un **Motor de Inferencia (Experta)** para explicar el razonamiento 
detrás de cada derivada, aplicando reglas recursivas y atómicas.
""")

# 2. Barra lateral informativa
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

# 3. Campo de entrada
fun_input = st.text_input("Ingresa la función a derivar:", "(-x^2) * (x^-1 - 5)")

# Contenedor para el proceso
if st.button("Analizar y Derivar"):
    if fun_input:
        # --- LIMPIEZA DE ENTRADA ---
        fun_limpia = fun_input.replace("^", "**")
        fun_limpia = fun_limpia.replace("ln","log")

        # Reiniciamos el estado para una nueva consulta
        st.session_state['resultado_crudo'] = None
        st.session_state['pasos_motor'] = []

        engine = DerivadorExperto()
        engine.reset()
        
        # Capturamos los prints que hace el motor de reglas
        f = io.StringIO()
        with redirect_stdout(f):
            analizar_funcion(engine, fun_limpia)
        
        salida_pasos = f.getvalue()
        
        if salida_pasos:
            for linea in salida_pasos.split('\n'):
                if "ERROR:" in linea:
                    st.error(linea.replace("ERROR:", "❌"))
                elif "SOLUCION_FINAL:" in linea:
                    # Guardamos el resultado en la sesión
                    st.session_state['resultado_crudo'] = linea.split("SOLUCION_FINAL:")[-1].strip()
                elif "[RECURSIVA]" in linea or "[ATÓMICA]" in linea:
                    # Guardamos los pasos para mostrarlos
                    st.session_state['pasos_motor'].append(linea)
    else:
        st.warning("⚠️ Por favor, ingresa una función.")

# --- MOSTRAR RESULTADOS SI EXISTEN EN SESIÓN ---
if 'pasos_motor' in st.session_state and st.session_state['pasos_motor']:
    st.subheader("🧠 Razonamiento del Motor")
    for paso in st.session_state['pasos_motor']:
        if "[RECURSIVA]" in paso:
            st.warning(paso)
        else:
            st.success(paso)

if 'resultado_crudo' in st.session_state and st.session_state['resultado_crudo']:
    st.divider()
    st.subheader("✅ Resultado Final (Sin simplificar)")
    
    # Mostramos el resultado del motor
    res_raw = st.session_state['resultado_crudo']
    expr_sympy = sp.sympify(res_raw)
    st.latex(sp.latex(expr_sympy))

    # --- BOTÓN DE SIMPLIFICACIÓN ---
    st.write("¿Deseas reducir la expresión?")
    if st.button("✨ Simplificar resultado"):
        with st.status("Simplificando matemáticamente...", expanded=False):
            # Aplicamos la simplificación de SymPy
            simplificado = sp.simplify(expr_sympy)
        
        st.info("Resultado Simplificado:")
        st.latex(sp.latex(simplificado))
        
        if str(simplificado) == str(expr_sympy):
            st.caption("Nota: El resultado ya estaba en su forma más simple.")

# Pie de página
st.divider()
st.caption("Desarrollado con Python, SymPy y Experta.")