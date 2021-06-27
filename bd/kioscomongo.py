import datetime
import dateutil
import logging
import json

import yaml

import pymongo
from pymongo import MongoClient
from pymongo.errors import OperationFailure, BulkWriteError

from medios.diarios.noticia import Noticia

class Kiosco:
    def __init__(self, conexiones=None):

        if conexiones is None:
            conexiones = 'conexiones-oracle.json'

        with open(conexiones) as c:
            j = json.load(c)
            
        usuario = j['kiosco']['usuario']
        pwd = j['kiosco']['pwd']
        server = j['kiosco']['server']

        conexion = "mongodb://" + usuario + ":" + pwd + "@" + server + "/"

        self.bd = MongoClient(conexion).dlm

    def actualizar_diario(self, diario):
        # ver si hay q restarle 3 o 6 horas. probar en el servidor

        # hago doble pasada para detectar duplicados
        urls_dups = []
        urls = []
        for n in diario.noticias:
            url = n.url
            if url in urls:
                urls_dups.append(url)
            else:
                urls.append(url)

        json_noticias = [{'fecha':n.fecha, 'url':n.url, 'diario':n.diario, 'seccion':n.seccion,'titulo':n.titulo, 'texto':n.texto} for n in diario.noticias if n.url not in urls_dups]

        if len(json_noticias) == 0:
        #     print("no hay noticias nuevas de '" + diario.etiqueta + "'")
        #     logging.warning("no hay noticias nuevas de '" + diario.etiqueta + "'")
            print("no hay noticias nuevas de '" + diario.etiqueta + "'")
            return 0
        
        try:
            return self.bd.noticias.insert_many(json_noticias)
        except BulkWriteError as bwe:
            errores_que_no_son_de_duplicados = filter(lambda x: x['code'] != 11000, bwe.details['writeErrors'])
            if len(errores_que_no_son_de_duplicados) > 0:
                raise Exception(bwe.details)


    def noticias(self, fecha=None, diario=None, secciones=None, fecha_in=True, url_in=True, diario_in=True, seccion_in=True, tit_in=True, text_in=True):
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

        if secciones:
            if type(secciones) is list:
                query['seccion']={"$in":secciones}
            else:
                query['seccion']={"$in":[secciones]}

        projection = {'fecha':fecha_in, 'url':url_in, 'diario':diario_in, 'seccion':seccion_in, 'titulo':tit_in, 'texto':text_in }

        cursor = self.bd.noticias.find(query, projection)

        return [Noticia(fecha=n['fecha'], url=n['url'], diario=n['diario'], seccion=n['seccion'], titulo=n['titulo'], texto=n['texto']) for n in cursor]

    def contar_noticias(self, fecha=None, diario=None, secciones=None, url=None):
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

        if secciones:
            if type(secciones) is list:
                query['seccion']={"$in":secciones}
            else:
                query['seccion']={"$in":[secciones]}

        if url:
            query['url']=url

        return self.bd.noticias.count_documents(query)

    def secciones_existentes(self, fecha=None, diario=None, url=None):
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

        return self.bd.noticias.distinct("seccion", query)
    
    def urls_recientes(self, fecha=None, diario=None, seccion=None, limite = 100):
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

        if seccion:
            query['seccion']=seccion

        projection = {'url':True}

        #h = self.bd.noticias.find(query, projection).sort('fecha', pymongo.DESCENDING).limit(limite)
        return [u['url'] for u in self.bd.noticias.find(query, projection).sort('fecha', pymongo.DESCENDING).limit(limite)]

