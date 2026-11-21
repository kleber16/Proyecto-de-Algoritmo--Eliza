# Archivo: main.py
# Autores: Kleber Bauza y Eduardo Chemello
# Programa principal del proyecto "El Efecto ELIZA".
# Se ejecuta con:  python main.py
from clases.eliza import Eliza


def main():
    """Crea a ELIZA, carga sus datos y empieza la conversacion.
    Eficiencia: O(1) por si sola, el costo esta en Eliza."""
    eliza = Eliza()
    if eliza.iniciar():
        eliza.conversar()
    else:
        print("No se pudo iniciar el programa.")


if __name__ == "__main__":
    main()
