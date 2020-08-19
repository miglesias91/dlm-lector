import unittest

import yaml

import feedparser as fp
import newspaper as np

from medios.diarios.lanacion import LaNacion

class TestLaNacion(unittest.TestCase):

    def test_entradas_feed(self):
        ln = LaNacion()
        url_fecha_titulo_categoria = ln.entradas_feed()
        return len(url_fecha_titulo_categoria) == 1000

    def test_parsear_noticia(self):
        ln = LaNacion()
        texto = ln.parsear_noticia(url="https://www.lanacion.com.ar/buenos-aires/mas-80-mil-pasajeros-viajan-aerolineas-argentinas-nid2269404")
        return 1