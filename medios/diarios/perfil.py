import dateutil
import datetime
import yaml
import feedparser as fp
import newspaper as np
import re

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs

from medios.medio import Medio
from medios.diarios.noticia import Noticia
from medios.diarios.diario import Diario

from bd.entidades import Kiosco

class Perfil(Diario):

    def __init__(self):
        Diario.__init__(self, "perfil")
                    
    def leer(self, fecha, categorias):
        kiosco = Kiosco()

        print("leyendo '" + self.etiqueta + "'...")

        for categoria, url_feed in self.feeds.items():
            for url, fecha, titulo in self.entradas_feed(url_feed=url_feed):
                if kiosco.contar_noticias(diario=self.etiqueta, url=url): # si existe ya la noticia (url), no la decargo
                    continue
                texto = self.parsear_noticia(url=url)
                if texto == None:
                    continue
                self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, categoria=categoria, titulo=titulo, texto=texto))

    def entradas_feed(self, url_feed):
        entradas = []
        for entrada in fp.parse(url_feed).entries:
            titulo = entrada.title
            fecha = dateutil.parser.parse(entrada.published)
            url = entrada.link
            entradas.append((url, fecha, titulo))
        return entradas

    def parsear_noticia(self, url):
        articulo = np.Article(url=url, language='es')
        try:
            articulo.download()
            articulo.parse()
        except:
            return None

        return self.limpiar_texto(articulo.text)

    def limpiar_texto(self, texto):
        regexp = re.compile(r'^[^\n]+\n')
        texto = re.sub(regexp,' ',texto)
        regexp = re.compile(r'\n[^\n]+$')
        texto = re.sub(regexp,' ',texto)
        texto = texto.replace('\n\n', ' ')
        return texto