import unittest
import datetime
import json

from medios.diarios.noticia import Noticia

from medios.diarios.infobae import Infobae

from procesamiento.frecuenciasgcp import Frecuencias

class TestFrecuenciasGCP(unittest.TestCase):

    def test_frecuencias(self):
        medio = Infobae()

        medio.leer()

        frecuencias = Frecuencias(medio.noticias)
        frecuencias.calcular()
        frecuencias.resultados

    def test_calcular(self):

        with open('noticias.json') as j:
            noticias = json.load(j)

        notis = [Noticia(texto = n['texto'], fecha=datetime.datetime.now(), url='', diario='', categoria='', titulo=n['titulo']) for n in noticias['noticias']][:5]
        
        f = Frecuencias(notis)
        f.calcular()
        f.resultados
