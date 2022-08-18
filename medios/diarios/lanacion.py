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

class LaNacion(Diario):

    def __init__(self):
        Diario.__init__(self, "lanacion")
                    
    def leer(self):
        kiosco = Kiosco()
        
        entradas = self.entradas_feed()[0:30]

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
        feed = bs(urlopen(req).read(), 'html.parser')
        for entrada in feed.find_all('article', ["mod-article"])[:30]:
            url = 'https://www.lanacion.com.ar' + entrada.contents[2].contents[0].contents[0].attrs['href']
            
            horas = int(entrada.contents[0].contents[0][:2])
            minutos = int(entrada.contents[0].contents[0][3:])
            fecha = (datetime.datetime.now() + datetime.timedelta(hours = 1)).replace(hour = horas, minute = minutos, second = 0)
        
            titulo = entrada.contents[2].contents[0].text
            seccion = str(url.split('/')[3])

            if seccion == "el-mundo":
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
        texto = texto.replace('SEGUIR', '')
        regexp = re.compile(r'[\n\s]Crédito[^\n]+\n')
        texto = re.sub(regexp,' ',texto)
        regexp = re.compile(r'[\n\s]Comentar[^\n]+\n')
        texto = re.sub(regexp,' ',texto)
        regexp = re.compile(r'[\n\s]Fuente[^\n]+\n')
        texto = re.sub(regexp,' ',texto)
        regexp = re.compile(r'Crédito[^\n]+\n')
        return re.sub(regexp,' ',texto)