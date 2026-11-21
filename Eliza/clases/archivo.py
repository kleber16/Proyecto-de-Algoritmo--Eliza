# Archivo: clases/archivo.py
# Autores: Kleber Bauza y Eduardo Chemello
import os
from clases.persona import Persona


class Archivo:
    """Se encarga de guardar y cargar las personas en archivos de texto.

    Formato del archivo (una persona por linea, separada por ';'):
        nombre;origen;relacion
    La primera linea siempre es el usuario (su relacion es 'usuario').
    Los datos que no se conocen quedan vacios. Ejemplo:
        Kleber;Venezuela;usuario
        Alicia;Cuba;abuela
        ;;tio
    """

    def __init__(self):
        """Define la carpeta 'datos_usuarios' junto a main.py. Eficiencia: O(1)."""
        # Se calcula la ruta desde este archivo para que funcione
        # sin importar desde donde se ejecute el programa.
        carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__carpeta = os.path.join(carpeta_proyecto, "datos_usuarios")

    def __ruta(self, nombre_archivo):
        """Devuelve la ruta completa de un archivo. Eficiencia: O(1)."""
        return os.path.join(self.__carpeta, nombre_archivo)

    def existe(self, nombre_archivo):
        """Dice si el archivo existe. Eficiencia: O(1)."""
        return os.path.isfile(self.__ruta(nombre_archivo))

    def guardar(self, personas, nombre_archivo):
        """Escribe la lista de personas en el archivo (lo reemplaza si ya existe).
        Devuelve True si pudo guardar y False si hubo un error.
        Eficiencia: O(n), una linea por persona."""
        try:
            os.makedirs(self.__carpeta, exist_ok=True)
            with open(self.__ruta(nombre_archivo), "w", encoding="utf-8") as archivo:
                for persona in personas:
                    linea = persona.get_nombre() + ";" + persona.get_origen() + ";" + persona.get_relacion()
                    archivo.write(linea + "\n")
            return True
        except OSError:
            return False

    def cargar(self, nombre_archivo):
        """Lee el archivo y devuelve una lista de objetos Persona.
        Las lineas mal formadas se ignoran. Si hay error, devuelve lista vacia.
        Eficiencia: O(n), se lee cada linea una sola vez."""
        personas = []
        try:
            with open(self.__ruta(nombre_archivo), "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    partes = linea.strip().split(";")
                    if len(partes) == 3 and partes[2] != "":
                        personas.append(Persona(partes[0], partes[1], partes[2]))
        except OSError:
            return []
        return personas
