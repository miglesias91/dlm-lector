import unittest

import yaml

import feedparser as fp
import newspaper as np

from medios.diarios.infobae import Infobae

class TestLaNacion(unittest.TestCase):

    def test_entradas_feed(self):
        i = Infobae()
        i.leer()
        return 1