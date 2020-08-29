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

from bd.kiosco import Kiosco

class Clarin(Diario):

    def __init__(self):
        Diario.__init__(self, "clarin")
                    
    def leer(self):
        kiosco = Kiosco()

        urls_existentes = kiosco.urls_recientes(fecha= (datetime.date.today() - datetime.timedelta(hours=3)) , diario = self.etiqueta, limite = 70)

        entradas = self.entradas_feed()[0:70]

        print("leyendo " + str(len(entradas)) + " noticias de '" + self.etiqueta + "'...")

        i = 0
        for url, fecha, titulo, categoria in entradas:
            
            i += 1

            if url in urls_existentes:
                print("noticia " + str(i) + "/" + str(len(entradas)) +" ya descargada")
                continue

            print("descargando noticia " + str(i) + "/" + str(len(entradas)))
            texto = self.parsear_noticia(url=url)
            if texto == None:
                continue
            self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, categoria=categoria, titulo=titulo, texto=texto))

    def entradas_feed(self):
        urls_fechas_titulo_categoria = []
        req = Request(self.feed_noticias, headers={'User-Agent': 'Mozilla/5.0'})
        feed = bs(urlopen(req).read(), 'html.parser')
        for entrada in feed.find_all('url'):
             # creo objetos str xq sino mas adelante tira RecursionError.            
            url = str(entrada.loc.string)
            fecha = dateutil.parser.parse(entrada.find('news:publication_date').string)            
            titulo = str(entrada.find('news:title').string)
            categoria = str(url.split('/')[3])

            if categoria == "mundo":
                categoria = "internacional"

            if categoria not in self.categorias:
                continue

            urls_fechas_titulo_categoria.append((url, fecha, titulo, categoria))
            
        return urls_fechas_titulo_categoria

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