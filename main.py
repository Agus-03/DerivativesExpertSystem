from rules import DerivadorExperto
from analizer import analizar_funcion

def menu():
    engine = DerivadorExperto()
    while True:
        print("\n" + "="*45)
        print(" SISTEMA EXPERTO PARA DERIVADAS ")
        print("="*45)
        print("Reglas:" \
        "\n  ♦ 3x = 3*x, explicitar los operadores" \
        "\n  ♦ x^2 = x**2, no usamos sombreritos" \
        "\n  ♦ Cuidar la notación de los logaritmos:" \
        "\n      ln(x)    = log(x)" \
        "\n      log_2(x) = log(x,2)" \
        "\n  ♦ En las divisiones usemos paréntesis:" \
        "\n      (a+b)/d" \
        "\n  ♦ Acepta funciones polinomiales, exponenciales, potenciales, logarítmicas, de seno, coseno, tangente y cotangente." \
        "\n  ♦ Escriba 'salir' para dar por terminado el programa")
        
        entrada = input("\nFunción a derivar: ")
        if entrada.lower() == 'salir':
            break
            
        engine.reset()
        analizar_funcion(engine, entrada)

if __name__ == "__main__":
    menu()