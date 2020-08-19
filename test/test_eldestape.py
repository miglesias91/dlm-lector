import unittest

import newspaper as np

from medios.diarios.eldestape import ElDestape

class TestElDestape(unittest.TestCase):

    def test_entradas_feed(self):
        ed = ElDestape()
        url_fecha_titulo_categoria = ed.entradas_feed()
        return len(url_fecha_titulo_categoria) == 50

    def test_parsear_noticia(self):
        ed = ElDestape()
        texto = ed.parsear_noticia(url="https://www.eldestapeweb.com/nota/encuestas-2019-encuesta-muestra-que-la-formula-fernandez-fernandez-se-impone-a-macri-pichetto-en-la-provincia-de-buenos-aires-201972317240")
        return 1