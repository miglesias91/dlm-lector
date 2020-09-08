import unittest

import json

from bd.resultados import Resultados

from medios.diarios.infobae import Infobae

class TestResultados(unittest.TestCase):

    def test_actualizar_freqs(self):

        with open('resultados.json') as r:
            j = json.load(r)

        resultados = Resultados()
        resultados.actualizar_freqs(j)
