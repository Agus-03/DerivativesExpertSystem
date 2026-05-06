# --- PARCHE DE COMPATIBILIDAD PARA PYTHON 3.10+ ---
import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
# --------------------------------------------------

from experta import *

class Operacion(Fact):
    """Hecho que representa un componente de la función"""
    pass

class DerivadorExperto(KnowledgeEngine):

    # ==========================================
    # CASOS RECURSIVOS (Estructura y Composición)
    # ==========================================

    @Rule(Operacion(tipo='Add'))
    def regla_suma(self):
        print("\n[RECURSIVA] Regla de Linealidad: d/dx[f(x) ± g(x)]")
        print("-> Lógica: 'Deriva cada sumando por separado: f'(x) ± g'(x)'")

    @Rule(Operacion(tipo='Mul', tiene_constante=True))
    def regla_constante_por_f(self):
        print("\n[RECURSIVA] Factor Constante: d/dx[c * f(x)]")
        print("-> Lógica: 'Saca la constante: c * f'(x)'")

    @Rule(Operacion(tipo='Mul', tiene_constante=False))
    def regla_producto(self):
        print("\n[RECURSIVA] Regla del Producto: d/dx[u * v]")
        print("-> Lógica: 'f'(x)g(x) + f(x)g'(x)'")

    @Rule(Operacion(tipo='Div'))
    def regla_cociente(self):
        print("\n[RECURSIVA] Regla del Cociente: d/dx[u / v]")
        print("-> Lógica: '[f'(x)g(x) - f(x)g'(x)] / [g(x)]^2'")

    # --- TRIGONOMÉTRICAS RECURSIVAS (Regla de la cadena implícita) ---
    @Rule(Operacion(tipo='sin', arg=MATCH.u))
    def regla_sin(self, u):
        print(f"\n[RECURSIVA] Derivada del Seno: d/dx[sin({u})]")
        print(f"-> Lógica: 'cos({u}) * d/dx({u})'")

    @Rule(Operacion(tipo='cos', arg=MATCH.u))
    def regla_cos(self, u):
        print(f"\n[RECURSIVA] Derivada del Coseno: d/dx[cos({u})]")
        print(f"-> Lógica: '-sin({u}) * d/dx({u})'")

    @Rule(Operacion(tipo='tan', arg=MATCH.u))
    def regla_tan(self, u):
        print(f"\n[RECURSIVA] Derivada de la Tangente: d/dx[tan({u})]")
        print(f"-> Lógica: 'sec^2({u}) * d/dx({u})'")

    # --- EXPONENCIALES Y LOGARITMOS RECURSIVOS ---
    @Rule(Operacion(tipo='exp', arg=MATCH.u))
    def regla_exp(self, u):
        print(f"\n[RECURSIVA] Derivada Exponencial: d/dx[e^({u})]")
        print(f"-> Lógica: 'e^({u}) * d/dx({u})'")

    @Rule(Operacion(tipo='log', arg=MATCH.u))
    def regla_ln(self, u):
        print(f"\n[RECURSIVA] Derivada Logaritmo Natural: d/dx[ln({u})]")
        print(f"-> Lógica: '(1/{u}) * d/dx({u})'")

    @Rule(Operacion(tipo='log_base_n', base=MATCH.a, arg=MATCH.u))
    def regla_log_base_n(self, a, u):
        print(f"\n[RECURSIVA] Logaritmo Base {a}: d/dx[log_{a}({u})]")
        print(f"-> Lógica: '1 / ({u} * ln({a})) * d/dx({u})'")

    # ==========================================
    # CASOS ATÓMICOS (Nivel Final)
    # ==========================================

    @Rule(Operacion(tipo='Pow', base='x', exp=MATCH.n))
    def regla_potencia(self, n):
        print(f"-> [ATÓMICA] Potencia: d/dx(x^{n}) = {n}x^{int(n)-1}")

    @Rule(Operacion(tipo='Identidad'))
    def regla_x(self):
        print("-> [ATÓMICA] Identidad: d/dx(x) = 1")

    @Rule(Operacion(tipo='Constante'))
    def regla_c(self):
        print("-> [ATÓMICA] Constante: d/dx(c) = 0")