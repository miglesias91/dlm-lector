import unittest

import newspaper as np

from medios.diarios.telam import Telam

class TestTelam(unittest.TestCase):

    def test_entradas_feed(self):
        t = Telam()
        urls_fechas_titulos = t.entradas_feed("https://www.telam.com.ar/rss2/politica.xml")
        return len(urls_fechas_titulos) == 20

    def test_parsear_noticia(self):
        t = Telam()
        texto = t.parsear_noticia(url="https://www.telam.com.ar/notas/201907/378120-biro-dice-que-van-a-seguir-leyendo-comunicados-de-porotesta-en-los-vuelos.html")
        return 1