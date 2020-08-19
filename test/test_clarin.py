import unittest

import newspaper as np

from medios.diarios.clarin import Clarin

class TestClarin(unittest.TestCase):

    def test_entradas_feed(self):
        c = Clarin()
        url_fecha_titulo_categoria = c.entradas_feed()
        return len(url_fecha_titulo_categoria) == 1000

    def test_parsear_noticia(self):
        c = Clarin()
        texto = c.parsear_noticia(url="https://www.clarin.com/deportes/emotivo-mensaje-sergio-goycochea-carlos-bilardo-delicado-salud_0_ZiDQnKVGD.html")
        return 1