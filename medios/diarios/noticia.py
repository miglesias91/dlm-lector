import re

from medios.contenido import Contenido

class Noticia(Contenido):

    def __init__(self, fecha, url, diario, seccion, titulo, texto):
        Contenido.__init__(self)
        self.fecha = fecha
        self.url = url
        self.diario = diario
        self.seccion = seccion
        self.titulo = titulo
        self.texto = texto
        self.texto = " ".join(re.split("\s+", texto, flags=re.UNICODE))
