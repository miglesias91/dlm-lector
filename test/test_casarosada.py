import json
import datetime

import unittest

import newspaper as np

from medios.diarios.casarosada import CasaRosada

class TestCasaRosada(unittest.TestCase):

    def test_parsear_entradas(self):
        cr = CasaRosada()
        entradas = cr.parsear_entradas()
        jsonfile = open("urls_entradas.txt", 'x')
        for fecha, url in entradas:
            jsonfile.write(fecha.strftime("%Y%m%d") + "|" + url + "\n")
        jsonfile.close()
        return 1

    def test_parsear_url_discursos(self):
        cr = CasaRosada()
        # entradas = cr.parsear_entradas()
        jsonfileentradas = open("urls_entradas.txt")
        entradas = []
        for linea in jsonfileentradas.readlines():
            fecha, url = linea.rstrip().split('|')
            entradas.append((datetime.datetime.strptime(fecha, "%Y%m%d"), url))

        urls_discursos = cr.parsear_urls_discursos(entradas)
        jsonfile = open("urls_discursos.txt", 'x')
        for fecha, url in urls_discursos:
            jsonfile.write(fecha.strftime("%Y%m%d") + "|" + url + "\n")
        jsonfile.close()
        return 1

    def test_parsear_discursos(self):
        cr = CasaRosada()
        # entradas = cr.parsear_entradas()
        jsonfilediscursos = open("urls_discursos.txt")
        urls_discursos = []
        for linea in jsonfilediscursos.readlines():
            fecha, url = linea.rstrip().split('|')
            urls_discursos.append((datetime.datetime.strptime(fecha, "%Y%m%d"), url))

        discursos = cr.parsear_discursos(urls_discursos)
        return 1