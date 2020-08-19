import unittest

import newspaper as np

from medios.diarios.popular import Popular

class TestPopular(unittest.TestCase):

    def test_tuplas(self):
        popu = Popular()
        tuplas = popu.getTuplas()
        return 1

    def test_parsear_noticia(self):
        popu = Popular()
        titulo, texto = popu.parsearNoticia(url="https://www.diariopopular.com.ar/politica/amplian-el-cierre-fronteras-argentinos-el-exterior-n468166")
        titulo, texto = popu.parsearNoticia(url="https://www.diariopopular.com.ar/espectaculos/fede-bal-compartio-el-primer-dia-su-tratamiento-n467914")
        return 1