# Archivo: utilidades/texto.py
# Autores: Kleber Bauza y Eduardo Chemello
# Funciones sencillas para limpiar y separar el texto que escribe el usuario.

# Valor que se guarda cuando el usuario no quiere dar un dato
DESCONOCIDO = "desconocido"

# Signos que se quitan del texto antes de buscar frases
SIGNOS = [".", ",", ";", ":", "!", "?", "¿", "¡", "(", ")", "\"", "'", "-", "_", "/", "…"]

# Palabras de saludo que no pueden ser un nombre
SALUDOS = ["hola", "buenas", "buenos", "hey", "hi"]


def quitar_signos(texto):
    """Reemplaza los signos de puntuacion por espacios.
    Eficiencia: recorre la lista de signos (16) una sola vez, O(s * n)."""
    for signo in SIGNOS:
        texto = texto.replace(signo, " ")
    return texto


def separar_palabras(texto):
    """Devuelve una lista con las palabras del texto, sin signos.
    Eficiencia: un recorrido del texto, O(n)."""
    texto = quitar_signos(texto)
    return texto.split()


def normalizar(palabra):
    """Pasa la palabra a minusculas y le quita las tildes, para que
    'Adiós' y 'adios' se consideren iguales.
    Eficiencia: O(n) con n = largo de la palabra."""
    palabra = palabra.lower()
    palabra = palabra.replace("á", "a")
    palabra = palabra.replace("é", "e")
    palabra = palabra.replace("í", "i")
    palabra = palabra.replace("ó", "o")
    palabra = palabra.replace("ú", "u")
    palabra = palabra.replace("ü", "u")
    return palabra


def quitar_articulo(frase):
    """Quita 'mi ', 'la ' o 'el ' del inicio de una frase.
    Ejemplo: 'mi abuela' -> 'abuela'.
    Eficiencia: O(1), solo revisa 3 articulos."""
    for articulo in ["mi ", "la ", "el "]:
        if frase.startswith(articulo):
            return frase[len(articulo):]
    return frase
