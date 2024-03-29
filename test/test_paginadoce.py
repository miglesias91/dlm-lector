import unittest
from urllib.request import Request, urlopen

import newspaper as np

from medios.diarios.paginadoce import PaginaDoce

class TestPaginaDoce(unittest.TestCase):

    def test_entradas_feed(self):
        p12 = PaginaDoce()
        url_fecha_titulo_seccion = p12.entradas_feed()
        return len(url_fecha_titulo_seccion) == 1000

    def test_parsear_noticia(self):
        p12 = PaginaDoce()
        seccion, titulo, texto = p12.parsear_noticia(url="https://www.pagina12.com.ar/363980-el-concejo-deliberante-solicito-suspender-el-convenio-sobre-")
        return 1

    def test_parsear_seccion(self):
        p12 = PaginaDoce()
        headers = {'User-Agent': 'Mozilla/5.0'}
        req1 = Request("https://www.pagina12.com.ar/203751-la-autogestion-tiene-mas-tela-para-cortar", headers=headers)
        req2 = Request("https://www.pagina12.com.ar/209532-genocidas", headers=headers)
        req3 = Request("https://www.pagina12.com.ar/209487-dime-de-que-hablas-pajarita", headers=headers)

        c1 = p12.parsear_seccion(html=urlopen(req1).read())
        c2 = p12.parsear_seccion(html=urlopen(req2).read())
        c3 = p12.parsear_seccion(html=urlopen(req3).read())
        return c1 == "el pais" and c2 == "rosario12" and c3 == "las12"