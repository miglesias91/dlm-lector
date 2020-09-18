import unittest

import datetime

from medios.diarios.infobae import Infobae

#from bd.kiosco import Kiosco
from bd.kioscomongo import Kiosco

class TestKiosco(unittest.TestCase):

    def test_actualizar_diario(self):
        k = Kiosco()

        i = Infobae()
        #i.etiqueta = 'test_todos'
        i.leer()

        k.actualizar_diario(i)

    def test_contar_noticias(self):
        k = Kiosco()

        notis = k.noticias(diario='clarin')

        #fecha = datetime.datetime(year = 2020, month = 8, day = 25)
        fecha = {'desde' : datetime.datetime(year = 2020, month = 8, day = 22), 'hasta' : datetime.datetime(year = 2020, month = 8, day = 24)}
        categoria = ['economia', 'internacional']
        conteo = k.contar_noticias(fecha = fecha, diario = 'test_todos', categorias = categoria)
        conteo

    def test_urls(self):
        k = Kiosco()

        fecha = datetime.datetime(year = 2020, month = 8, day = 26)
        #fecha = {'desde' : datetime.datetime(year = 2020, month = 8, day = 22), 'hasta' : datetime.datetime(year = 2020, month = 8, day = 24)}
        #categoria = ['economia', 'internacional']
        urls = k.urls(diario = 'clarin')
        urls

    def test_subir_historicos(self):
        k = Kiosco()

        k.subir_historicos('/home/manu/Documentos/discursos_historico.json')
