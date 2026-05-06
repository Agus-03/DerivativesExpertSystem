import sympy as sp
from rules import Operacion

def analizar_funcion(engine, texto):
    x = sp.Symbol('x')
    try:
        expr = sp.sympify(texto)
        # Recorremos el árbol de la función
        for nodo in sp.preorder_traversal(expr):
            tipo = type(nodo).__name__
            if tipo == 'Add':
                engine.declare(Operacion(tipo='Add'))
            elif tipo == 'Mul':
                tiene_c = any(arg.is_Number for arg in nodo.args)
                engine.declare(Operacion(tipo='Mul', tiene_constante=tiene_c))
            elif tipo == 'Pow':
                if nodo.args[0] == x:
                    engine.declare(Operacion(tipo='Pow', base='x', exp=nodo.args[1]))
            elif tipo in ['sin', 'cos', 'tan', 'exp', 'log']:
                engine.declare(Operacion(tipo=tipo, arg=str(nodo.args[0])))
            elif tipo == 'log':
                argumento = nodo.args[0]
                # Si tiene 2 argumentos, el segundo es la base. Si no, la base es 'e'
                if len(nodo.args) > 1:
                    base = nodo.args[1]
                    engine.declare(Operacion(tipo='log_base_n', base=str(base), arg=str(argumento)))
                else:
                    # Es logaritmo natural
                    engine.declare(Operacion(tipo='log', arg=str(argumento)))
            elif nodo.is_Symbol:
                engine.declare(Operacion(tipo='Identidad'))
            elif nodo.is_Number and nodo == expr:
                engine.declare(Operacion(tipo='Constante'))
        
        engine.run()
        derivada = sp.diff(expr, x)
        print(f"SOLUCION_FINAL:{derivada}")
        #print(f"\nRESULTADO MATEMÁTICO: {sp.diff(expr, x)}")
    except Exception as e:
        print(f"Error: {e}")