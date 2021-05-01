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

        entradas = self.entradas_feed()[0:40]

        print("leyendo " + str(len(entradas)) + " noticias de '" + self.etiqueta + "'...")

        i = 0
        for url, fecha in entradas:

            i += 1

            # if url in urls_existentes:
            if kiosco.contar_noticias(diario=self.etiqueta, url=url):
                print("noticia " + str(i) + "/" + str(len(entradas)) +" ya descargada")
                continue

            print("descargando noticia " + str(i) + "/" + str(len(entradas)))
            categoria, titulo, texto = self.parsear_noticia(url=url)
            if texto == None:
                continue

            if categoria not in self.categorias:
                continue
                
            self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, categoria=categoria, titulo=titulo, texto=self.limpiar_texto(texto)))

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
        # categoria = articulo.meta_keywords[0].translate(str.maketrans('áéíóúý', 'aeiouy', signos)).strip().lower()
        categoria = self.parsear_categoria(articulo.html)

        if categoria == "el pais":
            categoria = "politica"

        if categoria == "el mundo":
            categoria = "internacional"

        if categoria == "cultura y espectaculos":
            categoria = "espectaculos"            

        return  str(categoria), str(articulo.title), str(articulo.text)

    def parsear_categoria(self, html):
        feed = bs(html, 'lxml')
        categoria = feed.find(lambda tag: tag.name == 'h5' and tag.get('class') == ['current-tag']).text # aca es la joda
        signos = string.punctuation + "¡¿\n"
        return categoria.translate(str.maketrans('áéíóúý', 'aeiouy', signos)).strip().lower()

    def limpiar_texto(self, texto):
        regexp = re.compile(r'Loading tweet ...')
        texto = re.sub(regexp,' ',texto)
        return texto