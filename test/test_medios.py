import unittest

import newspaper as np

from medios.diarios.diarios import Clarin, ElDestape, Infobae, LaNacion, PaginaDoce, CasaRosada

class TestMedios(unittest.TestCase):

    def test_limpiar_texto_clarin(self):
        articulo = np.Article(url="https://www.clarin.com/politica/jingle-bizarro-nicolas-cano-ritmo-ricky-martin_0_K63KGeNkF.html", language='es')
        articulo.download()
        articulo.parse()

        diario = Clarin()
        t = diario.limpiar_texto(articulo.text)
        return 1
    
    def test_limpiar_texto_lanacion(self):
        articulo = np.Article(url="https://www.lanacion.com.ar/politica/un-legislador-tucumano-quiere-declarar-persona-no-nid2264493", language='es')
        articulo.download()
        articulo.parse()

        diario = LaNacion()
        t = diario.limpiar_texto(articulo.text)
        return 1

    def test_leer_casarosada(self):
        cr = CasaRosada()
        cr.leer()
        
    def test_reconcer_categoria_eldestape(self):
        articulo = np.Article(url="https://www.eldestapeweb.com/nota/copa-america-el-desplante-de-messi-a-la-conmebol-por-el-arbitraje-contra-chile-20197618140", language='es')
        articulo.download()
        articulo.parse()

        diario = ElDestape()
        t = diario.reconocer_categoria(articulo.html)
        return 1

