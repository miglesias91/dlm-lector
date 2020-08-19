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

class Infobae(Diario):

    def __init__(self):
        Diario.__init__(self, "infobae")

    def leer(self, fechas = {}, categorias = []):
        kiosco = Kiosco()

        print("leyendo '" + self.etiqueta + "'...")

        tag_regexp = re.compile(r'<[^>]+>')
        for entrada in fp.parse(self.feed_noticias).entries:
            url = entrada.link
            if kiosco.contar_noticias(diario=self.etiqueta, url=url): # si existe ya la noticia (url), no la decargo
               continue      
            titulo = entrada.title
            texto = re.sub(tag_regexp,' ',entrada.content[0].value)
            fecha = dateutil.parser.parse(entrada.published)  - datetime.timedelta(hours=3)

            categoria = url.split('/')[3]
            
            if categoria == "america":
                categoria = "internacional"

            if categoria == "teleshow":
                categoria = "espectaculos"

            if categoria == "deportes-2":
                categoria = "deportes"

            if categoria not in self.categorias:
                continue

            self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, categoria=categoria, titulo=titulo, texto=self.limpiar_texto(texto)))

        print(self.etiqueta + " leyo " + str(len(self.noticias)))

    def limpiar_texto(self, texto):
        regexp = re.compile(r'SEGUÍ LEYENDO[^$]+')
        texto = re.sub(regexp,' ',texto)
        regexp = re.compile(r'MÁS SOBRE ESTE TEMA[^$]+')
        texto = re.sub(regexp,' ',texto)
        regexp = re.compile(r'Seguí leyendo[^$]+')
        texto = re.sub(regexp,' ',texto)
        return texto