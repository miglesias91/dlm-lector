import unittest
import datetime
import json

from medios.diarios.noticia import Noticia

from medios.diarios.infobae import Infobae

from procesamiento.frecuenciasstanford import Frecuencias

class TestFrecuenciasStanford(unittest.TestCase):

    def test_frecuencias(self):
        medio = Infobae()

        medio.leer()

        frecuencias = Frecuencias(medio.noticias)
        frecuencias.calcular()
        frecuencias.resultados

    def test_calcular(self):

        with open('noticias.json') as j:
            noticias = json.load(j)

        notis = [Noticia(texto = n['texto'], fecha=datetime.datetime.now(), url='', diario='', seccion='', titulo=n['titulo']) for n in noticias['noticias']][:5]
        
        f = Frecuencias(notis)
        f.calcular()
        print(f.resultados)

    def test_calcular_solo_sustantivos_sin_lemma(self):

        with open('noticias.json') as j:
            noticias = json.load(j)

        notis = [Noticia(texto = n['texto'], fecha=datetime.datetime.now(), url='', diario='', seccion='', titulo=n['titulo']) for n in noticias['noticias']][:5]
        
        # f = Frecuencias(notis, config = {'leer':['sustantivos'], 'lemma':['']})
        f = Frecuencias(notis)
        f.calcular()
        print(f.resultados)

    def test_contar_anotaciones(self):

        with open('/home/manu/anotado.json') as j:
            anotado = json.load(j)
        
        titulo_anotado = anotado['sentences'][0]
        texto_anotado = {'entitymentions':[], 'tokens':[]}

        for oracion in anotado['sentences'][1:]:
            texto_anotado['entitymentions'].extend(oracion['entitymentions'])
            texto_anotado['tokens'].extend(oracion['tokens'])


        # volver a correr y ver resultados, al aprecer todo ok
        f = Frecuencias([])
        freqs_titulo = f.contar_anotaciones(titulo_anotado)
        freqs_texto = f.contar_anotaciones(texto_anotado)
        print('fin')

    def test_dummy(self):
        print('OKARDO')

# if __name__ == '__main__':
#     unittest.main()
