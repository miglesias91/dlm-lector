import unittest

import newspaper as np

from medios.diarios.tn import TN

class TestTN(unittest.TestCase):

    def test_entradas_feed(self):
        tn = TN()
        url_fecha_titulo_categoria = tn.entradas_feed()
        return len(url_fecha_titulo_categoria) > 200

    def test_parsear_noticia(self):
        tn = TN()
        texto = tn.parsear_noticia(url="https://tn.com.ar/politica/mauricio-macri-los-productores-de-marcas-como-cuchuflito-estan-muy-orgullosos-de-su-trabajo_980851")
        return 1