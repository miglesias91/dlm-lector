import unittest

import newspaper as np

from medios.diarios.perfil import Perfil

class TestPerfil(unittest.TestCase):

    def test_entradas_feed(self):
        p = Perfil()
        urls_fechas_titulos = p.entradas_feed("https://www.perfil.com/rss/politica")
        return len(urls_fechas_titulos) == 100

    def test_parsear_noticia(self):
        p = Perfil()
        texto = p.parsear_noticia(url="http://www.perfil.com/noticias/politica/jorde-landau-cuestiona-escrutinio-dijo-gobierno-nos-lleva-patadas-al-11-agosto-elecciones2019-paso.phtml")
        texto = p.parsear_noticia(url="https://radio.perfil.com/videos/juan-pablo-bellavilla-sobre-el-alimentazo-en-plaza-de-mayo-esta-lleno-de-gente-y-eso-demuestra-la-crisis.phtml")
        return 1