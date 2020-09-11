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

#from bd.kiosco import Kiosco
from bd.kioscomongo import Kiosco

class Popular(Diario):

    def __init__(self):
        Diario.__init__(self, "popular")

    def leer(self):
        kiosco = Kiosco()

        entradas = self.getTuplas()[0:70]

        print("leyendo " + str(len(entradas)) + " noticias de '" + self.etiqueta + "'...")

        i = 0
        for url, fecha, categoria in entradas:
            i += 1

            # if url in urls_existentes:
            if kiosco.contar_noticias(diario=self.etiqueta, categorias=categoria, url=url):
                print("noticia " + str(i) + "/" + str(len(entradas)) +" ya descargada")
                continue

            print("descargando noticia " + str(i) + "/" + str(len(entradas)))
            titulo, texto = self.parsearNoticia(url)

            if categoria == "futbol":
                categoria = "deportes"
            
            if categoria not in self.categorias:
                categoria = "varios"

            self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, categoria=categoria, titulo=titulo, texto=self.limpiar_texto(texto)))

    def parsearNoticia(self, url):
        articulo = np.Article(url=url, language='es')
        try:
            articulo.download()
            articulo.parse()
        except:
            return None

        return articulo.title, articulo.meta_description + '\n' + self.limpiar_texto(articulo.text)

    def limpiar_texto(self, texto):
        regexp = re.compile(r'ADEMÁS:\n\n[^\n]*\n\n[^\n]*\n')
        return re.sub(regexp,' ',texto)

    def getTuplas(self):
        req = Request(self.feed_noticias, headers={'User-Agent': 'Mozilla/5.0'})
        campos = bs(urlopen(req).read(), 'html.parser').text.split()[:-3]

        tuplas = []
        while len(campos) > 1:
            url = str(campos.pop(0))
            try:
                fecha = dateutil.parser.parse(campos.pop(0), ignoretz=True)
                categoria = str(url.split('/')[3])
            except:
                continue
            tuplas.append((url, fecha, categoria))
        return tuplas