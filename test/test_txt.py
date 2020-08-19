import codecs
import string

import pathlib
import unittest

import nltk
from nltk.corpus import cess_esp

from ia.txt import NLP
from bd.entidades import Kiosco

class TestTXT(unittest.TestCase):

    def test_armar_ngramas(self):
        nlp = NLP()
        nlp.__entrenar_ngramas__()
        return 1


if __name__ == '__main__':
    unittest.main()