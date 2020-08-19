import unittest

import newspaper as np

from medios.diarios.ambito import Ambito

class TestAmbito(unittest.TestCase):

    def test_entradas_feed(self):
        a = Ambito()
        urls_fechas_titulos = a.entradas_feed("https://www.ambito.com/rss/politica.xml")
        return len(urls_fechas_titulos) == 20

    def test_parsear_noticia(self):
        a = Ambito()
        texto = a.parsear_noticia(url="https://www.ambito.com/macri-tenemos-que-avanzar-la-segunda-etapa-y-proyectar-20-anos-desarrollo-n5044562")
        texto = a.parsear_noticia(url="https://www.ambito.com/julio-chavez-le-respondio-moyano-la-demanda-el-tigre-veron-n5044558")
        return 1