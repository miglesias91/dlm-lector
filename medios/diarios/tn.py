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

class TN(Diario):

    def __init__(self):
        Diario.__init__(self, "todonoticias")
        
    def leer(self):
        kiosco = Kiosco()

        print("leyendo '" + self.etiqueta + "'...")

        tag_regexp = re.compile(r'<[^>]+>')

        urls_existentes = kiosco.urls(diario = self.etiqueta)
        entradas = fp.parse(self.feed_noticias).entries[0:70]

        print("leyendo " + str(len(entradas)) + " noticias de '" + self.etiqueta + "'...")

        i = 0
        for entrada in entradas:
            i += 1

            url = str(entrada.link)
            
            if url in urls_existentes:
                print("noticia " + str(i) + "/" + str(len(entradas)) +" ya descargada")
                continue

            print("parseando noticia " + str(i) + "/" + str(len(entradas)))
            titulo = str(entrada.title)
            texto = str(re.sub(tag_regexp,' ',entrada.content[0].value))
            fecha = dateutil.parser.parse(entrada.published)  - datetime.timedelta(hours=3)

            categoria = str(url.split('/')[3])

            if categoria == "show":
                categoria = "espectaculos"

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


    # def leer(self):
    #     kiosco = Kiosco()

    #     urls_existentes = kiosco.urls(diario = self.etiqueta)

    #     entradas = self.entradas_feed()[0:100]

    #     print("leyendo " + str(len(entradas)) + " noticias de '" + self.etiqueta + "'...")

    #     i = 0
    #     for url, fecha, titulo, categoria in entradas:

    #         i += 1

    #         if url in urls_existentes:
    #             print("noticia " + str(i) + "/" + str(len(entradas)) +" ya descargada")
    #             continue

    #         print("descargando noticia " + str(i) + "/" + str(len(entradas)))
    #         texto = self.parsear_noticia(url=url)
    #         if texto == None:
    #             continue
    #         self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, categoria=categoria, titulo=titulo, texto=texto))

    # def entradas_feed(self):
    #     urls_fechas_titulo_categoria = []
    #     req = Request(self.feed_noticias, headers={'User-Agent': 'Mozilla/5.0'})
    #     feed = bs(urlopen(req).read(), 'html.parser')
    #     for entrada in feed.find_all('url'):
    #         url = str(entrada.loc.string)
    #         fecha = dateutil.parser.parse(entrada.find('news:publication_date').string) - datetime.timedelta(hours=3)
    #         titulo = str(entrada.find('news:title').string)

    #         categoria = str(url.split('/')[3])
    #         if categoria == "show":
    #             categoria = "espectaculos"

    #         if categoria not in self.categorias:
    #             continue

    #         urls_fechas_titulo_categoria.append((url, fecha, titulo, categoria))
            
    #     return urls_fechas_titulo_categoria

    # def parsear_noticia(self, url):
    #     articulo = np.Article(url=url, language='es')
    #     try:
    #         articulo.download()
    #         articulo.parse()
    #     except:
    #         return None

    #     return self.limpiar_texto(articulo.text)

    # def limpiar_texto(self, texto):
    #     texto = texto.replace('\n\n', ' ')
    #     return texto