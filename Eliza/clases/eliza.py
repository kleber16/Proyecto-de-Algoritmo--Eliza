# Archivo: clases/eliza.py
# Autores: Kleber Bauza y Eduardo Chemello

from clases.conexion_api import ConexionAPI
from clases.archivo import Archivo
from clases.persona import Persona
from clases.grupo_frases_clave import GrupoFrasesClave
from clases.grupo_respuestas import GrupoRespuestas
from utilidades.texto import separar_palabras, normalizar, quitar_articulo, DESCONOCIDO, SALUDOS


class Eliza:
    """Clase principal del programa. Lee lo que escribe el usuario, busca
    frases clave por prioridad, recopila informacion de las personas y
    responde con mensajes al azar.
    Eficiencia general: por cada mensaje se revisan los 12 grupos de frases,
    asi que el costo crece con la cantidad de frases (lineal) y no con la
    cantidad de mensajes."""

    def __init__(self):
        """Crea ELIZA vacia; los datos se cargan despues en iniciar(). Eficiencia: O(1)."""
        self.__grupos_frases = []        # 12 grupos de entrada
        self.__grupos_respuestas = []    # 13 grupos de salida (con el conversacional)
        self.__grupos_personas = {}      # grupos de personas.json
        self.__grupos_lugares = {}       # grupos de lugares.json
        self.__personas = []             # personas mencionadas (sin el usuario)
        self.__usuario = Persona("", "", "usuario")
        self.__persona_pendiente = None  # persona sobre la que se hizo una pregunta
        self.__terminar = False
        self.__api = ConexionAPI()
        self.__archivo = Archivo()

    # ------------------------------------------------------------------
    # Inicio del programa
    # ------------------------------------------------------------------
    def iniciar(self):
        """Descarga los JSON por la API y arma los grupos de frases y respuestas.
        Devuelve True si todo salio bien y False si no hay datos.
        Eficiencia: O(g * f), se recorre cada frase una sola vez."""
        entrada = self.__api.descargar_datos("entrada.json")
        salida = self.__api.descargar_datos("salida.json")
        personas = self.__api.descargar_datos("personas.json")
        lugares = self.__api.descargar_datos("lugares.json")
        if len(entrada) == 0 or len(salida) == 0 or len(personas) == 0 or len(lugares) == 0:
            print("Error: no se pudieron descargar los datos. Revisa tu conexion a internet.")
            return False
        try:

            # Crea los grupos de frases clave con los datos del JSON.
            # Crea los grupos de respuestas con los datos del JSON.
            for nombre in entrada:
                grupo = entrada[nombre]
                nuevo = GrupoFrasesClave(nombre, grupo["Prioridad"], grupo["Frases clave"])
                self.__grupos_frases.append(nuevo)
            for nombre in salida:
                grupo = salida[nombre]
                nuevo = GrupoRespuestas(nombre, grupo["Prioridad"], grupo["Frases clave"])
                self.__grupos_respuestas.append(nuevo)
            self.__grupos_personas = self.armar_grupos(personas)
            self.__grupos_lugares = self.armar_grupos(lugares)
        except (KeyError, TypeError):
            print("Error: los archivos JSON no tienen el formato esperado.")
            return False
        if len(self.__grupos_frases) == 0 or len(self.__grupos_respuestas) == 0:
            print("Error: no se pudieron cargar los datos de ELIZA.")
            return False
        return True

    def armar_grupos(self, datos):
        """Convierte un JSON de personas o lugares en un diccionario de grupos.
        Los que empiezan con 'Preguntar' son mensajes (GrupoRespuestas) y los
        'Reconocer' son frases clave (GrupoFrasesClave).
        Eficiencia: O(g * f)."""
        grupos = {}
        for nombre in datos:
            frases = datos[nombre]["Frases clave"]
            if nombre.startswith("Preguntar"):
                grupos[nombre] = GrupoRespuestas(nombre, 0, frases)
            else:
                grupos[nombre] = GrupoFrasesClave(nombre, 0, frases)
        return grupos

    # ------------------------------------------------------------------
    # Conversacion
    # ------------------------------------------------------------------
    def conversar(self):
        """Ciclo principal: lee el mensaje, responde y repite hasta la despedida.
        Si el usuario cierra la entrada (Ctrl+C o Ctrl+D) se trata como despedida
        para que igual se guarden los datos.
        Eficiencia: O(m) con m = cantidad de mensajes del usuario."""
        # El saludo incluye la primera pregunta (el nombre del usuario)
        print("Eliza: Hola, soy Eliza. " + self.preguntar_dato_faltante())
        while not self.__terminar:
            try:
                texto = input("Tú: ")
            except (EOFError, KeyboardInterrupt):
                print("")
                texto = "adiós"
            respuesta = self.responder(texto)
            print("Eliza: " + respuesta)

    def responder(self, texto):
        """Recibe el texto del usuario y devuelve la respuesta de ELIZA.
        Pasos: 1) valida el texto, 2) registra personas (prioridad 3 siempre se
        revisa), 3) busca la frase clave, 4) despedida, 5) respuesta a una
        pregunta pendiente, 6) respuesta normal.
        Eficiencia: O(g * f) por mensaje."""
        palabras = separar_palabras(texto)
        if len(palabras) == 0:
            return "No logré leer palabras en tu mensaje. Por favor escribe con letras."

        mencionadas = self.registrar_personas(texto)
        grupo = self.buscar_frase_clave(texto)

        # Las perdidas reciben un pesame aunque haya una pregunta pendiente.
        if grupo is not None and grupo.get_prioridad() == 2:
            return self.elegir_respuesta(grupo.get_nombre())


        # Prioridad 1: despedida (guarda los datos y termina)
        if grupo != None and grupo.get_prioridad() == 1:
            self.guardar_datos()
            self.__terminar = True
            return self.elegir_respuesta(grupo.get_nombre())

        # Si ELIZA hizo una pregunta antes, este mensaje puede ser la respuesta
        if self.__persona_pendiente != None:
            persona = self.__persona_pendiente

            valor = self.extraer_dato(texto, persona, grupo)

            if valor != "":
                self.__persona_pendiente = None
                return self.guardar_dato(persona, valor)

            return "Disculpa, no entendí ese dato. " + self.preguntar_dato_faltante()
        
            # Busca una persona mencionada que tenga datos incompletos.
        if len(mencionadas) > 0:

            if grupo != None and grupo.get_prioridad() != 3:
                mensaje = self.elegir_respuesta(grupo.get_nombre())
            else:
                mensaje = self.mensaje_freudiano(mencionadas)

            for persona in mencionadas:

                if not persona.esta_completa():

                    self.__persona_pendiente = persona

                    if persona.dato_que_falta() == "nombre":
                        pregunta = (
                            "Háblame de tu "
                            + persona.get_relacion()
                            + ". "
                            + self.__grupos_personas["Preguntar relación"].elegir_mensaje()
                        )

                    else:
                        pregunta = (
                            "Háblame de tu "
                            + persona.get_relacion()
                            + ". "
                            + self.__grupos_lugares["Preguntar relación"].elegir_mensaje()
                    )

                    return mensaje + " " + pregunta

            return mensaje

        if grupo == None:
            return self.preguntar_dato_faltante()

        return self.elegir_respuesta(grupo.get_nombre())

     # Recorre las prioridades de mayor a menor importancia.
    # Busca coincidencias en los grupos de la prioridad actual.
    def buscar_frase_clave(self, texto):
        """Busca el grupo de frases clave de mayor prioridad (numero mas bajo)
        que aparezca en el texto. Revisa todo el grupo de prioridad 1 antes de
        pasar al 2, y asi sucesivamente. Devuelve None si no hay ninguno.
        Eficiencia: O(n * g * f), con n = cantidad de prioridades."""
        for prioridad in range(1, len(self.__grupos_frases) + 1):
            for grupo in self.__grupos_frases:
                if grupo.get_prioridad() == prioridad and grupo.esta_en(texto):
                    return grupo
        return None

    def elegir_respuesta(self, nombre_grupo):
        """Elige un mensaje al azar del grupo de respuestas con ese nombre.
        Eficiencia: O(g), se busca el grupo por nombre."""
        for grupo in self.__grupos_respuestas:
            if grupo.get_nombre() == nombre_grupo:
                return grupo.elegir_mensaje()
        return "Cuéntame más."

    # ------------------------------------------------------------------
    # Recopilacion de informacion sobre personas
    # ------------------------------------------------------------------
    def registrar_personas(self, texto):
        """Revisa SIEMPRE las frases de prioridad 3 y agrega a la lista las
        personas nuevas que se mencionen (la relacion es la frase detectada).
        Devuelve la lista de personas mencionadas en este mensaje.
        Eficiencia: O(k * p * f) con k = frases de prioridad 3."""
        mencionadas = []

        # Recorre los grupos para encontrar los de prioridad 3.
        # Recorre las frases encontradas para identificar la relación de cada persona.
        for grupo in self.__grupos_frases:
            if grupo.get_prioridad() == 3:
                for frase in grupo.frases_encontradas(texto):
                    if "*" in frase:
                        relacion = grupo.palabra_despues_asterisco(texto, frase).lower()
                    else:
                        relacion = frase
                    relacion = quitar_articulo(relacion)
                    if relacion.isalpha():
                        persona = self.buscar_persona(relacion)
                        if persona == None:
                            persona = Persona("", "", relacion)
                            self.__personas.append(persona)
                        if persona not in mencionadas:
                            mencionadas.append(persona)
        return mencionadas

    def buscar_persona(self, relacion):
        """Busca en la lista una persona con esa relacion. Devuelve None si no esta.
        Eficiencia: O(n) con n = personas mencionadas."""
        for persona in self.__personas:
            if normalizar(persona.get_relacion()) == normalizar(relacion):
                return persona
        return None

    def mensaje_freudiano(self, mencionadas):
        """Si una persona mencionada ya tiene nombre, lo usa en la pregunta
        (por ejemplo '¿Tu abuela llamada Alicia?'). Si no, usa un mensaje
        freudiano normal. Eficiencia: O(n) con n = personas mencionadas."""
        for persona in mencionadas:
            nombre = persona.get_nombre()
            if nombre != "" and nombre != DESCONOCIDO:
                relacion = persona.get_relacion()
                llamado = "llamado"
                if relacion.endswith("a") or relacion == "madre" or relacion == "mamá":
                    llamado = "llamada"
                return "¿Tu " + relacion + " " + llamado + " " + nombre + "?"
        return self.elegir_respuesta("Freudiano")

    def preguntar_dato_faltante(self):
        """Pregunta el primer dato que falte: primero los del usuario, luego los
        de las personas mencionadas. Si no falta nada, manda un mensaje
        conversacional (prioridad 0). Deja guardada la persona sobre la que se pregunta.
        Eficiencia: O(n) con n = personas mencionadas."""
        if not self.__usuario.esta_completa():
            self.__persona_pendiente = self.__usuario
            if self.__usuario.dato_que_falta() == "nombre":
                return self.__grupos_personas["Preguntar usuario"].elegir_mensaje()
            return self.__grupos_lugares["Preguntar usuario"].elegir_mensaje()

        for persona in self.__personas:
            if not persona.esta_completa():
                self.__persona_pendiente = persona
                introduccion = "Háblame de tu " + persona.get_relacion() + ". "
                if persona.dato_que_falta() == "nombre":
                    return introduccion + self.__grupos_personas["Preguntar relación"].elegir_mensaje()
                return introduccion + self.__grupos_lugares["Preguntar relación"].elegir_mensaje()

        return self.elegir_respuesta("Conversacional")

    def buscar_palabra_en(self, grupo, texto):
        """Si alguna frase del grupo (con '*') aparece en el texto, devuelve la
        palabra del asterisco. Si no, devuelve ''. Eficiencia: O(k * p * f)."""
        frases = grupo.frases_encontradas(texto)
        if len(frases) > 0:
            return grupo.palabra_despues_asterisco(texto, frases[0])
        return ""

    def extraer_dato(self, texto, persona, grupo):
        """Saca del texto la respuesta a la pregunta pendiente (nombre u origen).
        Usa las frases que reconocen nombres/lugares/gentilicios; si no hay,
        toma la primera palabra. Devuelve '' si el texto no parece una respuesta
        (tiene letras raras, es muy largo o es otra frase clave).
        Si el usuario responde 'no' se guarda 'desconocido'.
        Eficiencia: O(k * p * f)."""
        palabras = separar_palabras(texto)
        if len(palabras) <= 2 and normalizar(palabras[0]) == "no":
            return DESCONOCIDO

        if persona.dato_que_falta() == "nombre":
            if persona is self.__usuario:
                reconocedor = self.__grupos_personas["Reconocer usuario"]
            else:
                reconocedor = self.__grupos_personas["Reconocer relación"]
            valor = self.buscar_palabra_en(reconocedor, texto)
        else:
            valor = self.buscar_palabra_en(self.__grupos_lugares["Reconocer lugar"], texto)
            if valor == "":
                valor = self.buscar_palabra_en(self.__grupos_lugares["Reconocer gentilicio"], texto)

        if valor == "":
            if grupo != None or len(palabras) > 3:
                return ""
            valor = palabras[0]
            if normalizar(valor) in SALUDOS:
                if len(palabras) == 1:
                    return ""
                valor = palabras[1]

        if not valor.isalpha():
            return ""
        return valor

    def guardar_dato(self, persona, valor):
        """Guarda el nombre u origen recibido y pregunta el siguiente dato faltante.
        Si es el nombre del usuario, intenta cargar su archivo anterior.
        Eficiencia: O(1) mas el costo de cargar_datos y preguntar_dato_faltante."""
        dato_faltante = persona.dato_que_falta()

        if valor != DESCONOCIDO:
            valor = valor.capitalize()

        if dato_faltante == "nombre":

            persona.set_nombre(valor)

            if persona is self.__usuario and valor != DESCONOCIDO:
                if self.cargar_datos(valor):
                    return (
                        "Gracias, continúa. Qué bueno verte de nuevo, "
                        + valor
                        + ". "
                        + self.preguntar_dato_faltante()
                    )

        else:
            persona.set_origen(valor)

        return "Gracias, continúa. " + self.preguntar_dato_faltante()
    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------
    def nombre_de_archivo(self):
        """Devuelve el nombre del archivo del usuario: su nombre en minusculas
        + '.txt', o 'usuario.txt' si no dio su nombre. Eficiencia: O(1)."""
        nombre = self.__usuario.get_nombre()
        if nombre == "" or nombre == DESCONOCIDO:
            return "usuario.txt"
        return nombre.lower() + ".txt"

    def guardar_datos(self):
        """Guarda al usuario y a las personas mencionadas en el archivo.
        Eficiencia: O(n) con n = personas."""
        lista = [self.__usuario] + self.__personas
        nombre_archivo = self.nombre_de_archivo()
        if self.__archivo.guardar(lista, nombre_archivo):
            print("(Información guardada en datos_usuarios/" + nombre_archivo + ")")
        else:
            print("(No pude guardar la información en el archivo.)")

    def cargar_datos(self, nombre):
        """Si existe un archivo con el nombre del usuario, mezcla sus datos con
        los de esta conversacion. Si un dato esta en los dos lugares, queda el
        de la conversacion actual (el mas reciente); el archivo solo rellena
        lo que falta. Devuelve True si encontro el archivo.
        Eficiencia: O(n * m) con n = personas del archivo y m = personas actuales."""
        nombre_archivo = nombre.lower() + ".txt"
        if not self.__archivo.existe(nombre_archivo):
            return False
        for guardada in self.__archivo.cargar(nombre_archivo):
            if guardada.get_relacion() == "usuario":
                self.completar(self.__usuario, guardada)
            else:
                actual = self.buscar_persona(guardada.get_relacion())
                if actual == None:
                    self.__personas.append(guardada)
                else:
                    self.completar(actual, guardada)
        return True

    def completar(self, actual, guardada):
        """Copia a 'actual' los datos de 'guardada' solo si 'actual' no los tiene.
        Eficiencia: O(1)."""
        if actual.get_nombre() == "":
            actual.set_nombre(guardada.get_nombre())
        if actual.get_origen() == "":
            actual.set_origen(guardada.get_origen())
