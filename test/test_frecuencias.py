import unittest

import json

from medios.diarios.infobae import Infobae

from procesamiento.frecuencias import Frecuencias

class TestFrecuencias(unittest.TestCase):

    def test_frecuencias(self):
        medio = Infobae()

        medio.leer()

        frecuencias = Frecuencias(medio.noticias)
        frecuencias.calcular()
        frecuencias.resultados

    def test_noticias2freqs(self):
        p = Procesador()

        with open('noticias.json') as j:
            noticias = json.load(j)

        notis = [Noticia(texto = n['texto'], fecha='', url='', diario='', categoria='', titulo=n['titulo']) for n in noticias['noticias']]
        
        fq = p.__noticias2freqs__(notis)

    def test_levantar_freqs_vacios(self):
        p = Procesador()

        f1, f2, f3, f4, f5, f6 = p.__levantar_freqs__('freqs/noexiste.json')
        f1

    def test_levantar_freqs(self):
        p = Procesador()

        f1, f2, f3, f4, f5, f6  = p.__levantar_freqs__('freqs/test_levantar_freqs.json')
        f1

    def test_serializar_freqs(self):
        p = Procesador()
        
        p.__serializar_freqs__('freqs/test_serializar_freqs.json', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6')
        p.__serializar_freqs__('freqs/test_serializar_freqs.json', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12')