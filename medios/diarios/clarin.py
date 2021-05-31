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

class Clarin(Diario):

    def __init__(self):
        Diario.__init__(self, "clarin")
                    
    def leer(self):
        kiosco = Kiosco()

        entradas = self.entradas_feed()[0:70]

        print("leyendo " + str(len(entradas)) + " noticias de '" + self.etiqueta + "'...")

        i = 0
        for url, fecha, titulo, seccion in entradas:
            
            i += 1

            #if url in urls_existentes:
            if kiosco.contar_noticias(diario=self.etiqueta, url=url):
                print("noticia " + str(i) + "/" + str(len(entradas)) +" ya descargada")
                continue

            print("descargando noticia " + str(i) + "/" + str(len(entradas)))
            texto = self.parsear_noticia(url=url)
            if texto == None:
                continue
            self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, seccion=seccion, titulo=titulo, texto=texto))

    def entradas_feed(self):
        urls_fechas_titulo_seccion = []
        req = Request(self.feed_noticias, headers={'User-Agent': 'Mozilla/5.0'})
        rss = urlopen(req)
        feed = bs(rss.read(), 'html.parser')
        for entrada in feed.find_all('url'):
             # creo objetos str xq sino mas adelante tira RecursionError.            
            url = str(entrada.loc.string)
            fecha = dateutil.parser.parse(entrada.find('news:publication_date').string, ignoretz=True)
            titulo = str(entrada.find('news:title').string)
            seccion = str(url.split('/')[3])

            if seccion == "mundo":
                seccion = "internacional"

            if seccion not in self.secciones:
                continue

            urls_fechas_titulo_seccion.append((url, fecha, titulo, seccion))
            
        return urls_fechas_titulo_seccion

    def parsear_noticia(self, url):
        articulo = np.Article(url=url, language='es')
        try:
            articulo.download()
            articulo.parse()
        except:
            return None

        return self.limpiar_texto(articulo.text)

    def limpiar_texto(self, texto):
        regexp = re.compile(r'[\n\s]Newsletters[^\n]+\n')
        texto = re.sub(regexp,' ',texto)
        regexp = re.compile(r'[\n\s]Mirá también[^\n]+\n')
        return re.sub(regexp,' ',texto)