import re

from medios.contenido import Contenido

class Noticia(Contenido):

    def __init__(self, fecha, url, diario, categoria, titulo, texto):
        Contenido.__init__(self)
        self.fecha = fecha
        self.url = url
        self.diario = diario
        self.categoria = categoria
        self.titulo = titulo
        self.texto = texto
        self.texto = " ".join(re.split("\s+", texto, flags=re.UNICODE))
