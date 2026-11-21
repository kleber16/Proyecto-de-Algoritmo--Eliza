# Archivo: clases/grupo_respuestas.py
# Autores: Kleber Bauza y Eduardo Chemello
import random


class GrupoRespuestas:
    """Un grupo de mensajes de salida de ELIZA (por ejemplo 'Pesame').
    Eficiencia: elegir un mensaje es O(m), con m = mensajes del grupo (maximo ~20),
    porque quitar el mensaje usado de la lista recorre la lista."""

    def __init__(self, nombre, prioridad, mensajes):
        """Guarda el nombre, la prioridad, los mensajes y una copia de los mensajes
        todavia no usados. Eficiencia: O(m) por la copia de la lista."""
        self.__nombre = nombre
        self.__prioridad = prioridad
        self.__mensajes = mensajes
        self.__mensajes_disponibles = mensajes.copy()

    def get_nombre(self):
        """Devuelve el nombre del grupo. Eficiencia: O(1)."""
        return self.__nombre

    def get_prioridad(self):
        """Devuelve la prioridad del grupo. Eficiencia: O(1)."""
        return self.__prioridad

    def elegir_mensaje(self):
        """Elige un mensaje al azar sin repetir hasta usar todos; cuando se acaban,
        vuelve a llenar la lista de disponibles.
        Eficiencia: O(m), por el remove() sobre la lista de disponibles."""

        if len(self.__mensajes) == 0:
            return ""

        if len(self.__mensajes_disponibles) == 0:
            self.__mensajes_disponibles = self.__mensajes.copy()

        mensaje = random.choice(self.__mensajes_disponibles)

        self.__mensajes_disponibles.remove(mensaje)

        return mensaje