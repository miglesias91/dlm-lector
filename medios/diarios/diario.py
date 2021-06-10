import dateutil
import yaml
import feedparser as fp
import newspaper as np
import nltk


from medios.medio import Medio
from medios.diarios.noticia import Noticia

from bd.kioscomongo import Kiosco

class Diario(Medio):

    def __init__(self, etiqueta):
        Medio.__init__(self, etiqueta)
        self.noticias = []
        self.feeds = {}
        self.feed_noticias = ""
        self.secciones = []
        self.configurar()

    def configurar(self):
        with open('medios/diarios/config.yaml', 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        for diario in config['diarios']:
            if diario['tag'] != self.etiqueta:
                continue
            if 'feed_noticias' in diario:
                self.feed_noticias = diario['feed_noticias']
            if 'secciones' in diario:
                self.secciones = diario['secciones']
            if 'feeds' in diario:
                self.secciones = []
                for feed in diario['feeds']:
                    self.feeds[feed['tag']] = feed['url']
                    self.secciones.append(feed['tag'])
                    
    def leer(self):
        kiosco = Kiosco()

        print("leyendo '" + self.etiqueta + "'...")

        for tag, url_feed in self.feeds.items():
            for url_noticia, fecha in self.reconocer_urls_y_fechas_noticias(url_feed=url_feed):
                if kiosco.bd.noticias.find(filter={'diario':self.etiqueta, 'url':url_noticia}).count() > 0: # si existe ya la noticia (url), no la decargo
                    continue
                noticia = self.nueva_noticia(url=url_noticia, seccion=tag, diario=self.etiqueta)
                if noticia == None:
                    continue
                if noticia.fecha == None:
                    noticia.fecha = fecha
                    
                self.noticias.append(noticia)

    def limpiar_texto(self, texto):
        return texto

    def reconocer_urls_y_fechas_noticias(self, url_feed):
        urls_y_fechas = []
        for entrada in fp.parse(url_feed).entries:
            fecha = self.parsear_fecha(entrada)
            urls_y_fechas.append((entrada.link, fecha))
        return urls_y_fechas

    def nueva_noticia(self, url, seccion, diario):
        articulo = np.Article(url=url, language='es')
        try:
            articulo.download()
            articulo.parse()
        except:
            return None

        return Noticia(fecha=articulo.publish_date, url=url, diario=diario, seccion=seccion, titulo=articulo.title, texto=self.limpiar_texto(articulo.text))

    def parsear_fecha(self, entrada):
        return dateutil.parser.parse(entrada.published)