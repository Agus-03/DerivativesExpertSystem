# DerivativeExpert-SBC
DerivativeExpert es un sistema experto basado en reglas diseñado para la derivación simbólica de funciones matemáticas. A diferencia de un calculador estándar, este sistema utiliza un motor de inferencia para explicar paso a paso qué reglas de cálculo se están aplicando (Suma, Producto, Cadena, etc.), emulando el razonamiento de un experto en matemáticas.

## Características
- Motor de Inferencia: Desarrollado con Experta para la ejecución de reglas lógicas.
- Análisis Simbólico: Utiliza SymPy para descomponer funciones en Árboles de Sintaxis Abstracta (AST).
- Explicación Paso a Paso: Clasifica las operaciones en Casos Recursivos (descomposición) y Casos Atómicos (resolución final).
- Interfaz Web: Frontend interactivo construido con Streamlit.
- Soporte Avanzado: Gestiona funciones trigonométricas, exponenciales, logaritmos de cualquier base y reglas de la cadena anidadas.

## Tecnologías utilizadas
- Python 3.10+
- Experta: Para la implementación de la base de conocimientos y el motor de reglas.
- SymPy: Para el parsing y manipulación simbólica de expresiones.
- Streamlit: Para la interfaz de usuario moderna.

## Reglas del Sistema
El sistema opera bajo una jerarquía de reglas:
1. Reglas de Estructura (Recursivas): Descomponen la función (Ej: $\frac{d}{dx}[f(x) \cdot g(x)]$).
2. Reglas de Composición: Implementan la Regla de la Cadena para funciones anidadas como $\sin(x^2)$
3. Reglas de Operación (Atómicas): Resolución directa de identidades, constantes y potencias simples.

## Instalación rápida
1. Clonar el repositorio
2. Ejecutar la aplicación:

    ```python run.py```

    *El script configurará automáticamente las librerías necesarias e iniciará la interfaz web.*