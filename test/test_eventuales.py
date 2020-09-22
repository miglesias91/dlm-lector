import unittest

import datetime

from medios.diarios.infobae import Infobae

#from bd.kiosco import Kiosco
import bd.eventuales

class TestEventuales(unittest.TestCase):

    def test_subir_resultados_editoriales(self):
        bd.eventuales.resultados_editoriales()
