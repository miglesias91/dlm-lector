import datetime
import dateutil
import logging
import json

import yaml

import pymongo
from pymongo import MongoClient

from medios.diarios.noticia import Noticia

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
