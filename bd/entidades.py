import datetime
import dateutil
import logging

import yaml

import pymongo
from pymongo import MongoClient

class Kiosco:
    def __init__(self, fecha=None):
        self.bd = MongoClient().dlm

    def actualizar_diario(self, diario):
        urls = self.bd.noticias.find(filter={'diario':diario.etiqueta}, projection=['url'])
        json_noticias = [{'fecha':n.fecha, 'url':n.url, 'diario':n.diario, 'cat':n.categoria,'titulo':n.titulo, 'texto':n.texto} for n in diario.noticias if n.url not in urls]

        if len(json_noticias) == 0:
            print("no hay noticias nuevas de '" + diario.etiqueta + "'")
            logging.warning("no hay noticias nuevas de '" + diario.etiqueta + "'")
            return 0

        logging.warning("'" + diario.etiqueta + "': " + str(len(json_noticias)) + " noticias nuevas.")

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

        return self.bd.noticias.find(query, projection)

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
