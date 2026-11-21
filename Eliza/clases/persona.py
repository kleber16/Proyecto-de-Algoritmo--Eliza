# Archivo: clases/persona.py
# Autores: Kleber Bauza y Eduardo Chemello


class Persona:
    """Guarda la informacion de una persona mencionada (o del usuario):
    nombre, lugar de origen y relacion con el usuario.
    Eficiencia: todos los metodos son O(1), solo comparan strings."""

    def __init__(self, nombre="", origen="", relacion=""):
        """Crea la persona. Los datos que no se conocen quedan como ''. Eficiencia: O(1)."""
        self.__nombre = nombre
        self.__origen = origen
        self.__relacion = relacion

    def get_nombre(self):
        """Devuelve el nombre. Eficiencia: O(1)."""
        return self.__nombre

    def set_nombre(self, nombre):
        """Cambia el nombre. Eficiencia: O(1)."""
        self.__nombre = nombre

    def get_origen(self):
        """Devuelve el lugar de origen. Eficiencia: O(1)."""
        return self.__origen

    def set_origen(self, origen):
        """Cambia el lugar de origen. Eficiencia: O(1)."""
        self.__origen = origen

    def get_relacion(self):
        """Devuelve la relacion con el usuario. Eficiencia: O(1)."""
        return self.__relacion

    def set_relacion(self, relacion):
        """Cambia la relacion con el usuario. Eficiencia: O(1)."""
        self.__relacion = relacion

    def esta_completa(self):
        """Dice si ya se conocen el nombre y el origen.
        (La relacion siempre se conoce porque se detecta sola.)
        Eficiencia: O(1)."""
        return self.__nombre != "" and self.__origen != ""

    def dato_que_falta(self):
        """Devuelve 'nombre' u 'origen' segun lo que falte, o '' si esta completa.
        Eficiencia: O(1)."""
        if self.__nombre == "":
            return "nombre"
        if self.__origen == "":
            return "origen"
        return ""
