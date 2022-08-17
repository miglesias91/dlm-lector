import dateutil
import datetime
import yaml
import feedparser as fp
import newspaper as np
import re
import string

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs

from medios.medio import Medio
from medios.diarios.noticia import Noticia
from medios.diarios.diario import Diario

#from bd.kiosco import Kiosco
from bd.kioscomongo import Kiosco

class PaginaDoce(Diario):

    def __init__(self):
        Diario.__init__(self, "paginadoce")
                    
    def leer(self):
        kiosco = Kiosco()

        entradas = self.entradas_feed()[0:30]

        print("leyendo " + str(len(entradas)) + " noticias de '" + self.etiqueta + "'...")

        i = 0
        for url, fecha in entradas:

            i += 1

            # if url in urls_existentes:
            if kiosco.contar_noticias(diario=self.etiqueta, url=url):
                print("noticia " + str(i) + "/" + str(len(entradas)) +" ya descargada")
                continue

            print("descargando noticia " + str(i) + "/" + str(len(entradas)))
            seccion, titulo, texto = self.parsear_noticia(url=url)
            if texto == None:
                continue

            if seccion not in self.secciones:
                continue
                
            self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, seccion=seccion, titulo=titulo, texto=self.limpiar_texto(texto)))

    def entradas_feed(self):
        urls_fechas = []
        req = Request(self.feed_noticias, headers={'User-Agent': 'Mozilla/5.0'})
        feed = bs(urlopen(req).read(), 'html.parser')
        for entrada in feed.find_all('url'):
            url = str(entrada.loc.string)
            fecha = dateutil.parser.parse(entrada.find('news:publication_date').string, ignoretz=True)
            urls_fechas.append((url, fecha))
            
        urls_fechas.sort(key=lambda e: e[1], reverse=True)

        return urls_fechas

    def parsear_noticia(self, url):
        articulo = np.Article(url=url, language='es')
        try:
            articulo.download()
            articulo.parse()
        except:
            return None
        
        signos = string.punctuation + "¡¿\n"
        # seccion = articulo.meta_keywords[0].translate(str.maketrans('áéíóúý', 'aeiouy', signos)).strip().lower()
        seccion = self.parsear_seccion(articulo.html)

        if seccion == "el pais":
            seccion = "politica"

        if seccion == "el mundo":
            seccion = "internacional"

        if seccion == "cultura y espectaculos":
            seccion = "espectaculos"            

        return  str(seccion), str(articulo.title), str(articulo.text)

    def parsear_seccion(self, html):
        feed = bs(html, 'lxml')
        seccion = feed.find(lambda tag: tag.name == 'h5' and tag.get('class') == ['current-tag']).text
        signos = string.punctuation + "¡¿\n"
        return seccion.translate(str.maketrans('áéíóúý', 'aeiouy', signos)).strip().lower()

    def limpiar_texto(self, texto):
        regexp = re.compile(r'Loading tweet ...')
        texto = re.sub(regexp,' ',texto)
        return texto