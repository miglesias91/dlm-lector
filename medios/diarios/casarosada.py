import dateutil
import datetime
import yaml
import feedparser as fp
import newspaper as np
import re

import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs

from medios.medio import Medio
from medios.diarios.noticia import Noticia
from medios.diarios.diario import Diario

from bd.entidades import Kiosco

class CasaRosada(Diario):

    def __init__(self):
        Diario.__init__(self, "casarosada")

    def leer_historico(self):
        entradas = self.parsear_entradas()
        urls_discursos = self.parsear_urls_discursos(entradas)
        discursos = self.parsear_discursos(urls_discursos)

        for titulo, fecha, texto, url in discursos:
            self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, categoria='todo', titulo=titulo, texto=self.limpiar_texto(texto)))


    def leer_todo(self):
        kiosco = Kiosco()

        print("leyendo '" + self.etiqueta + "'...")

        tag_regexp = re.compile(r'<[^>]+>')

        entradas = []
        url_feed_template = self.feeds['todo'] + "&start="
        index = 0
        feed = fp.parse(url_feed_template + str(index))
        while len(feed.entries) > 0:
            entradas.extend(feed.entries)
            index += 40
            feed = fp.parse(url_feed_template + str(index))

        for entrada in entradas:
            titulo = entrada.title
            texto = bs(re.sub(tag_regexp,' ',entrada.summary), features="lxml").text
                
            fecha = dateutil.parser.parse(entrada.published)
            url = entrada.link
            if kiosco.bd.noticias.find(filter={'diario':self.etiqueta, 'url':url}).count() > 0: # si existe ya la noticia (url), no la decargo
                continue
            self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, categoria='todo', titulo=titulo, texto=self.limpiar_texto(texto)))


    def leer(self, fecha, categorias):
        kiosco = Kiosco()

        print("leyendo '" + self.etiqueta + "'...")

        tag_regexp = re.compile(r'<[^>]+>')

        for tag, url_feed in self.feeds.items():
            feed = fp.parse(url_feed)
            for entrada in feed.entries:
                titulo = entrada.title
                texto = bs(re.sub(tag_regexp,' ',entrada.summary), features="lxml").text

                fecha = dateutil.parser.parse(entrada.published)
                url = entrada.link
                if kiosco.bd.noticias.find(filter={'diario':self.etiqueta, 'url':url}).count() > 0: # si existe ya la noticia (url), no la decargo
                    continue
                self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, categoria=tag, titulo=titulo, texto=self.limpiar_texto(texto)))

    def limpiar_texto(self, texto):
        primer_linea_regexp = re.compile(r'^[^\n]+\n')
        texto_limpio = re.sub(primer_linea_regexp,' ',texto)
        if len(texto_limpio) == 0:
            texto_limpio = texto
        return texto_limpio


    def parsear_entradas(self):
        with open('medios/diarios/config.yaml', 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        url_historica = ""
        for diario in config['diarios']:
            if diario['tag'] == self.etiqueta:
                url_historica = diario['feed_historico']
                break

        entradas = []
        url_historica = url_historica + "&start="
        index = 0
        feed = fp.parse(url_historica + str(index))
        intentos = 0
        while feed.bozo == 1 and intentos < 5:
            feed = fp.parse(url_historica + str(index))
            intentos += 1

        while len(feed.entries) > 0:
            entradas.extend(feed.entries)
            print("entradas: " + str(len(entradas)))
            index += 40
            feed = fp.parse(url_historica + str(index))
            intentos = 0
            while feed.bozo == 1 and intentos < 5:
                feed = fp.parse(url_historica + str(index))
                intentos += 1

        return [(dateutil.parser.parse(e.published), e.link) for e in entradas]

    def parsear_urls_discursos(self, entradas):

        urls_discursos = []
        fecha_asuncion_cfk =  dateutil.parser.parse("Mon, 10 Dec 2007 18:36:41 +0000")
        for fecha, url in entradas:
            if fecha > fecha_asuncion_cfk:
                # index 7557
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                
                leyo_ok = False
                html_posteo = None
                i = 0
                while leyo_ok == False and i < 5:
                    try:
                        html_posteo = bs(urlopen(req).read(), 'html.parser')
                        leyo_ok = True
                    except:
                        i += 1
                        leyo_ok = False
                
                e_link = None
                if html_posteo:
                    e_link = html_posteo.find(lambda tag: tag.name == 'a' and tag.get('class') == ['discurso', 'btn', 'btn-primary'])
                if e_link and 'href' in e_link.attrs:
                    url_discurso = 'https://www.casarosada.gob.ar' + e_link.attrs['href']
                    urls_discursos.append((fecha, url_discurso))
            else:
                urls_discursos.append((fecha, url))

        return urls_discursos

    def parsear_discursos(self, urls_discursos):
        discursos = []
        for fecha, url in urls_discursos:            
            leyo_ok = False
            html_posteo = None
            i = 0
            articulo = None
            while leyo_ok == False and i < 5:
                articulo = np.Article(url=url, language='es')
                try:
                    articulo.download()
                    articulo.parse()
                    leyo_ok = True
                except:
                    i += 1
                    leyo_ok = False

            texto = articulo.text

            discursos.append((articulo.title, fecha, articulo.text, url))
        return discursos