import unittest
from urllib.request import Request, urlopen

import newspaper as np

from medios.diarios.paginadoce import PaginaDoce

class TestPaginaDoce(unittest.TestCase):

    def test_entradas_feed(self):
        p12 = PaginaDoce()
        url_fecha_titulo_categoria = p12.entradas_feed()
        return len(url_fecha_titulo_categoria) == 1000

    def test_parsear_noticia(self):
        p12 = PaginaDoce()
        categoria, titulo, texto = p12.parsear_noticia(url="https://www.pagina12.com.ar/207920-ricky-martin-al-frente-de-las-manifestaciones-en-puerto-rico")
        return 1

    def test_parsear_categoria(self):
        p12 = PaginaDoce()
        headers = {'User-Agent': 'Mozilla/5.0'}
        req1 = Request("https://www.pagina12.com.ar/203751-la-autogestion-tiene-mas-tela-para-cortar", headers=headers)
        req2 = Request("https://www.pagina12.com.ar/209532-genocidas", headers=headers)
        req3 = Request("https://www.pagina12.com.ar/209487-dime-de-que-hablas-pajarita", headers=headers)

        c1 = p12.parsear_categoria(html=urlopen(req1).read())
        c2 = p12.parsear_categoria(html=urlopen(req2).read())
        c3 = p12.parsear_categoria(html=urlopen(req3).read())
        return c1 == "el pais" and c2 == "rosario12" and c3 == "las12"