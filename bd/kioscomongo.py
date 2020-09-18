import datetime
import dateutil
import logging
import json

import yaml

import pymongo
from pymongo import MongoClient

from medios.diarios.noticia import Noticia

from bd.resultados import Resultados
from procesamiento.frecuenciasspacy import Frecuencias

class Kiosco:
    def __init__(self, fecha=None):
        with open('conexiones.json') as c:
            j = json.load(c)
            
        usuario = j['kiosco']['usuario']
        pwd = j['kiosco']['pwd']
        server = j['kiosco']['server']

        conexion = "mongodb://" + usuario + ":" + pwd + "@" + server + "/"

        self.bd = MongoClient(conexion).dlm

    def actualizar_diario(self, diario):
        # ver si hay q restarle 3 o 6 horas. probar en el servidor
        json_noticias = [{'fecha':n.fecha, 'url':n.url, 'diario':n.diario, 'cat':n.categoria,'titulo':n.titulo, 'texto':n.texto} for n in diario.noticias]

        if len(json_noticias) == 0:
        #     print("no hay noticias nuevas de '" + diario.etiqueta + "'")
        #     logging.warning("no hay noticias nuevas de '" + diario.etiqueta + "'")
            print("no hay noticias nuevas de '" + diario.etiqueta + "'")
            return 0

        return self.bd.noticias.insert_many(json_noticias)

    def noticias(self, fecha=None, diario=None, categorias=None, fecha_in=True, url_in=True, diario_in=True, cat_in=True, tit_in=True, text_in=True):
        query = {}

        if fecha:
            if type(fecha) is dict:
                desde = datetime.datetime(fecha['desde'].year, fecha['desde'].month, fecha['desde'].day, 0,0,0)
                hasta = datetime.datetime(fecha['hasta'].year, fecha['hasta'].month, fecha['hasta'].day, 23,59,59)                
            else:
                desde = datetime.datetime(fecha.year, fecha.month, fecha.day, 0,0,0)
                hasta = datetime.datetime(fecha.year, fecha.month, fecha.day, 23,59,59)
            query['fecha']={"$gte":desde, "$lte":hasta}

        if diario:
            query['diario']=diario

        if categorias:
            if len(categorias) > 0:
                query['cat']={"$in":categorias}

        projection = {'fecha':fecha_in, 'url':url_in, 'diario':diario_in, 'cat':cat_in, 'titulo':tit_in, 'texto':text_in }

        cursor = self.bd.noticias.find(query, projection)

        return [Noticia(fecha=n['fecha'], url=n['url'], diario=n['diario'], categoria=n['cat'], titulo=n['titulo'], texto=n['texto']) for n in cursor]

    def contar_noticias(self, fecha=None, diario=None, categorias=None, url=None):
        query = {}

        if fecha:
            if type(fecha) is dict:
                desde = datetime.datetime(fecha['desde'].year, fecha['desde'].month, fecha['desde'].day, 0,0,0)
                hasta = datetime.datetime(fecha['hasta'].year, fecha['hasta'].month, fecha['hasta'].day, 23,59,59)                
            else:
                desde = datetime.datetime(fecha.year, fecha.month, fecha.day, 0,0,0)
                hasta = datetime.datetime(fecha.year, fecha.month, fecha.day, 23,59,59)
            query['fecha']={"$gte":desde, "$lte":hasta}

        if diario:
            query['diario']=diario

        if categorias:
            if type(categorias) is list and len(categorias) > 0:
                query['cat']={"$in":categorias}
            else:
                query['cat']={"$in":[categorias]}

        if url:
            query['url']=url

        return self.bd.noticias.count_documents(query)

    def categorias_existentes(self, fecha=None, diario=None, url=None):
        query = {}

        if fecha:
            if type(fecha) is dict:
                desde = datetime.datetime(fecha['desde'].year, fecha['desde'].month, fecha['desde'].day, 0,0,0)
                hasta = datetime.datetime(fecha['hasta'].year, fecha['hasta'].month, fecha['hasta'].day, 23,59,59)                
            else:
                desde = datetime.datetime(fecha.year, fecha.month, fecha.day, 0,0,0)
                hasta = datetime.datetime(fecha.year, fecha.month, fecha.day, 23,59,59)
            query['fecha']={"$gte":desde, "$lte":hasta}

        if diario:
            query['diario']=diario

        if url:
            query['url']=url

        return self.bd.noticias.distinct("cat", query)
    
    def urls_recientes(self, fecha=None, diario=None, categoria=None, limite = 100):
        query = {}

        if fecha:
            if type(fecha) is dict:
                desde = datetime.datetime(fecha['desde'].year, fecha['desde'].month, fecha['desde'].day, 0,0,0)
                hasta = datetime.datetime(fecha['hasta'].year, fecha['hasta'].month, fecha['hasta'].day, 23,59,59)                
            else:
                desde = datetime.datetime(fecha.year, fecha.month, fecha.day, 0,0,0)
                hasta = datetime.datetime(fecha.year, fecha.month, fecha.day, 23,59,59)
            query['fecha']={"$gte":desde, "$lte":hasta}

        if diario:
            query['diario']=diario

        if categoria:
            query['cat']=categoria

        projection = {'url':True}

        #h = self.bd.noticias.find(query, projection).sort('fecha', pymongo.DESCENDING).limit(limite)
        return [u['url'] for u in self.bd.noticias.find(query, projection).sort('fecha', pymongo.DESCENDING).limit(limite)]

    # metodo usado una sola vez para subir discursos historicos
    def subir_historicos(self, path_discursos_historicos):
        buffer_kiosco = []
        buffer_resultado = []

        resultados = Resultados()
        freqs = Frecuencias()
        total = 0
        agregados = 0
        with open(path_discursos_historicos) as f:
            for linea in f:
                total += 1
                jdiscurso = json.loads(linea)

                texto = jdiscurso['texto']

                if not texto:
                    continue

                diario = jdiscurso['diario']
                url = jdiscurso['url']
                titulo = jdiscurso['titulo']

                fecha = datetime.datetime.strptime(jdiscurso['fecha']['$date'], '%Y-%m-%dT%H:%M:%SZ')

                # if fecha.strftime('%Y%m%d%H%M%S') > '20071206233745':
                #     continue

                sfecha = fecha.strftime('%Y%m%d')
                categoria = ""
                if sfecha >= "20191210":
                    categoria = "alberto"

                if sfecha < "20191210" and sfecha >= "20151210":
                    categoria = "macri"

                if sfecha < "20151210" and sfecha >= "20071210":
                    categoria = "cristina"

                if sfecha < "20071210":
                    categoria = "nestor"

                # if self.contar_noticias(diario=diario, categorias=categoria, url=url):
                #     continue
                if categoria != "nestor":
                    continue

                if resultados.bd.frecuencias.find_one({'diario': diario, 'categoria': categoria, 'fecha': fecha.strftime('%Y%m%d%H%M%S'), 'url':url}):
                    continue

                while resultados.bd.frecuencias.find_one({'diario': diario, 'categoria': categoria, 'fecha': fecha.strftime('%Y%m%d%H%M%S')}):
                    fecha += datetime.timedelta(seconds=10)

                while self.existe_fecha(fecha, buffer_resultado):
                    fecha += datetime.timedelta(seconds=10)

                # buffer_kiosco.append({'diario': diario, 'cat':categoria, 'fecha': fecha, 'url':url, 'titulo':titulo, 'texto':texto})

                # if len(buffer_kiosco) >= 100:
                #     self.bd.noticias.insert_many(buffer_kiosco)
                #     agregados += 100
                #     buffer_kiosco = []
                #     print('total procesados: ' + str(total) + '. agregados ' + str(agregados) + ' en total en Kiosco')

                f_ter_tit, f_ver_tit, f_per_tit, f_ter_txt, f_ver_txt, f_per_txt = freqs.tituloytexto2freqs(titulo,texto)

                buffer_resultado.append({'diario':diario, 'categoria': categoria, 'fecha': fecha.strftime('%Y%m%d%H%M%S'), 'url':url, 'f_ter_tit': f_ter_tit, 'f_ver_tit': f_ver_tit, 'f_per_tit': f_per_tit, 'f_ter_txt': f_ter_txt, 'f_ver_txt': f_ver_txt, 'f_per_txt': f_per_txt})

                if len(buffer_resultado) >= 100:
                    resultados.bd.frecuencias.insert_many(buffer_resultado)
                    agregados += 100
                    buffer_resultado = []
                    print('total procesados: ' + str(total) + '. agregados ' + str(agregados) + ' en total en Resultados')

        if len(buffer_resultado):
            self.bd.noticias.insert_many(buffer_resultado)
            print('total procesados: ' + str(total) + '. agregados ' + str(agregados+len(buffer_kiosco)) + ' en total en Resultados')

        print('fin')

    def existe_fecha(self, fecha, buffer_resultado):
        sfecha = fecha.strftime('%Y%m%d%H%M%S')
        for r in buffer_resultado:
            if sfecha == r['fecha']:
                return True
        return False

