import subprocess
import sys
import importlib.util

def install_and_launch():
    # 1. Lista de dependencias necesarias
    required = ["experta", "sympy", "streamlit", "frozendict==1.2"]
    
    # Verificamos qué librerías faltan realmente
    for lib in required:
        # Extraemos el nombre base (sin versiones) para verificar
        lib_name = lib.split('==')[0]
        if importlib.util.find_spec(lib_name) is None:
            print(f"Instalando dependencia faltante: {lib}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib], 
                                      stdout=subprocess.DEVNULL) # Silenciamos el log de pip
            except Exception as e:
                print(f"Error al instalar {lib}: {e}")
                sys.exit(1)

    # 2. Lanzar la aplicación
    print("\n" + "="*30)
    print("Iniciando Sistema Experto...")
    print("="*30 + "\n")
    
    try:
        # USAMOS sys.executable -m streamlit para asegurar que use el mismo Python
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\nPrograma finalizado por el usuario.")
    except Exception as e:
        print(f"Error al iniciar la interfaz: {e}")

if __name__ == "__main__":
    install_and_launch()