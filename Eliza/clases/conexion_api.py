# Archivo: clases/conexion_api.py
# Autores: Kleber Bauza y Eduardo Chemello
import json
import urllib.request


class ConexionAPI:
    """Descarga los archivos JSON (frases clave y respuestas) del repositorio
    de GitHub del curso.
    Eficiencia: cada descarga es una sola peticion HTTP; el costo lo domina la red."""

    def __init__(self):
        """Guarda la direccion base del repositorio. Eficiencia: O(1)."""
        self.__url = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2627-1/main/"

    def descargar_datos(self, nombre_archivo):
        """Pide el archivo JSON a GitHub y lo devuelve como diccionario.
        Si la descarga falla (sin internet, archivo no encontrado o JSON invalido)
        muestra el error y devuelve un diccionario vacio {}, nunca None.
        Eficiencia: una peticion con tiempo maximo de espera de 10 segundos."""
        try:
            respuesta = urllib.request.urlopen(self.__url + nombre_archivo, timeout=10)
            texto = respuesta.read().decode("utf-8-sig")
            respuesta.close()
            return json.loads(texto)
        except (OSError, ValueError) as error:
            print("No pude descargar " + nombre_archivo + " de GitHub.")
            print("Detalle del error:", error)
            return {}
