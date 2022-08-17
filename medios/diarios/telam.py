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

class Telam(Diario):

    def __init__(self):
        Diario.__init__(self, "telam")
                    
    def leer(self):
        kiosco = Kiosco()

        print("leyendo noticias de '" + self.etiqueta + "'...")

        for seccion, url_feed in self.feeds.items():

            i = 0

            entradas = self.entradas_feed(url_feed=url_feed)[0:3]

            print("     " + str(len(entradas)) + " noticias de '" + self.etiqueta + "/" + seccion + "'...")
            for url, fecha, titulo in entradas:

                i += 1

                # if url in urls_existentes:
                if kiosco.contar_noticias(diario=self.etiqueta, url=url):
                    print("     noticia " + str(i) + "/" + str(len(entradas)) +" ya descargada")
                    continue

                print("     descargando noticia " + str(i) + "/" + str(len(entradas)))
                texto = self.parsear_noticia(url=url)
                if texto == None:
                    continue
                self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, seccion=seccion, titulo=titulo, texto=texto))

    def entradas_feed(self, url_feed):
        entradas = []
        for entrada in fp.parse(url_feed).entries:
            titulo = str(entrada.title)
            fecha = dateutil.parser.parse(entrada.published, ignoretz=True)
            url = str(entrada.link)
            entradas.append((url, fecha, titulo))
        return entradas

    def parsear_noticia(self, url):
        articulo = np.Article(url=url, language='es')
        try:
            articulo.download()
            articulo.parse()
        except:
            return None

        return articulo.text