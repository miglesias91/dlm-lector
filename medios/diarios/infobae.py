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

class Infobae(Diario):

    def __init__(self):
        Diario.__init__(self, "infobae")

    def leer(self):
        kiosco = Kiosco()

        tag_regexp = re.compile(r'<[^>]+>')

        # recupero las urls del dia de hoy, con la diferencia horario del servidor.
        # si no hay de hoy, me trae de ayer.
        entradas = fp.parse(self.feed_noticias).entries[0:50]

        print("leyendo " + str(len(entradas)) + " noticias de '" + self.etiqueta + "'...")

        i = 0
        for entrada in entradas:
            i += 1

            url = str(entrada.link)
            
            seccion = ''
            try:
                seccion = str(url.split('/')[3])
            except:
                continue

            if seccion == "america":
                seccion = "internacional"

            if seccion == "teleshow":
                seccion = "espectaculos"

            if seccion == "deportes-2":
                seccion = "deportes"

            #if url in urls_existentes:
            if kiosco.contar_noticias(diario=self.etiqueta, secciones=seccion, url=url):
                print("noticia " + str(i) + "/" + str(len(entradas)) +" ya descargada")
                continue

            print("parseando noticia " + str(i) + "/" + str(len(entradas)))
            titulo = str(entrada.title)
            texto = str(re.sub(tag_regexp,' ',entrada.content[0].value))
            fecha = dateutil.parser.parse(entrada.published, ignoretz=True) - datetime.timedelta(hours=3)

            if seccion not in self.secciones:
                continue

            self.noticias.append(Noticia(fecha=fecha, url=url, diario=self.etiqueta, seccion=seccion, titulo=titulo, texto=self.limpiar_texto(texto)))

        print(self.etiqueta + " leyo " + str(len(self.noticias)))

    def limpiar_texto(self, texto):
        regexp = re.compile(r'SEGUÍ LEYENDO[^$]+')
        texto = re.sub(regexp,' ',texto)
        regexp = re.compile(r'MÁS SOBRE ESTE TEMA[^$]+')
        texto = re.sub(regexp,' ',texto)
        regexp = re.compile(r'Seguí leyendo[^$]+')
        texto = re.sub(regexp,' ',texto)
        return texto