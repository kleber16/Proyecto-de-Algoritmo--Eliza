# Archivo: clases/grupo_frases_clave.py
# Autores: Kleber Bauza y Eduardo Chemello
from utilidades.texto import separar_palabras, normalizar


class GrupoFrasesClave:
    """Un grupo de frases clave de entrada (por ejemplo 'Despedida').
    Sabe buscar sus frases dentro de un texto y sacar la palabra del comodin '*'."""

    def __init__(self, nombre, prioridad, frases):
        """Guarda el nombre del grupo, su prioridad y la lista de frases. Eficiencia: O(1)."""
        self.__nombre = nombre
        self.__prioridad = prioridad
        self.__frases = frases

    def get_nombre(self):
        """Devuelve el nombre del grupo. Eficiencia: O(1)."""
        return self.__nombre

    def get_prioridad(self):
        """Devuelve la prioridad del grupo. Eficiencia: O(1)."""
        return self.__prioridad

    def get_frases(self):
        """Devuelve la lista de frases. Eficiencia: O(1)."""
        return self.__frases

    def posicion_de(self, frase, texto):
        """Busca la frase dentro del texto y devuelve el indice de la palabra
        donde empieza, o -1 si no esta. El '*' coincide con cualquier palabra,
        pero esa palabra tiene que existir (si el texto termina antes, no coincide).
        Eficiencia: O(p * f) con p = palabras del texto y f = palabras de la frase."""
        palabras = separar_palabras(texto)
        partes = frase.split()
        i = 0

        # Recorre las posiciones donde podría comenzar la frase clave.
        while i + len(partes) <= len(palabras):
            coincide = True
            j = 0
            while j < len(partes):
                if partes[j] != "*":
                    if normalizar(palabras[i + j]) != normalizar(partes[j]):
                        coincide = False
                j = j + 1
            if coincide:
                return i
            i = i + 1
        return -1

    def esta_en(self, texto):
        """Dice si alguna frase del grupo aparece en el texto.
        Eficiencia: O(k * p * f) con k = cantidad de frases del grupo."""
        for frase in self.__frases:
            if self.posicion_de(frase, texto) != -1:
                return True
        return False

    def frases_encontradas(self, texto):
        """Devuelve la lista de frases del grupo que aparecen en el texto.
        Eficiencia: O(k * p * f), igual que esta_en pero sin parar en la primera."""
        encontradas = []
        for frase in self.__frases:
            if self.posicion_de(frase, texto) != -1:
                encontradas.append(frase)
        return encontradas

    def palabra_despues_asterisco(self, texto, frase):
        """Devuelve la palabra del texto que ocupa el lugar del '*' en la frase.
        Si la frase no tiene '*' o no esta en el texto, devuelve ''.
        Eficiencia: O(p * f)."""
        if "*" not in frase:
            return ""
        posicion = self.posicion_de(frase, texto)
        if posicion == -1:
            return ""
        partes = frase.split()
        lugar_asterisco = partes.index("*")
        palabras = separar_palabras(texto)
        return palabras[posicion + lugar_asterisco]
